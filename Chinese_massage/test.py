from tool import AipSpeech

if __name__ == '__main__':
    while True:
        text = AipSpeech.thread_readvoice()
        print(text)
        if text == '退出':
            break

