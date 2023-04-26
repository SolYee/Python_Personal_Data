"""
#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time:2023/4/25 10:03
# @Author:Szeto YiZe
# @File:get_file_path.py
# @Update:
"""
import os
import time
import random

from PIL import Image
from datetime import datetime


def get_img_size(img_path):
    """获取图片大小

    :param img_path:
    :return
    """
    img = Image.open(img_path)
    # print(img.size)
    return img.size


def generate_img_url(name):
    """生成存放图片路径

    :param name:
    :return:
    """
    random_name = str(round(int(time.time())))
    # 存放OS路径
    file_name = name.format(random_name)
    # print(file_name)
    return file_name


def generate_file_url(name):
    """生成存放文件路径

    :param name:
    :return:
    """
    random_name = datetime.now().strftime("%Y%m%d/") + str(round(int(time.time())))
    # 存放OS路径
    file_name = name.format(random_name)
    # print(file_name)
    return file_name


"""
1. 首先导入了time、random和PIL库，time库用于获取当前时间，random库用于生成随机数，PIL库用于处理图片；
2. 然后定义了三个函数，get_img_size()用于获取图片大小，generate_img_url()用于生成存放图片路径，generate_file_url()用于生成存放文件路径；
3. get_img_size()函数中，使用Image.open()方法打开图片，并使用img.size获取图片大小；
4. generate_img_url()函数中，使用time.time()获取当前时间，并使用str()方法将其转换为字符串，然后使用name.format()方法生成存放图片路径；
5. generate_file_url()函数中，使用now.strftime()方法获取当前日期，并使用time.time()获取当前时间，然后使用name.format()方法生成存放文件路径。
"""
