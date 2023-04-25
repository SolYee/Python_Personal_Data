"""
#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time:2023/4/24 9:37
# @Author: Szeto YiZe
# @File:test_logging_file.py
# @Update:
"""
import logging


def setup_logger(name, log_file, level=logging.INFO):
    """设置日志记录器

    :param name: 日志记录器名称
    :param log_file: 日志文件路径
    :param level: 日志记录级别
    :return: 日志记录器对象
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)

    handler = logging.FileHandler(log_file)
    handler.setLevel(level)

    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    handler.setFormatter(formatter)

    logger.addHandler(handler)

    return logger


def log_request(logger, path, params, result):
    """记录请求日志

    :param logger: 日志记录器对象
    :param path: 请求路径
    :param params: 请求参数
    :param result: 输出结果
    """
    logger.info(f'请求路径：{path}，请求参数：{params}，输出结果：{result}')
    # logger.info('请求路径：%s，请求参数：%s，输出结果：%s', path, params, result)


"""
上面的代码中，我们定义了两个函数：

- `setup_logger()`：用于设置日志记录器，接受三个参数：`name`表示日志记录器的名称，`log_file`表示日志文件的路径，`level`表示日志记录的级别。
在函数中，我们创建了一个名为`logger`的日志记录器对象，并将其级别设置为传入的`level`参数。然后创建一个名为`handler`的日志处理器对象，用于将日志记录到指定的文件中。
接着创建一个名为`formatter`的日志格式化器对象，将其格式设置为包含时间、级别和消息的格式。最后将处理器和格式化器分别添加到日志记录器对象中，并返回记录器对象。
- `log_request()`：用于记录请求日志，接受四个参数：`logger`表示日志记录器对象，`path`表示请求的路径，`params`表示请求的参数，`result`表示输出的结果。
在函数中，我们调用日志记录器对象的`info()`方法，将请求路径、请求参数和输出结果作为参数传入，生成日志。

使用时，可以先调用`setup_logger()`函数创建一个日志记录器对象，然后在需要记录请求日志的地方，调用`log_request()`函数即可。
例如：

```python
logger = setup_logger('test_logger', 'log.txt')
log_request(logger, '/path/to/api', {'key': 'value'}, 'result')
```
这样，就可以方便地记录请求日志了。
"""

import os
import sys
import time
from loguru import logger
from typing import Union

LOG_DIR: Union[bytes, str] = os.path.dirname(os.path.abspath(__file__))

my_log_file_path = os.path.join(LOG_DIR, time.strftime("%Y-%m-%d.log"))


# 2 用法
class Loggings:
    __instance = None

    def __init__(self, log_file_path=my_log_file_path):
        self.logger = logger
        # 清空所有设置
        self.logger.remove()
        # 添加控制台输出的格式,sys.stdout为输出到屏幕;关于这些配置还需要自定义请移步官网查看相关参数说明
        self.logger.add(sys.stdout,
                        format="<green>{time:HH:mm:ss</green>"  # 颜色>时间
                               "ccyan>(moduleJ</cyan>,<cyan>{function}</cyan>"  # 横块名.方法名{process ,name)"# 进程名
                               "{thread.name]"  # 进程名
                               ":<cyan>{lineJ</cyan>"  # 行号
                               "<level>{levelJ</level>:"  # 等级
                               "<level>{messageJ</level>")  # 日志内容
        # 输出到文件的格式，注释下面的add",则关闭日志写入
        self.logger.add(log_file_path, level='DEBUG',
                        format='{time :HH:mm:ss}-'  # 时间
                               "(process ,name}|"  # 进程名
                               "{thread.name}]"  # 进程名
                               "{module}.{function}:{line} - [level》 -{message》",  # 模块名.方法名:行号
                        rotation="500MB",
                        encoding="utf-8",
                        enqueue=True,
                        retention="10 week")

    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = super(Loggings, cls).__new__(cls, *args, **kwargs)
        return cls.__instance

    def get_logger(self):
        return self.logger


"""
以上代码是一个封装了第三方库 `loguru` 的类，用于输出日志到控制台和文件中。

代码中定义了一个 `Loggings` 类，该类实现了单例模式，即只有一个实例对象，避免了多次调用时重复创建对象。`__init__()` 方法用于进行初始化操作，
接受一个参数 `log_file_path` 表示日志文件的路径，默认值为当天的日期。

在 `__init__()` 方法中，首先创建一个 `logger` 对象，然后使用 `remove()` 方法清空所有之前的设置。接着使用 `add()` 方法添加一个日志输出处理器，这个处理器用于将日志输出到控制台。
其中，`sys.stdout` 表示日志输出到标准输出流（即控制台），`format` 参数表示日志输出的格式，其中包括时间、进程名、线程名、行号、日志级别和日志内容等信息。
这里使用了一些颜色和 `loguru` 库的相关 API 来实现颜色和样式的输出。

然后使用 `add()` 方法再添加一个日志输出处理器，这个处理器用于将日志写入文件。
其中，`format` 参数表示日志输出到文件的格式，`rotation` 参数表示日志文件的自动轮换大小，`encoding` 参数表示日志文件的编码格式，`enqueue` 参数表示是否在异步进程队列中处理日志记录，
`retention` 参数表示日志文件的最大保留时间。

最后定义了一个 `get_logger()` 方法，用于获取 `logger` 对象。需要注意的是，这个 `get_logger()` 方法没有实现任何功能，需要根据实际需求自行实现。

`Loggings` 类的单例模式实现方式是通过 `__new__()` 方法实现的，该方法在对象实例化时被调用，如果类的实例对象已经存在，则直接返回该对象，否则执行父类 `__new__()` 方法创建新的实例对象。
"""

# import os
# import sys
# import loguru
# import time
# from typing import Union
#
# LOG_DIR: Union[bytes, str] = os.path.dirname(os.path.abspath(__file__))
#
#
#
# class Loggings:
#     __instance = None
#
#     def __new__(cls, *args, **kwargs):
#         if not cls.__instance:
#             cls.__instance = super().__new__(cls)
#         return cls.__instance
#
#     def __init__(self, log_file_path=my_log_file_path):
#         self.logger = logger
#         # 清空所有设置
#         self.logger.remove()
#         # 添加控制台输出的格式,sys.stdout为输出到屏幕;关于这些配置还需要自定义请移步官网查看相关参数说明
#         self.logger.add(sys.stdout,
#                         format="<green>{time:HH:mm:ss</green>"  # 颜色>时间
#                                "ccyan>(moduleJ</cyan>,<cyan>{function}</cyan>"  # 横块名.方法名{process ,name)"# 进程名
#                                "{thread.name]"  # 进程名
#                                ":<cyan>{lineJ</cyan>"  # 行号
#                                "<level>{levelJ</level>:"  # 等级
#                                "<level>{messageJ</level>")  # 日志内容
#         # 输出到文件的格式，注释下面的add",则关闭日志写入
#         self.logger.add(log_file_path,
#                         rotation="1 day",
#                         encoding="utf-8",
#                         enqueue=True,
#                         retention="7 days",
#                         format="<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green>"
#                                " <cyan>{name}:{function}:{line}</cyan> - "
#                                "<level>{level}: {message}</level>")
#
#     def get_logger(self):
#         return self.logger
