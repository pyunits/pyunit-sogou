#!/usr/bin/python3.7
# -*- coding: utf-8 -*-
# @Time : 2019/1/24 0024
# @Email : jtyoui@qq.com
from urllib.parse import quote, unquote
from fake_useragent import UserAgent
import requests
import struct
import re
import os
import math


class SoGou:
    """
    爬取搜狗只需要三步：\n
    第一步：搜索关键字。爬取关键字的下载链接\n
    第二步：筛选下载链接，进行下载\n
    第三步：将下载的搜狗文件转化为UTF-8格式
    """

    def __init__(self):
        self.ua = UserAgent()

    def download_all_lexicon(self, start=0, end=629):
        """下载全部的分类词库

        :param start: 最久的分类索引
        :param end: 最新的分类索引
        :return: 爬取搜狗下的所有词库
        """
        for page in range(start, end):
            url = f'https://pinyin.sogou.com/dict/cate/index/{page}'
            data = self.one_classify_lexicon(url)
            yield data

    def one_classify_lexicon(self, url):
        """下载一个分类下的词库

        点击链接可以查看词库：https://pinyin.sogou.com/dict/cate/index/1 \n
        选中某一个分类，获取该分类下的URL链接

        >>> SoGou().one_classify_lexicon('https://pinyin.sogou.com/dict/cate/index/13') #下载化学分类词库

        :param url: 分类词库链接
        :return: 该分类下的所有词库信息
        """
        response = requests.get(url=url, headers={'User-Agent': self.ua.random}).text
        max_page = re.search('分类下共有(.+)个词库', response).group(1)
        urls = re.findall('http://download.pinyin.sogou.com/dict/download_cell.php?.+"', response)
        for page in range(2, math.ceil(int(max_page) / 10) + 1):
            response = requests.get(url=url + f'/default/{page}', headers={'User-Agent': self.ua.random}).text
            urls.extend(re.findall('http://download.pinyin.sogou.com/dict/download_cell.php?.+"', response))
        return map(lambda x: unquote(x[:-1]), urls)

    def search_name_lexicon(self, search_name):
        """根据名字来搜索词库

        :param search_name: 名称
        :return: 返回词库的下载链接
        """
        url_word = quote(search_name.encode('GBK'))  # 将中文字转化为URL链接。注意搜狗将中文字进行的GBK编码。而不是UTF-8
        urls = 'https://pinyin.sogou.com/dict/search/search_list/%s/normal/' % url_word  # 搜索链接
        response = requests.get(url=urls, headers={'User-Agent': self.ua.random}).text
        max_page = re.search('共有(.+)个搜索结果', response).group(1)
        m = re.findall('//pinyin.sogou.com/d/dict/download_cell.php?.+"', response)
        for page in range(2, math.ceil(int(max_page) / 10) + 1):
            response = requests.get(url=urls + str(page), headers={'User-Agent': self.ua.random}).text
            m.extend(re.findall('//pinyin.sogou.com/d/dict/download_cell.php?.+"', response))  # 将匹配到的下载链接装到链表中
        return map(lambda x: 'https:' + x[:-1], m)

    @staticmethod
    def _url_to_chinese(url):
        """将URL解码成中文"""
        url_word = unquote(url)
        match = re.search('name=(.+)&|name=(.+)', url_word)
        name = match.group(1) if match.group(1) else match.group(2)
        return name, url_word

    def download_to_text(self, url_word):
        """根据词库链接下载搜狗文件

        :param url_word: 词库链接
        :return: 转化好的搜狗文件。返回格式的链表
        """
        name, url_word = self._url_to_chinese(url_word)
        response = requests.get(url=url_word, headers={'User-Agent': self.ua.random})
        return name, self._to_txt(response.content)

    def download_to_scel(self, url_word, save_dir):
        """根据词库链接下载词库文件scel

        :param url_word: 词库链接
        :param save_dir: 保存词库的文件夹
        :return: 保存成功返回保存文件的地址
        """
        if not os.path.isdir(save_dir):
            os.makedirs(save_dir)
        name, url_word = self._url_to_chinese(url_word)
        path = os.path.abspath(save_dir) + os.sep + name + '.scel'
        response = requests.get(url=url_word, headers={'User-Agent': self.ua.random})
        with open(path, mode='wb')as f:
            f.write(response.content)
        return path

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

    def download_to_txt(self, url, txt_dir):
        """保存为txt文件

        :param url: 要下载的url链接
        :param txt_dir: 保存txt文件夹路径
        :return: 返回保存文件的地址
        """
        if not os.path.isdir(txt_dir):
            os.makedirs(txt_dir)
        name, text = self.download_to_text(url)
        path = os.path.abspath(txt_dir) + os.sep + name + '.txt'
        with open(path, 'w', encoding='utf-8')as f:
            f.writelines(t + '\n' for t in text)
        return path
