# -*- coding = utf-8 -*-
# @Time：2020-10-29 19:20
# @Author：来瓶安慕嘻
# @File：网易云1.2.py
# @开始美好的一天吧 @Q_Q@

import requests
from lxml import etree
import re
import os
import time

if __name__ == "__main__":
    if not os.path.exists('./林俊杰2'):
        os.mkdir('./林俊杰2')

    proxy = {'http':'222.189.191.246:9999'}
    url = "https://music.163.com/artist?id=3684"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4270.0 Safari/537.36"
    }
    page_text = requests.get(url=url, headers=headers,proxies=proxy).text

    # # 自己创建一个page_text用来调试
    # with open('网易云.text','w',encoding='utf-8') as f:
    #     f.write(page_text)


    # 利用etree进行网页解析
    tree1 = etree.HTML(page_text)

    # 获取歌曲id
    music_list = tree1.xpath('//a[contains(@href,"/song?")]/@href')
    for music in music_list:
        music_id_first= music.split('=')[1]
        # print(music_id_first)
        # 清洗所有的ID
        if "$" not in music_id_first:
            music_id = music_id_first
            music_name = tree1.xpath('//a[contains(@href,"/song?id='+music_id+
                                     '")]/text()')[0]
            # 下载链接下载网易云音乐
            # base_url = 'https://link.hhtjim.com/163/'+music_id+'.mp3'
            # https://link.hhtjim.com/163/64625.mp3
            # https://music.163.com/song/media/outer/url?id=413812448

            base_url = 'https://music.163.com/song/media/outer/url?id='+music_id

            with open('./林俊杰2/'+music_name+'.mp3','wb')as fp:
                music_text = requests.get(url=base_url,headers=headers,proxies=proxy).content
                fp.write(music_text)
                print('%s下载完成'%music_name)
        time.sleep(1)