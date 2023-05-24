"""
#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time:2023/5/17 10:55
# @Author:Szeto YiZe
# @File:OpenFileManager.py
# @Update:使用 `plyer` 库调用 Android 设备的相册等功能。
"""

from plyer import filechooser


# 打开相册
def open_gallery():
    selected_file = filechooser.open_file(title='Select a file', filters=[('Images', '*.jpg')])
    print(selected_file)


# 打开文件管理器
def open_file_manager():
    selected_file = filechooser.choose_directory(title='Select a directory')
    print(selected_file)

