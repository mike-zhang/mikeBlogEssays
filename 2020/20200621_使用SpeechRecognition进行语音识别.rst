使用SpeechRecognition进行语音识别
===================================================

操作系统 ： CentOS7.7.1908_x64

gcc版本 ：4.8.5

Python 版本 : 3.6.8


安装语音识别环境：
::

    virtualenv -p /usr/bin/python3 py36asr
    source py36asr/bin/activate
    pip install SpeechRecognition
    yum install python3-devel
    yum install pulseaudio-libs-devel
    yum install alsa-lib-devel
    pip install  PocketSphinx

配置中文语音识别数据：

下载地址：

https://sourceforge.net/projects/cmusphinx/files/Acoustic%20and%20Language%20Models/

选择： Mandarin->cmusphinx-zh-cn-5.2.tar.gz

配置数据：
::

    cd py36asr/lib/python3.6/site-packages/speech_recognition/pocketsphinx-data/
    tar zxvf cmusphinx-zh-cn-5.2.tar.gz
    mv cmusphinx-zh-cn-5.2 zh-cn
    cd zh-cn
    mv zh_cn.cd_cont_5000 acoustic-model
    mv zh_cn.lm.bin language-model.lm.bin
    mv zh_cn.dic pronounciation-dictionary.dict


测试文本：

自然语言理解和生成是一个多方面问题，我们对它可能也只是部分理解。

语音识别示例：
::

    (py36asr) [root@host60 pyasrTest1]# ls
    test1.py  test1.wav
    (py36asr) [root@host60 pyasrTest1]# cat test1.py
    # -*- coding: utf-8 -*-
    # /usr/bin/python

    import speech_recognition as sr
    r = sr.Recognizer()
    test = sr.AudioFile("test1.wav")
    with test as source:
        audio = r.record(source)
    type(audio)
    c=r.recognize_sphinx(audio, language='zh-cn')
    print(c)
    (py36asr) [root@host60 pyasrTest1]# python test1.py
    自然 语言 李杰 和 申城 是一 个 多方 面 问题 我们 对 他 可能 也 只是 部分 礼节
    (py36asr) [root@host60 pyasrTest1]#


.. image:: images/20200621.1.1.png

本文涉及资源下载地址：https://pan.baidu.com/s/1Out0tJlb_Qs-2C06_2YHOQ 

可关注微信公众号（聊聊博文）后回复 2020062101 获取提取码




