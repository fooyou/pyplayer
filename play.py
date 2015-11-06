#!/usr/bin/env python
#! coding: utf8

import os
import sys
import random
import config
import signal
import json
import re

def play(path):
    basename = os.path.basename(path)
    cmd = 'ffplay -i ' + re.escape(path) + \
            ' -window_title ' + basename + \
            ' -autoexit -hide_banner'
    print('\n播放：', basename)
    os.system('ffplay ' + re.escape(path) + ' -autoexit -hide_banner')

song_list = []
play_list = []
music_folder = []
song_type = ['mp3', 'wav']

def gen_songlist(folders):
    # 遍历目录下的音乐文件
    for folder in folders:
        for root, dirs, files in os.walk(folder):
            for fl in files:
                for st in song_type:
                    if fl.endswith(st):
                        song_list.append(os.path.join(root, fl))
                        break

    # 建立播放列表
    if len(play_list) > 0 and music_folder == config.music_folder:
        for song in play_list:
            if not song in song_list:
                play_list.remove(song)
    else:
        for song in song_list:
            play_list.append(song)

def show():
    # 打印音乐列表
    print('序号\t\t歌名')
    for i, song in enumerate(song_list):
        print(i, song)

def interrupt(signum, frame):
    raise('Time out')

def timer_input(sec):
    signal.signal(signal.SIGALRM, interrupt)
    signal.alarm(sec)
    try:
        istr = input('\n输入序号播放，"ls"查看列表，"q"退出：')
    except:
        istr = None
    finally:
        signal.alarm(0)
    return istr

def save():
    data = {}
    data['music_folder'] = config.music_folder
    # data['song_list'] = song_list
    data['play_list'] = play_list
    content = json.dumps(data, ensure_ascii=False, indent=4)
    with open('.cache', 'w') as f:
        f.write(content)

def read():
    if os.path.isfile('.cache'):
        with open('.cache', 'r') as f:
            content = f.read()
        if len(content) > 0:
            data = json.loads(content)
            config = data['config']
            play_list = data['play_list']

def parse():
    istr = timer_input(5)
    if None == istr:
        if len(play_list) > 0:
            no = random.randint(0, len(play_list) - 1)
            play(play_list[no])
            play_list.remove(play_list[0])
    elif 'l' == istr or 'ls' == istr:
        show()
    elif 'q' == istr:
        save()
        exit(0)
    else:
        try:
            no = int(istr)
            if no < 0 or no >= len(song_list):
                no = random.randint(0, len(song_list) - 1)
        except ValueError as e:
            no = random.randint(0, len(song_list) - 1)

        play(song_list[no])
    parse()


def run():
    music_folder = config.music_folder
    gen_songlist(config.music_folder)
    show()
    parse()

if __name__ == '__main__':
    run()
