"""
#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time:2023/5/6 14:58
# @Author:Szeto YiZe
# @File:python_decode_qr_code.py
# @Update:
"""
import pyzbar.pyzbar as pyzbar
from PIL import Image
import numpy as np


def decode_qr_code(image):
    """
    解码二维码
    :param image: PIL.Image对象
    :return: 二维码内容
    """
    # 将PIL.Image对象转换为numpy数组
    img = np.array(image.convert('L'))
    # 解码二维码
    qr_codes = pyzbar.decode(img)
    # 如果没有解码到二维码，返回None
    if len(qr_codes) == 0:
        return None
    # 返回第一个二维码的内容
    return qr_codes[0].data.decode('utf-8')


# 使用示例
# 从文件中读取图片
image = Image.open('chat_list.png')
# 解码二维码
qr_code = decode_qr_code(image)
# 如果成功解码到二维码，输出二维码内容
if qr_code is not None:
    print(qr_code)
else:
    print('未识别到二维码')