# 实现网易云音乐的可视化下载界面
利用爬虫实现网易云音乐的下载，并绘制词云图欣赏网易云热评，制作GUI交互界面

```
本文只是在技术层面上学习爬虫技术，为了保护版权，请勿随意爬取，保护我国的版权，人人有责。
不得用于商业用途！
```

本项目主要实现的功能为：
* 实现网易云音乐的爬取（包括VIP付费歌曲）
* 实现网易云热评的爬取分析，绘制词云图，实现可视化操作
* 利用GUI设计可视化操作界面
* 利用Threading多线程爬取歌曲
* 在PyQt与Python交互时，通过信号处理使得主界面显示内容与主代码程序分离

## 主要的工具
* Pycharm
* PySide2(designer)


## 文件说明
* branch中利用爬虫下载网易云音乐VIP歌曲markdown文件主要 介绍项目实现的具体步骤和思路
* cloudmusic库.py   主要对cloudmusic库作简要的代码示例
* 网易云1.2.py     实现歌曲的批量下载（包括VIP歌曲）
* 网易云2.0.py     利用PyQt2实现交互的爬取界面，可以输入想要下载的歌手并且一键下载，也可点击生成词云图
* wangyiyun.ui     利用PyQt2设计好以后，生成的UI文件

**项目已于2020-11-09更新完毕，有个小小的瑕疵就是在用Pyinstaller打包.exe文件时导包错误~**

**再次声明：不得用于商业用途，尊重版权**
