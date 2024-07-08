# revTianGong/__init__.py

# 导入当前包的子模块，如果需要的话
from .entity import ChatContent, TianGongChatResponse, HistoryResponse, OrdinaryResponse
from .errors import TianGongProtocalError
from .tiangong import Chatbot, gen_request_id

# 定义包的版本信息
__version__ = '0.1.0'

# 定义包的作者信息
__author__ = 'DrTang'

# 如果需要，可以设置 __all__ 列表来控制 from revTianGong import * 的行为
__all__ = [
    'ChatContent',
    'TianGongChatResponse',
    'HistoryResponse',
    'OrdinaryResponse',
    'TianGongProtocalError',
    'Chatbot',
    'gen_request_id',
    '__version__',
    '__author__',
]

# 包初始化代码，例如打印欢迎信息
def __init_package__():
    print("Welcome to the revTianGong package!")

# 以下代码会在包被导入时执行
__init_package__()