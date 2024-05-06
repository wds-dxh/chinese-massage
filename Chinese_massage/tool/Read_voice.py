'''
Author: wds-dxh wdsnpshy@163.com
Date: 2024-04-11 17:24:58
LastEditors: wds-dxh wdsnpshy@163.com
LastEditTime: 2024-04-20 16:47:49
FilePath: /Chinese_massage/Chinese_massage/tool/Read_voice.py
Description:    读取音频文件
微信: 15310638214 
邮箱：wdsnpshy@163.com 
Copyright (c) 2024 by ${wds-dxh}, All Rights Reserved. 
'''
import pyaudio   #pyaudio录音模块
import wave      # wava模块是Python中处理WAV音频文件的模块
input_filename = ".wav"               # 麦克风采集的语音输入
input_filepath = "音频"              # 输入文件的path
in_path = input_filepath + input_filename
#pip install pyaudio -i https://pypi.tuna.tsinghua.edu.cn/simple

def get_audio(filepath):
    # aa = str(input("是否开始录音？   （是/否）"))
    # if 1:#aa == str("是") :
    CHUNK = 256                 # 块大小
    FORMAT = pyaudio.paInt16    # 每次采集的位数
    CHANNELS = 1                # 声道数
    RATE = 11025                # 采样率
    RECORD_SECONDS = 5          # 录音时间
    WAVE_OUTPUT_FILENAME = filepath
    p = pyaudio.PyAudio()           # 实例化pyaudio
    stream = p.open(format=FORMAT,      # 打开数据流
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)    # 每次读取的帧数
    print("*"*10, "开始录音：请在5秒内输入语音")
    frames = []
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):  # 控制录音时间
        data = stream.read(CHUNK)                        # 读取chunk个字节 保存到data中
        frames.append(data)                             # 添加到frames中 保存
    print("*"*10, "录音结束\n")
    stream.stop_stream()        # 停止数据流
    stream.close()              # 关闭数据流
    p.terminate()               # 关闭 PyAudio
    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')  # 打开刚才录制的语音文件
    wf.setnchannels(CHANNELS)                           # 配置声道数
    wf.setsampwidth(p.get_sample_size(FORMAT))          # 配置量化位数
    wf.setframerate(RATE)                               # 配置取样频率
    wf.writeframes(b''.join(frames))                    # 将数据写入文件
    wf.close()                                          # 关闭文件
    # elif aa == str("否"):                                    # 退出程序
    #     exit()
    # else:
    #     print("无效输入，请重新选择")
    #     get_audio(in_path)
    return 1


if __name__ == '__main__':
    get_audio(in_path)
