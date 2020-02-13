#!/usr/bin/python3.7
# -*- coding: utf-8 -*-
# @Time  : 2018/2/28 10:58
# @Author: Jtyoui@qq.com
from pyunit_sogou import SoGou


def test():
    """测试"""
    sg = SoGou()  # 获取搜索关键字下的词库
    res = sg.search_name('LOL英雄联盟')
    for u in res:  # 遍历关键字下的URL
        txt = sg.url_to_text(u)  # 下载
        print(txt)  # 打印


if __name__ == '__main__':
    test()
