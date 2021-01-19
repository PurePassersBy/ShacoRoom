import socket
import threading
from time import sleep

from VideoChatter import VideoChatter
from AudioChatter import AudioChatter

#SERVER_ADDRESS = ('192.168.43.113', 3976)
#VIDEO_SERVER_ADDRESS = ('192.168.43.113', 3977)
SERVER_ADDRESS = ('39.97.190.111', 3976)
VIDEO_SERVER_ADDRESS = ('39.97.190.111', 3977)
AUDIO_SERVER_ADDRESS = ('39.97.190.111', 3978)

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
class Sender(threading.Thread):
    def __init__(self, sender):
        super().__init__()
        self._sender = sender
    def run(self):
        while True:
            try:
                msg = input().encode('utf-8')
                self._sender.send(msg)
            except Exception as e:
                print(e)
                break
class Chatter():
    def __init__(self, addr, name, buffer_size=1024):
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
        sender = Sender(self._client)
        sender.setDaemon(True)
        receiver.start()
        sender.start()

if __name__ == '__main__':
    # chatter = Chatter((sys.argv[1], int(sys.argv[2])), sys.argv[3])
    username = input('Plz enter your username:')
    chatter = Chatter(SERVER_ADDRESS, username)
    chatter.run()


