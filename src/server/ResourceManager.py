import socket
import threading
import struct

import numpy as np
import cv2
import pymysql

CHUNK = 1024
PAYLOAD_SIZE = struct.calcsize("L")

class ResourceManager:

    def __init__(self, addr):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind(addr)
        self.server.listen(50)

    def fetch_and_store(self, conn, path, file_name):
        data = ''.encode()
        while len(data) < PAYLOAD_SIZE:
            data += self.server.recv(CHUNK)
        packed_size = data[:PAYLOAD_SIZE]
        data = data[PAYLOAD_SIZE:]
        msg_size = struct.unpack("L", packed_size)[0]
        while len(data) < packed_size:
            data += self.server.recv(CHUNK)
        nparr = np.array(bytearray(data[:msg_size]), np.uint8)
        img_decode = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        # TODO: 有效存储



class PortraitManager(threading.Thread, ResourceManager):

    def __init__(self, addr):
        super().__init__()

    def run(self):
        while True:
            conn, addr = self.server.accept()
