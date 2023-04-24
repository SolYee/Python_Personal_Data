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
