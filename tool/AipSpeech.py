'''
Author: wds-dxh wdsnpshy@163.com
Date: 2024-04-20 16:46:03
LastEditors: wds-dxh wdsnpshy@163.com
LastEditTime: 2024-06-19 10:06:36
FilePath: /chinese-massage/tool/AipSpeech.py
Description: 
微信: 15310638214 
邮箱：wdsnpshy@163.com 
Copyright (c) 2024 by ${wds-dxh}, All Rights Reserved. 
'''
import time
from threading import Thread
#添加路径
import sys
sys.path.append('..')

from aip import AipSpeech
from tool import Read_voice


""" 你的 APPID AK SK """
APP_ID = '84368232'
API_KEY = 'JbvSnXC3o8Ipv1pOLCRXKdzD'
SECRET_KEY = 'HgS9gIBN2qbMzh6hi8OfLjJMDhenYdQc'

client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)#创建一个客户端用以访问百度云
# 读取文件
def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()

def get_result():
    result  = client.asr(get_file_content('音频.wav'), 'pcm', 16000, {
        'dev_pid': 1537,
    })
    # print(result['result'][0])  #[0]的意思是只输出第一个结果，如果不加[0]，输出的结果是一个列表，列表中的元素是每个可能的结果
    return result['result'][0]

# global text
# text = ''
def thread_readvoice():
    global text
    while True:
        if Read_voice.get_audio('音频.wav') == 0:       ##录音,并保存为音频.wav
            continue
        text = get_result()
        if text == None:
            print("未识别到语音")
            text = ''
        return text
if __name__ == '__main__':
    while True:
        text = thread_readvoice()
        print(text)
        if text == '退出':
            break




