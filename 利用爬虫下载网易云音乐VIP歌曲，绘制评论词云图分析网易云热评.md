学习爬虫也有段时间了，趁着最近稍微有点闲，爬取一下网易云音乐的歌曲，边听歌边coding是不是很舒服！


 - 爬取网易云歌曲
 - 绘制词云图，分析网易云热评
 - 利用GUI设计可视化操作界面

> 本文只是在技术层面上学习爬虫技术，为了保护版权，请勿随意爬取，**保护我国的版权**，人人有责。
> **不得用于商业用途**！

以下全是个人摸索得来，如果有不对的地方，还请指正！
## 1.cloudmusic库
**首先**要给大家介绍一个强大的API接口，也是一个强大的第三方库，`cloudmusic`，该库主要针对的就是网易云音乐信息的获取，其GitHub地址为：
[cloudmusic用法说明](https://github.com/p697/cloudmusic)：https://github.com/p697/cloudmusic

### 1.1安装
`pip install cloudmusic`

### 1.2 对象属性
* url：歌曲音频文件链接
* id：歌曲id
* name：歌曲名称
* artist：歌手名称
* artistId: 歌手id
* album：专辑名称
* albumId: 专辑id
* size：音频文件大小
* type：音频文件类型（mp3或m4a）
* level：歌曲品质。默认higher
* picUrl: 专辑图url
###  1.3 对象方法
* `download(dirs, level)`  下载歌曲，返回值为下载绝对路径

> dirs：可选。下载保存路径。默认为当前文件夹内创建的新的cloudmusic文件夹。 level：可选，字符型。默认higher。下载品质，有且只有四种选择：standard，higher，exhigh，lossless。

* `getHotComments(number)`  获取热评

>number：可选，整型，默认为15。希望获取的评论个数。上限为15个。

* `getComments(number)`  获取最新的评论

> number：整型，评论个数。数量无限制。

* `getLyrics()`  获取歌词

### 1.4 对象函数
* `getMusic(id/id_list)`  通过歌曲id或一个由id组成的列表生成music对象

> id/id_list: 必须，整型、字符型或列表。歌曲id或由歌曲id组成的列表。

* `getPlaylist(id)` 通过歌单id生成music对象
> id：必须，整型或字符型。歌单id。

* `search(content, number)` 通过关键词搜索获取music对象

> content：必须，字符型。搜索关键字。 number：可选，整形，搜索结果个数，默认为5。

* `getAlbum(id)` 

> id: 必须，整型或字符型。专辑id。

以**周深**为例，，简单说明`cloudmusic`的用法

![在这里插入图片描述](https://img-blog.csdnimg.cn/20201029100840218.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3N0ZXBoZW5fY3VycnkzMDA=,size_16,color_FFFFFF,t_70#pic_center)
```python
# -*- coding = utf-8 -*-
# @Time：2020-10-28 22:16
# @Author：一只安慕嘻
# @File：cloudmusic库.py
# @开始美好的一天吧 @Q_Q@

import cloudmusic

music = cloudmusic.getMusic(1434062381)  # 获取达拉崩吧的id 1434062381

print("歌名为：",music.name)  # 歌名为： 达拉崩吧 (Live)
print("歌手为：",music.artist[0])  # 歌手为： 周深
```

搜索周深的所有歌曲

```python
import cloudmusic

music_result = cloudmusic.search("周深",20) # 搜索关键词为周深，展示前20条结果

for music in music_result:
    print("歌名为:%s,歌曲id为:%s"%(music.name,music.id))
    
'''
歌名为:大鱼 动画电影《大鱼海棠》印象曲,歌曲id为:413812448
歌名为:Monsters (Live),歌曲id为:1428598981
歌名为:化身孤岛的鲸,歌曲id为:1465313631
歌名为:达拉崩吧 (Live),歌曲id为:1434062381
歌名为:愿得一心人 《鹤唳华亭》主题曲,歌曲id为:1401790402
歌名为:请笃信一个梦 电影《姜子牙》片尾曲,歌曲id为:1416619074
歌名为:起风了 BILIBILI 11周年演讲,歌曲id为:1475596788
歌名为:亲爱的旅人啊（翻自 木村弓） ,歌曲id为:1371939273
歌名为:漂洋过海来看你,歌曲id为:30903117
歌名为:大鱼 (唱片版),歌曲id为:516823132
歌名为:爱若琉璃 电视剧《琉璃》主题曲,歌曲id为:1436150979
歌名为:有可能的夜晚 (Live),歌曲id为:1432427879
歌名为:相思 (Live),歌曲id为:1436912291
歌名为:千千阙歌 (Live),歌曲id为:1446233390
歌名为:蓝色降落伞,歌曲id为:514765774
歌名为:自己按门铃自己听 (Live),歌曲id为:1439111144
歌名为:雪花落下 电视剧《冰糖炖雪梨》主题曲,歌曲id为:1429392929
歌名为:听我说 五福贺岁短片《到哪儿了》主题曲,歌曲id为:1415078941
歌名为:真夏的樱花 (Live),歌曲id为:1489294867
歌名为:大鱼 (Live),歌曲id为:1421191783
'''
```

![在这里插入图片描述](https://img-blog.csdnimg.cn/20201029101348346.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3N0ZXBoZW5fY3VycnkzMDA=,size_16,color_FFFFFF,t_70#pic_center)
### 1.5 下载VIP歌曲

>  重点开始，下载VIP歌曲！！！

以王贰浪的往后余生为例！
![在这里插入图片描述](https://img-blog.csdnimg.cn/20201029101936108.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3N0ZXBoZW5fY3VycnkzMDA=,size_16,color_FFFFFF,t_70#pic_center)
其实很简单，只要利用`cloudmusic`中的`download`方法即可！

```python
import cloudmusic

music = cloudmusic.getMusic(571338279) # 往后余生的ID
music.download()
```

![在这里插入图片描述](https://img-blog.csdnimg.cn/20201029102226543.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3N0ZXBoZW5fY3VycnkzMDA=,size_16,color_FFFFFF,t_70#pic_center)
**批量爬取的方法同理可得：**

```python
import cloudmusic
import os

if not os.path.exists('./周深网易云歌曲'):
    os.mkdir("./周深网易云歌曲")

music_zs = cloudmusic.search("周深",40)
for music in music_zs:
    music.download("./周深网易云歌曲")
```
![在这里插入图片描述](https://img-blog.csdnimg.cn/20201029102850739.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3N0ZXBoZW5fY3VycnkzMDA=,size_16,color_FFFFFF,t_70#pic_center)
## 2. 利用python自己爬取
作为程序员，如果自己能实现底层代码，那当然是再舒服不过了。所以下面我们不利用第三方库自己手撕爬虫代码，实现**敏感词汇**的批量下载！
![在这里插入图片描述](https://img-blog.csdnimg.cn/20201029201002168.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3N0ZXBoZW5fY3VycnkzMDA=,size_16,color_FFFFFF,t_70#pic_center)
ok，下面我将一步步分析如何实现网易云歌曲下载，教你找到接口在哪！看了很多博客和教学视频，都是直接给你外链链接，不告诉你怎么来的！（我会写明，略略略~）

### 2.1 寻找下载歌曲的url区别
![在这里插入图片描述](https://img-blog.csdnimg.cn/20201029201406207.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3N0ZXBoZW5fY3VycnkzMDA=,size_16,color_FFFFFF,t_70#pic_center)
![在这里插入图片描述](https://img-blog.csdnimg.cn/2020102920143129.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3N0ZXBoZW5fY3VycnkzMDA=,size_16,color_FFFFFF,t_70#pic_center)
[化身孤岛的鲸的url](https://music.163.com/#/song?id=1465313631)：https://music.163.com/#/song?id=1465313631
[相思(live)的url](https://music.163.com/#/song?id=1436912291)：https://music.163.com/#/song?id=1436912291

> *可以看到两个url唯一不同的区别在于两首歌曲的`url`不同，因此我们是不是只要找到每个歌手所有歌曲的`url`就能爬到对应的歌曲（答案：是的）

下面我们去提取所有的歌曲的id:

 1. 右击检查（或F12）打开开发者工具，利用元素定位，找到歌曲的id
 ![在这里插入图片描述](https://img-blog.csdnimg.cn/2020102920200798.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3N0ZXBoZW5fY3VycnkzMDA=,size_16,color_FFFFFF,t_70#pic_center)

![在这里插入图片描述](https://img-blog.csdnimg.cn/20201029201945110.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3N0ZXBoZW5fY3VycnkzMDA=,size_16,color_FFFFFF,t_70#pic_center)

> 可以看到所有的歌曲id都在a标签下href对应的属性下！因此我们只需要通过网页解析，利用`xpath`定位即可！

```python
# 获取歌曲id
music_list = tree1.xpath('//a[contains(@href,"/song?")]/@href')
```
但是提取到的数据含有干扰项（噪声），因此需要清洗！

```python
for music in music_list:
    music_id_first= music.split('=')[1]
    # print(music_id_first)
    # 清洗所有的ID
    if "$" not in music_id_first:
        music_id = music_id_first
        music_name = tree1.xpath('//a[contains(@href,"/song?id='+music_id+
                                 '")]/text()')[0]  # 歌曲对应名称

```
### 2.2 寻找歌曲的外链下载地址
* 如何找到下载的接口，这是最关键的步骤，也是很多教学含糊不清的地方！
 * [x] 第一种方法
打开开发者工具，点击播放任意一首歌曲，在network抓包工具中找到`audio`类型


![在这里插入图片描述](https://img-blog.csdnimg.cn/20201029202855618.png#pic_center)
![在这里插入图片描述](https://img-blog.csdnimg.cn/20201029203028673.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3N0ZXBoZW5fY3VycnkzMDA=,size_16,color_FFFFFF,t_70#pic_center)
打开对应的url:
[https://m701.music.126.net/20201029205248/84e60a6b73215a47c1aa1916a9bcdb96/jdyyaac/550f/035a/0008/be2fc579744073f1a3597b5b0ea18935.m4a](https://m701.music.126.net/20201029205248/84e60a6b73215a47c1aa1916a9bcdb96/jdyyaac/550f/035a/0008/be2fc579744073f1a3597b5b0ea18935.m4a)
可以看到是下载接口，大功告成！
![在这里插入图片描述](https://img-blog.csdnimg.cn/20201029203212497.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3N0ZXBoZW5fY3VycnkzMDA=,size_16,color_FFFFFF,t_70#pic_center)
但是别高兴的太早，每一首歌的下载地址毫无规律可循，特别是m4a前面的`be2fc579744073f1a3597b5b0ea1893`是32位的信息摘要，极有可能经过`md5`加密。显然这种方法不利于我们批量下载歌曲，但是如果不嫌麻烦，一首一首找url那确实是勇士~

 - [x] 第二种方法
那如何找到下载接口是不是没有办法了，显示是有的！

* 提供一个宝藏**外链工具**，可以下载QQ音乐，网易云音乐，虾米音乐的付费歌曲（悄悄的不要告诉别人~）

网址双手奉上：[https://link.hhtjim.com/](https://link.hhtjim.com/)
![在这里插入图片描述](https://img-blog.csdnimg.cn/20201029203819474.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3N0ZXBoZW5fY3VycnkzMDA=,size_16,color_FFFFFF,t_70#pic_center)
使用方法：点击网易云音乐，输入歌曲ID，点击提交，就可以找到下载接口！
打开下面的链接，如图：
![在这里插入图片描述](https://img-blog.csdnimg.cn/20201029203951203.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3N0ZXBoZW5fY3VycnkzMDA=,size_16,color_FFFFFF,t_70#pic_center)

> 因此只需要将每一个ID拼接到`https://link.hhtjim.com/163/歌曲id.mp3`中是不是就可以拿到歌曲了，所以利用我们刚刚提取到的`id`就可以下载歌曲啦~

 - [x] 第三种方法
以前的网易博客中使用的歌曲开源于网易云音乐，虽然现在的网易博客关闭，但是外链链接仍然可以使用，

同样链接奉上：`https://music.163.com/song/media/outer/url?id=歌曲ID`

例如周深的大鱼：`https://music.163.com/song/media/outer/url?id=413812448`会得到同样的界面。
![在这里插入图片描述](https://img-blog.csdnimg.cn/20201029204548200.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3N0ZXBoZW5fY3VycnkzMDA=,size_16,color_FFFFFF,t_70#pic_center)
### 2.3 手撕代码

```python
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
    if not os.path.exists('./林俊杰'):
        os.mkdir('./林俊杰')

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

            with open('./林俊杰/'+music_name+'.mp3','wb')as fp:
                music_text = requests.get(url=base_url,headers=headers,proxies=proxy).content
                fp.write(music_text)
                print('%s下载完成'%music_name)
        time.sleep(1)
```

> 例如林俊杰的歌曲如下。刚开始偷懒，没有加载歌曲名字，但是代码中我都帮你写好了~

![在这里插入图片描述](https://img-blog.csdnimg.cn/20201029204740514.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3N0ZXBoZW5fY3VycnkzMDA=,size_16,color_FFFFFF,t_70#pic_center)
## 3. 绘制词云图，欣赏网易云热评

