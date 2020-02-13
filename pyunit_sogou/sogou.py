#!/usr/bin/python3.7
# -*- coding: utf-8 -*-
# @Time : 2019/1/24 0024
# @Email : jtyoui@qq.com
from urllib.parse import quote
from fake_useragent import UserAgent
import requests
import struct
import re


class SoGou:
    """
    爬取搜狗只需要三步：\n
    第一步：搜索关键字。爬取关键字的下载链接\n
    第二步：筛选下载链接，进行下载\n
    第三步：将下载的搜狗文件转化为UTF-8格式
    """

    def __init__(self):
        self.ua = UserAgent()

    def download_all_lexicon(self):
        pass

    def search_name(self, search_name):
        url_word = quote(search_name.encode('GBK'))  # 将中文字转化为URL链接。注意搜狗将中文字进行的GBK编码。而不是UTF-8
        urls = 'https://pinyin.sogou.com/dict/search/search_list/%s/normal/' % url_word  # 搜索链接
        response = requests.get(url=urls, headers={'User-Agent': self.ua.random})
        match = re.findall(urls[24:] + '(.{1,3})">', response.text)  # 匹配下载页数
        max_page = max(map(lambda x: int(x), match)) if match else 1  # 选取最大的页数，如果没有页数返回1
        m = []  # 将匹配到下载链接
        for page in range(1, max_page + 1):
            response = requests.get(url=urls + str(page), headers={'User-Agent': self.ua.random})
            match = re.findall(r'id=(.+)&name=(.+)"', response.text)  # 匹配下载链接
            m.extend(match)  # 将匹配到的下载链接装到链表中
        load_url = 'https://pinyin.sogou.com/d/dict/download_cell.php?id={0}&name={1}'  # 下载链接的格式
        # 将匹配到的，名字和ID映射到下载链接格式中
        return map(lambda x: load_url.format(x[0], x[1]), m)

    def url_to_text(self, url_word):
        """下载搜狗文件

        :param url_word: 下载链接
        :return: 转化好的搜狗文件。返回格式的链表
        """
        load_ls = {}  # 字典的键是下载词库的名字。字典的值是词库的内容
        name = url_word[url_word.rfind('=') + 1:]
        response = requests.get(url=url_word, headers={'User-Agent': self.ua.random})
        load_ls[name] = self._to_txt(response.content)
        return load_ls  # 返回字典

    @staticmethod
    def _to_txt(data):
        """转写搜狗文件格式"""
        ls_word = []  # 转化搜狗为UTF-8格式内容
        w = ''  # 每一个词条
        for i in range(0, len(data), 2):
            x = data[i:i + 2]  # 搜狗的UTF-8编码是两个字节
            t = struct.unpack('H', x)[0]  # 将其转化为无符号的短整形
            if 19968 < t < 40959 or t == 10:  # 判断是否是中文字符。10表示的是换行
                if t != 10:  # 不换行放在单个词条
                    w += chr(t)
                elif t == 10 and len(w):  # 换行且不等于空
                    ls_word.append(w)
                    w = ''
        return ls_word[1:]  # 第一行是注释。不需要，去除第一行
