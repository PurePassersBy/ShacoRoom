import socket
import threading
from time import sleep

from .VideoChatter import VideoChatter
from .AudioChatter import AudioChatter

SERVER_ADDRESS = ('39.106.169.58', 3976)
VIDEO_SERVER_ADDRESS = ('39.106.169.58', 3977)
AUDIO_SERVER_ADDRESS = ('39.106.169.58', 3978)


class Receiver(threading.Thread):
    def __init__(self, receiver):
        super().__init__()
        self._receiver = receiver
    def run(self):
        while True:
            try:
                data = self._receiver.recv(1024).decode('utf-8')
                if data == '#Exit Permission':
                    sleep(0.5)
                    self._receiver.close()
                    print("You have exited safely...")
                    break
                if data == '#VideoChat Permission':
                    videoChatter = VideoChatter(VIDEO_SERVER_ADDRESS)
                    videoChatter.start()
                    audioChatter = AudioChatter(AUDIO_SERVER_ADDRESS)
                    audioChatter.start()

                print(data)
            except Exception as e:
                print(e)
                break


class Chatter():
    def __init__(self, name, addr=SERVER_ADDRESS, buffer_size=1024):
        super().__init__()
        self._addr = addr
        self._name = name
        self._buffer_size = buffer_size
        self._client = None

    def run(self):
        self._client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._client.connect(self._addr)
        self._client.send(self._name.encode('utf-8'))
        receiver = Receiver(self._client)
        receiver.start()

    def send(self, msg):
        self._client.send(msg.encode('utf-8'))

if __name__ == '__main__':
    # chatter = Chatter((sys.argv[1], int(sys.argv[2])), sys.argv[3])
    username = input('Plz enter your username:')
    chatter = Chatter(username)
    chatter.run()


