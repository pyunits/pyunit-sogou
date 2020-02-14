#!/usr/bin/python3.7
# -*- coding: utf-8 -*-
# @Time  : 2018/2/28 10:58
# @Author: Jtyoui@qq.com
from pyunit_sogou import SoGou


def test_search_name():
    """测试搜索关键词来下载词库"""
    sg = SoGou()  # 获取搜索关键字下的词库
    res = sg.search_name_lexicon('化学')
    for url in res:  # 遍历关键字下的URL
        print(url)
        txt = sg.download_to_text(url)  # 下载
        print(txt)  # 打印
        break


def test_download_scel():
    """测试下载scel库文件"""
    sg = SoGou()
    path = sg.download_to_scel('http://download.pinyin.sogou.com/dict/download_cell.php?id=15205&name=化学化工词汇大全【官方推荐】',
                               './lexicon')
    print(path)


def test_download_text():
    """测试下载词库转为文本内容"""
    sg = SoGou()
    path = sg.download_to_text('http://download.pinyin.sogou.com/dict/download_cell.php?id=15205&name=化学化工词汇大全【官方推荐】')
    print(path)


def test_download_classify():
    """测试下载词库分类"""
    sg = SoGou()
    one = sg.one_classify_lexicon('https://pinyin.sogou.com/dict/cate/index/13')  # 化学分类
    for url in one:
        print(url)
        txt = sg.download_to_text(url)  # 下载
        print(txt)  # 打印
        break


def test_save_txt():
    sg = SoGou()
    urls = sg.one_classify_lexicon('https://pinyin.sogou.com/dict/cate/index/13')  # 化学分类
    for url in urls:
        result = sg.download_to_txt(url, './化学分类')
        print(result)
        break


if __name__ == '__main__':
    # test_search_name()
    # test_download_scel()
    # test_download_text()
    # test_download_classify()
    test_save_txt()
