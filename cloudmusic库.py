# -*- coding = utf-8 -*-
# @Time：2020-10-28 22:16
# @Author：来瓶安慕嘻
# @File：cloudmusic库.py
# @开始美好的一天吧 @Q_Q@

import cloudmusic
import os

if not os.path.exists('./周深网易云歌曲'):
    os.mkdir("./周深网易云歌曲")

music_zs = cloudmusic.search("周深",40)
for music in music_zs:
    music.download("./周深网易云歌曲")



