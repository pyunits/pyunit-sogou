#!/usr/bin/python3.7
# -*- coding: utf-8 -*-
# @Time  : 2018/2/28 10:58
# @Author: Jtyoui@qq.com
from pyunit_newword import NewWords


def test():
    """测试"""
    nw = NewWords(accuracy=0.01)
    nw.add_text(r'C:\Users\Administrator\Desktop\西游记.txt')
    nw.analysis_data()
    for word in nw.get_words():
        print(word[0])


if __name__ == '__main__':
    test()
