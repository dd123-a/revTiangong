class ChatContent:
    """
      对话内容模版
      """
    text: str
    contentType: str
    cardId: str
    author: str
    createdAt: str
    options_title: str
    type: str
    suggestion: dict

    # 初始化方法，接收一个字典参数，将字典的键值对转化为类的属性
    def __init__(self, content: dict):
        self.__dict__ = content

    # 支持通过键名方式获取属性值，类似于字典操作
    def __getitem__(self, key):
        return getattr(self, key)

    # 支持通过键名方式设置属性值，类似于字典操作
    def __setitem__(self, key, value):
        setattr(self, key, value)

    # 覆盖默认的字符串转换方法，返回类属性构成的字典字符串形式
    def __str__(self):
        return str(self.__dict__)

    # 覆盖默认的呈现方法，返回类属性构成的字典字符串形式
    def __repr__(self):
        return str(self.__dict__)


class TianGongChatResponse:
    # 响应内容类型
    type: str
    # 一组对话内容，每一项为ChatContent对象
    contents: list[ChatContent] | None
    # 消息状态
    card_type: str
    # 消息ID
    target: str
    # 父消息ID
    conversation_id: str
    # 会话ID
    ask_id: str

    request_id: str

    app_copilot_input: str

    # 初始化方法，接收一个字典参数，将其中的对话响应内容解析为类属性
    def __init__(self, response: dict):
        # 将原始响应字典中的部分键值包装进类属性，并将"contents"字段转换为ChatContent对象列表
        packaged_response = {
            "type": response["type"],
            # "card_type": response["card_type"],
            "target": response["target"],
            "conversation_id": response["conversation_id"],
            "ask_id": response["ask_id"],
            "message": [ChatContent(message) for message in response["arguments"]] if response.get(
                "arguments") else None,
            "request_id": response["request_id"],
            # "app_copilot_input": response["app_copilot_input"]
        }
        self.__dict__ = packaged_response

        # 同样支持通过键名方式获取属性值
        def __getitem__(self, key):
            return getattr(self, key)

        # 同样支持通过键名方式设置属性值
        def __setitem__(self, key, value):
            setattr(self, key, value)

        # 返回类属性构成的字典字符串形式
        def __str__(self):
            return str(self.__dict__)

        # 返回类属性构成的字典字符串形式
        def __repr__(self):
            return str(self.__dict__)


# 定义历史记录响应类，用于封装一段对话历史记录的信息
class HistoryResponse:
    """
    历史记录响应模版
    """
    # 会话ID
    sessionId: str
    # 消息ID
    msgId: str
    # 消息状态
    msgStatus: str
    # 父消息ID
    parentMsgId: str
    # 内容类型
    contentType: str
    # 一组对话内容，每一项为ChatContent对象
    contents: list[ChatContent] | None
    # 发送者类型，比如用户、机器人等
    senderType: str
    # 创建时间戳
    createTime: int

    # 初始化方法，接收一个字典参数，将历史记录信息解析为类属性
    def __init__(self, response: dict):
        # 将历史记录响应字典中的信息包装进类属性，并将"contents"字段转换为ChatContent对象列表
        packaged_response = {
            "sessionId": response["sessionId"],
            "msgId": response["msgId"],
            "msgStatus": response["msgStatus"],
            "parentMsgId": response["parentMsgId"],
            "contentType": response["contentType"],
            "contents": [ChatContent(content) for content in response["contents"]] if response.get(
                "contents") else None,
            "senderType": response["senderType"],
            "createTime": response["createTime"]
        }
        self.__dict__ = packaged_response

    # 同样支持通过键名方式获取属性值
    def __getitem__(self, key):
        return getattr(self, key)

    # 同样支持通过键名方式设置属性值
    def __setitem__(self, key, value):
        setattr(self, key, value)

    # 返回类属性构成的字典字符串形式
    def __str__(self):
        return str(self.__dict__)

    # 返回类属性构成的字典字符串形式
    def __repr__(self):
        return str(self.__dict__)


# 定义通用响应类，用于处理非特定格式的一般性响应数据
class OrdinaryResponse:
    # 初始化方法，接收一个字典参数，直接将其键值对转换为类属性
    def __init__(self, response: dict):
        self.__dict__ = response

    # 同样支持通过键名方式获取属性值
    def __getitem__(self, key):
        return getattr(self, key)

    # 同样支持通过键名方式设置属性值
    def __setitem__(self, key, value):
        setattr(self, key, value)

    # 返回类属性构成的字典字符串形式
    def __str__(self):
        return str(self.__dict__)

    # 返回类属性构成的字典字符串形式
    def __repr__(self):
        return str(self.__dict__)
