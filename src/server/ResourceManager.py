import socket
import threading
import struct

import numpy as np
import cv2
import pymysql

CHUNK = 1024
PAYLOAD_SIZE = struct.calcsize("L")
RESOURCE_SERVER_ADDRESS = ('0.0.0.0', 3979)


class ResourceManager(threading.Thread):
    def __init__(self, addr):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind(addr)
        self.server.listen(50)

    def fetch_and_store(self, conn):
        user_id = conn.recv(CHUNK).decode()
        data = ''.encode()
        while len(data) < PAYLOAD_SIZE:
            data += conn.recv(CHUNK)
        file_size = struct.unpack("L", data[:PAYLOAD_SIZE])[0]
        data = data[PAYLOAD_SIZE:]
        while len(data) < file_size:
            data += conn.recv(CHUNK)
        with open(f'./resource/portrait/{user_id}.jpg', 'wb') as f:
            f.write(data)
        conn.close()

        def run(self):
            while True:
                try:
                    conn, addr = self.server.accept()
                    threading.Thread(target=self.fetch_and_store, args=(conn,)).start()
                except:
                    print('Resource Error')
                    break

if __name__ == '__main__':
    resourceManager = ResourceManager(RESOURCE_SERVER_ADDRESS)
    resourceManager.start()
    resourceManager.join()