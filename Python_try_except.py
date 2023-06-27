"""
#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time:2023/6/26 14:03
# @Author:Szeto YiZe
# @File:Python_try_except.py
# @Update: Python 异常处理
"""

# -*- coding: UTF-8 -*-
import json
import traceback
import logging

logger = logging.getLogger(__name__)


def load_json(file):
    try:
        with open(file, 'r') as f:
            return json.loads(f.read())
    except FileNotFoundError:
        logger.exception(f"File not found error occurred while loading {file}")
    except json.JSONDecodeError:
        logger.exception(f"JSON decode error occurred while loading {file}")
    except:
        logger.exception(f"An unexpected error occurred while loading {file}")


def test():

    try:
        ret = load_json('a.json')
        return {'err': 'success', 'result': ret}
    except Exception as e:
        logger.error(f"load json exception:{str(e)}")
        logger.error(e.format_exc())
        return {'err': 'exception'}


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    test()


"""该代码实现了一个简单的读取 JSON 文件的函数，并使用 logging 库记录错误日志，可以方便地对不同的 JSON 文件进行读取测试。
但需要注意，该函数只能读取符合 JSON 格式的文件，否则会出现 JSON 解析错误。"""