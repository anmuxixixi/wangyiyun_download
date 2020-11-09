# -*- coding = utf-8 -*-
# @Time：2020-10-31 16:59
# @Author：来瓶安慕嘻
# @File：网易云2.0.py
# @开始美好的一天吧 @Q_Q@

from PySide2.QtWidgets import QApplication, QMessageBox, QTextBrowser, QTextEdit, QTableWidgetItem, QFileDialog
from PySide2.QtUiTools import QUiLoader
from PyQt5 import QtGui
from PySide2.QtCore import Signal, QObject
from threading import Thread
import time
import requests
import cloudmusic
from lxml import etree
import os
import matplotlib.pyplot as plt  # 数据可视化
import jieba  # 词语切割
import wordcloud
from wordcloud import WordCloud, ImageColorGenerator  # 词云，颜色生成器
import numpy as np
from PIL import Image  # 处理图片
from PySide2.QtGui import  QIcon
import sys

class Mysignals(QObject):
    text_print = Signal(QTextBrowser, str)  # 将爬虫信息打印在主窗口上
    progress_display = Signal(float)  # 将下载歌曲的进度展示在主窗口进度条上
    table_insert = Signal(dict)  # 将歌手的信息展示在主窗口表格中


class WangYiYun_Download():
    def __init__(self):
        # 设置是否先点击了下载目录按钮（这段代码的思路真的写的好香，我先迷恋我自己一下
        self.flag1 = False
        self.start_num = 0
        self.item = 0

        # 爬虫初始化
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4270.0 Safari/537.36"
        }
        self.music_info = []

        # UI设计初始化
        self.ui = QUiLoader().load('wangyiyun.ui')
        self.ui.setWindowTitle('网易云1.0')
        self.ui.loadText.setReadOnly(True)
        self.ui.searchButton.clicked.connect(self.wangyiyun_spyider)
        self.ui.dictPath.clicked.connect(self.choose_path)
        self.ui.pageBox.setValue(10)
        self.ui.startdownbutton.clicked.connect(self.song_download)
        self.ui.ciyunButton.clicked.connect(self.comment_spider)
        self.ui.tableWidget.setColumnWidth(0, 500)
        self.ui.stopdownloadButton.clicked.connect(self.stop_song_download)

        # 信号实例化
        self.ms = Mysignals()
        self.ms.text_print.connect(self.printToGui)  # 连接到打印函数
        self.ms.progress_display.connect(self.displayToGui)  # 连接到展示进度条函数
        self.ms.table_insert.connect(self.insertToGui)  # 连接到表格填充函数

    # -----------------------------------Mysignals相关函数--------------------------------------------------------
    def printToGui(self, fb, text):
        fb.append(str(text))
        fb.ensureCursorVisible()

    def displayToGui(self, num):
        self.ui.progressBar.setValue(num)

    def insertToGui(self, text1):
        self.ui.tableWidget.insertRow(0)

        item1 = QTableWidgetItem()
        item1.setText(text1)

        self.ui.tableWidget.setItem(0, 0, item1)

    # ----------------------------------用来获取用户输入作者的左右歌曲的ID------------------------------------------------
    def wangyiyun_spyider(self):
        # 获取用户在输入栏的信息
        self.info = self.ui.artistText.toPlainText()

        # 利用cloudmusic获取作者的ID（后期还需要优化）
        music = cloudmusic.search(self.info)
        artist_id = music[0].artistId

        url = "https://music.163.com/artist?id=" + str(artist_id[0])  # 拼接ID，生成作者页信息

        page_text = requests.get(url=url, headers=self.headers).text

        # 利用etree进行网页解析
        tree1 = etree.HTML(page_text)

        # 定位所有的歌曲
        music_list = tree1.xpath('//a[contains(@href,"/song?")]/@href')

        # run1用来建一个新的线程，主要实现的功能为：1.获取歌曲名称 2.获取歌曲ID
        def run1():
            for music in music_list:
                music_id_first = music.split('=')[1]
                # print(music_id_first)
                # 清洗所有的ID
                if "$" not in music_id_first:
                    music_id = music_id_first
                    music_name = tree1.xpath('//a[contains(@href,"/song?id=' + music_id +
                                             '")]/text()')[0]

                    self.ms.table_insert.emit(music_name)

                    data = {'name': music_name, 'id': music_id}
                    self.music_info.append(data)

        t1 = Thread(target=run1)  # 一定不要写成run1()  切记！！！  不然程序崩溃 调试了一晚上才发现这个错误
        t1.start()

    # --------------------------------下载网易云音乐歌曲---------------------------------------------------------------
    def song_download(self):
        if self.flag1:
            self.flag2 = True
            if not os.path.exists(self.FileDirectory + '/音乐文件'):
                os.mkdir(self.FileDirectory + '/音乐文件')

            # 设置进度条
            song_num = len(self.music_info)
            self.ui.progressBar.setRange(0, song_num)

            def run2():
                for item in range(self.start_num, song_num):
                    self.item = item
                    base_url = 'https://link.hhtjim.com/163/' + self.music_info[item]['id'] + '.mp3'
                    if self.flag2:
                        with open(self.FileDirectory + '/音乐文件/' + self.music_info[item]['name'] + '.mp3', 'wb')as fp:
                            music_text = requests.get(url=base_url, headers=self.headers).content
                            fp.write(music_text)
                            self.ms.text_print.emit(self.ui.loadText, self.music_info[item]['name'] + '   下载完成...')
                            self.ms.progress_display.emit(item + 1)

            t2 = Thread(target=run2)
            t2.start()
        else:
            self.warning_info()

    # --------------------------------停止下载网易云音乐歌曲---------------------------------------------------------------
    def stop_song_download(self):
        self.flag2 = False
        self.start_num = self.item+1

    # -------------------------------------选择存储音乐文件的路径---------------------------------------------------------------
    def choose_path(self):
        self.flag1 = True
        FileDialog = QFileDialog(self.ui)
        self.FileDirectory = FileDialog.getExistingDirectory(self.ui)

    # ------------------------------------爬取网易云音乐评论-------------------------------------------------------------------
    def comment_spider(self):
        if self.flag1:
            if not os.path.exists(self.FileDirectory + '/词云文件'):
                os.mkdir(self.FileDirectory + '/词云文件')

            item = QTableWidgetItem()
            music_row = self.ui.tableWidget.currentRow() + 1
            text = self.ui.tableWidget.item(music_row - 1, 0).text()  # 获取选中文件的歌名
            # 匹配到选中歌名对应的歌曲ID
            for i in range(len(self.music_info)):
                if self.music_info[i]['name'] == text:
                    music_id = self.music_info[i]['id']

            page = self.ui.pageBox.value()  # 获取用户需要的评论的页数
            comment_url = 'http://music.163.com/api/v1/resource/comments/R_SO_4_' + music_id + '?limit=20'
            with open(self.FileDirectory + '/词云文件/' + text + '.txt', 'w', encoding='utf-8')as f:
                if page == 1:
                    comment_text = requests.get(comment_url, headers=self.headers).json()
                    for i in range(15):
                        f.write(comment_text['hotComments'][i]['content'])
                        f.write('\n')
                    for i in range(20):
                        f.write(comment_text['comments'][i]['content'])
                        f.write('\n')
                else:
                    for i in range(page):
                        if i == 0:
                            comment_text = requests.get(comment_url, headers=self.headers).json()
                            for j in range(15):
                                f.write(comment_text['hotComments'][j]['content'])
                                f.write('\n')
                            for j in range(20):
                                f.write(comment_text['comments'][j]['content'])
                                f.write('\n')
                        else:
                            comment_url2 = comment_url + '&offset=' + str(i * 20)
                            comment_text = requests.get(comment_url2, headers=self.headers).json()
                            for j in range(20):
                                f.write(comment_text['comments'][j]['content'])
                                f.write('\n')
                        time.sleep(0.5)
            self.generate_cloudpic(text)


        else:
            self.warning_info()

    # ----------------------------------------生成词云图--------------------------------------------------------------
    def generate_cloudpic(self, text):
        with open('stop_words.txt', 'r', encoding='utf-8') as f:
            stop = f.read()
            stop = stop  # 具体问题添加具体的停用词
        stop = stop.split()

        print(self.FileDirectory + '/词云文件/' + text + '.txt')

        # 打开目标文档
        with open(self.FileDirectory + '/词云文件/' + text + '.txt', 'r', encoding='utf-8') as f:  # 打开新的文本转码为gbk
            textfile = f.read()  # 读取文本内容

        wordlist = jieba.lcut(textfile)  # 切割词语

        # 调用停用词列表
        result_wordlist = []
        for word in wordlist:
            if word not in stop:
                result_wordlist.append(word)

        space_list = ' '.join(result_wordlist)  # 空格链接词语

        wc = WordCloud(width=1400, height=2200,
                       background_color='white',
                       mask=plt.imread('backgroundpic.jpg'),
                       max_words=500,
                       font_path='C:\Windows\Fonts\STZHONGS.ttf',
                       max_font_size=150,
                       relative_scaling=0.6,  # 设置字体大小与词频的关联程度为0.4
                       random_state=50,
                       scale=2
                       ).generate(space_list)

        plt.imshow(wc)  # 显示词云
        plt.axis('off')  # 关闭x,y轴
        plt.show()  # 显示
        wc.to_file(self.FileDirectory + '/词云文件/' + text + ' 词云图.jpg')  # 保存词云图

    # --------------------------------开始下载按钮，生成词云图按钮误操作提醒------------------------------------------------
    def warning_info(self):
        QMessageBox.warning(self.ui, '未定义路径', f'''亲，先选择你要保存的目录哦~\n
不选择的话就不是好学生鸭☺''')


if __name__ == "__main__":
    sys.setrecursionlimit(1000000)
    app = QApplication([])
    # 加载 icon
    app.setWindowIcon(QIcon('./图标/音乐.png'))
    wyy = WangYiYun_Download()
    wyy.ui.show()
    app.exec_()
