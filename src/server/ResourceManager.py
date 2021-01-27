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
        pass
        # TODO: 有效存储