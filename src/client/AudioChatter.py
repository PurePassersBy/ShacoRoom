import threading
import socket
import struct
import pickle
import time
import sys
import zlib

import pyaudio

CHUNK = 8192
FORMAT = pyaudio.paInt16    # 格式
CHANNELS = 2    # 输入/输出通道数
RATE = 22050    # 音频数据的采样频率
RECORD_SECONDS = 0.5    # 记录秒


class AudioChatter(threading.Thread):
    def __init__(self, addr):
        super().__init__()
        self._addr = addr
        self._client = None
    def run(self):
        self._client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._client.connect(self._addr)
        receiver = AudioReceiver(self._client)
        sender = AudioSender(self._client)
        receiver.start()
        sender.start()

class AudioSender(threading.Thread):
    def __init__(self, conn):
        super().__init__()
        self.socket = conn
        self.stream = None
        self.p = pyaudio.PyAudio()

    def __del__(self):
        self.socket.close()   # 关闭套接字
        if self.stream is not None:
            self.stream.stop_stream()   # 暂停播放 / 录制
            self.stream.close()     # 终止流
        self.p.terminate()      # 终止会话

    def run(self):
        print("AUDIO client connected...")
        self.stream = self.p.open(format=FORMAT,
                             channels=CHANNELS,
                             rate=RATE,
                             input=True,
                             frames_per_buffer=1024)
        while self.stream.is_active():
            last = time.time()
            frames = []
            #print(int(RATE / CHUNK * RECORD_SECONDS))
            for i in range(5):
                data = self.stream.read(1024)
                frames.append(data)
            senddata = pickle.dumps(frames)
            zdata = zlib.compress(senddata)
            #print(sys.getsizeof(senddata), sys.getsizeof(zdata))
            #print('音频处理',time.time() - last)
            last = time.time()
            try:
                self.socket.sendall(struct.pack("L", len(zdata)) + zdata)
            except:
                break
            #print('音频发送', time.time() - last)
            time.sleep(0.05)


class AudioReceiver(threading.Thread):
    def __init__(self, conn):
        super().__init__()
        self.socket = conn
        self.stream = None
        self.p = pyaudio.PyAudio()

    def __del__(self):
        self.socket.close()   # 关闭套接字
        if self.stream is not None:
            self.stream.stop_stream()   # 暂停播放 / 录制
            self.stream.close()     # 终止流
        self.p.terminate()      # 终止会话

    def run(self):
        data = "".encode('utf-8')
        payload_size = struct.calcsize("L")
        self.stream = self.p.open(format=FORMAT,
                                  channels=CHANNELS,
                                  rate=RATE,
                                  output=True,
                                  frames_per_buffer=1024
                                  )
        while True:
            while len(data) < payload_size:
                data += self.socket.recv(CHUNK)
            packed_size = data[:payload_size]
            data = data[payload_size:]
            msg_size = struct.unpack("L", packed_size)[0]
            while len(data) < msg_size:
                data += self.socket.recv(CHUNK)
            frame_data = data[:msg_size]
            data = data[msg_size:]
            frames = pickle.loads(zlib.decompress(frame_data))
            for frame in frames:
                self.stream.write(frame, 1024)