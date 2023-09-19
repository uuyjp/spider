# -*- coding: utf-8 -*-
# @Time    : 18/9/2023 下午 1:45
# @Author  : 明月清风我
# @File    : test.py
# @Software: PyCharm
import os
path = './mv'      # 输入文件夹地址
files = os.listdir(path)   # 读入文件夹
num_png = len(files)       # 统计文件夹中的文件个数
print(num_png)             # 打印文件个数
