import asyncio
import hashlib
import json
import logging
import typing
import uuid

import filetype
import requests
import websockets
from fake_useragent import UserAgent
from websockets.exceptions import ConnectionClosedOK, ConnectionClosedError

from . import errors
from .entity import *


def gen_request_id() -> str:
    """生成requestId"""
    # uuid无分隔符
    request_id = uuid.uuid4().hex
    return request_id


class Chatbot:
    """天工 Chatbot 对象"""

    api_base: str = "wss://work.tiangong.cn/agents_api/chat/ws?device=Web&device_id=825c6b2e8d2ebd9bb4808c55056b969c&device_hash=825c6b2e8d2ebd9bb4808c55056b969c&app_version=1.7.3"

    cookies: dict

    cookies_str: str

    userId: str
    """Current user id"""

    title: str
    """Title of current session"""

    sessionId: str = ""
    """Current session id"""

    parentId: str = "0"
    """Parent msg id"""

    def __init__(
            self,
            cookies: dict = None,
            cookies_str: str = "",
    ):

        if cookies and cookies_str:
            raise ValueError("cookies和cookies_str不能同时存在")

        if cookies:
            self.cookies = cookies
            self.cookies_str = ""
            for key in cookies:
                self.cookies_str += "{}={}; ".format(key, cookies[key])
        elif cookies_str:
            self.cookies_str = cookies_str

            spt = self.cookies_str.split(";")

            self.cookies = {}

            for it in spt:
                it = it.strip()
                if it:
                    equ_loc = it.find("=")
                    key = it[:equ_loc]
                    value = it[equ_loc + 1:]
                    self.cookies[key] = value

        logging.debug(self.cookies)

        self.headers = {
            'Pragma': 'no-cache',
            'Origin': 'https://www.tiangong.cn',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Sec-WebSocket-Key': 'tb2KERRebVx0hf6Yr5HGgA==',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36 SLBrowser/9.0.3.1311 SLBChan/103',
            'Upgrade': 'websocket',
            'Cache-Control': 'no-cache',
            'Connection': 'Upgrade',
            'Sec-WebSocket-Version': '13',
            'Sec-WebSocket-Extensions': 'permessage-deflate; client_max_window_bits',
            "Cookie": self.cookies_str
        }

    async def _stream_ask(
            self,
            prompt: str,
            parentId: str = "0",
            sessionId: str = "",
            timeout: int = 60,
            image: bytes = None
    ) -> typing.Generator[TianGongChatResponse, None, None]:
        """流式回复

        Args:
            prompt (str): 提问内容
            parentId (str, optional): 父消息id. Defaults to "0".
            sessionId (str, optional): 对话id. Defaults to "".
            timeout (int, optional): 超时时间. Defaults to 60.
            image (bytes, optional): 图片二进制数据. Defaults to None.
        """
        if parentId == "0":
            self.parentId = self.parentId

        headers = self.headers.copy()

        headers['Accept'] = 'text/event-stream'

        data = {
            "agent_id": "016",
            "agent_type": "universal",
            "conversation_id": "6322210d-567b-42bb-983b-6c26f417d2f2",
            "prompt": {
                "action": None,
                "ask_from": "user",
                "ask_id": None,
                "content": prompt,
                "prompt_content": None,
                "template_id": None,
                "action": None,
                "file": None,
                "template": None,
                "copilot": False,
                "bubble_text": None,
                "publish_agent": None,
                "copilot_option": None
            },
        }
        async with websockets.connect(self.api_base, extra_headers=headers) as websocket:
            # 将JSON消息转换为字符串并发送
            json_message_str = json.dumps(data)
            await websocket.send(json_message_str)

            while True:
                try:
                    message = await websocket.recv()
                    data_dict = json.loads(message)
                    if message is not None and data_dict['type'] != 101:
                        result = TianGongChatResponse(data_dict)

                        if data_dict['type'] == 2:
                            break
                        yield result
                except json.JSONDecodeError:
                    # 当接收到的消息无法解析为JSON时的处理
                    print("Received message cannot be decoded as JSON.")
                    break
                except ConnectionClosedOK as e:
                    raise e
                    break
                except ConnectionClosedError as e:
                    raise e
                    break

        logging.debug("done: {}".format(result))

    async def _non_stream_ask(
            self,
            prompt: str,
            parentId: str = "0",
            sessionId: str = "",
            timeout: int = 60,
            image: bytes = None
    ) -> TianGongChatResponse:
        """非流式回复

        Args:
            prompt (str): 提问内容
            parentId (str, optional): 父消息id. Defaults to "0".
            sessionId (str, optional): 对话id. Defaults to "".
            timeout (int, optional): 超时时间. Defaults to 60.
            image (bytes, optional): 图片二进制数据. Defaults to None.
        """

        result = {
            'texts': "",
            'suggestion': "",
        }
        async for message in self._stream_ask(prompt, parentId, sessionId, timeout, image):
            # 更新result字典，对于已存在的键，覆盖其值；对于新键，则添加进字典
            message = message.__dict__
            if 'message' in message and isinstance(message['message'], list) and message['message']:
                if 'text' in message['message'][0]['messages'][0]:
                    result['texts'] += str(message['message'][0]['messages'][0]['text'])
                if 'suggestedResponses' in message['message'][0]['messages'][0]:
                    result['suggestion'] += str(message['message'][0]['messages'][0]['suggestedResponses'])
        return result

    async def ask(
            self,
            prompt: str,
            parentId: str = "0",
            sessionId: str = "",
            timeout: int = 60,
            stream: bool = False,
            image: bytes = None
    ) -> typing.Union[typing.Generator[TianGongChatResponse, None, None], TianGongChatResponse]:
        """提问

        Args:
            prompt (str): 提问内容
            parentId (str, optional): 父消息id. Defaults to "0".
            sessionId (str, optional): 对话id. Defaults to "".
            timeout (int, optional): 超时时间. Defaults to 60.
            stream (bool, optional): 是否流式. Defaults to False.
            image (bytes, optional): 图片二进制数据. Defaults to None.
        """

        return await (self._non_stream_ask(
            prompt,
            parentId,
            sessionId,
            timeout,
            image
        ))
