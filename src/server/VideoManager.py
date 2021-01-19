import threading
import socket
from time import strftime,localtime,time
import sys

CHUNK = 8192


def get_localtime():
    return strftime("%Y-%m-%d %H:%M:%S", localtime())


class VideoManager(threading.Thread):
    def __init__(self, address=('0.0.0.0',3977), max_connections = 20):
        super().__init__()
        self._addr = address
        self._max_connections = max_connections
        self._server = None
        self._init_server()

    def _init_server(self):
        self._server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._server.bind(self._addr)
        self._server.listen(self._max_connections)

    def run(self):
        print(f"{get_localtime()}  VideoManager starts...")
        while True:
            conn1, addr1 = self._server.accept()
            conn2, addr2 = self._server.accept()
            videoThread1 = VideoThread(conn1, conn2)
            videoThread2 = VideoThread(conn2, conn1)
            videoThread1.start()
            videoThread2.start()


class VideoThread(threading.Thread):
    def __init__(self, sender, receiver):
        super().__init__()
        self.sender = sender
        self.receiver = receiver
    def run(self):
        while True:
            try:
                last = time()
                data = self.receiver.recv(CHUNK)
                print(self.sender,self.receiver,time() - last)
                print(sys.getsizeof(data))
                self.sender.send(data)
            except Exception as e:
                print('VideoThread:', e)
                break


class VideoConnection(threading.Thread):
    def __init__(self, c1, c2):
        super().__init__()
        self.c1 = c1
        self.c2 = c2

    def run(self):
        while True:
            try:
                self.c2.send(self.c1.recv(CHUNK))
                self.c1.send(self.c2.recv(CHUNK))
            except:
                break
