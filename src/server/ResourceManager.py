import os
import socket
import threading
import struct
import json
from time import strftime, localtime

CHUNK = 1024
PAYLOAD_SIZE = struct.calcsize("L")
RESOURCE_SERVER_ADDRESS = ('0.0.0.0', 3979)

def get_localtime():
    return strftime("%Y-%m-%d %H:%M:%S", localtime())


def send_package(conn, pack):
    pack_str = json.dumps(pack).encode()
    conn.send(struct.pack('i', len(pack_str)))
    conn.send(pack_str)


def fetch_package(conn):
    size = struct.unpack('i', conn.recv(4))[0]
    pack = json.loads(conn.recv(size).decode())
    return pack


class ResourceManager(threading.Thread):
    def __init__(self, addr):
        super().__init__()
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind(addr)
        self.server.listen(20)

    def fetch_resource(self, conn):
        header = fetch_package(conn)
        user_id = header['user_id']
        file_size = header['file_size']
        file_path = f'./resource/portrait/{user_id}.jpg'
        with open(file_path, 'wb') as f:
            recv_size = 0
            while recv_size < file_size:
                data = conn.recv(CHUNK)
                f.write(data)
                recv_size += len(data)

    def send_resource(self, conn, user_id):
        portrait_path = f'./resource/portrait/{user_id}.jpg'
        header = {
            'file_size': os.path.getsize(portrait_path) if os.path.exists(portrait_path) else 0
        }
        send_package(conn, header)
        with open(portrait_path, 'rb') as f:
            for line in f:
                conn.send(line)

    def handle_connect(self, conn):
        while True:
            try:
                query = fetch_package(conn)
                type_ = query['type']
                if type_ == 'fetch':
                    user_id = query['user_id']
                    self.send_resource(conn, user_id)
                else:
                    self.fetch_resource(conn)

            except Exception as e:
                print('handle Resource Connect error', e)
                break

    def run(self):
        print(f"{get_localtime()}  ResourceManager starts...")
        while True:
            try:
                conn, addr = self.server.accept()
                handler = threading.Thread(target=self.handle_connect, args=(conn,))
                handler.setDaemon(True)
                handler.start()
            except Exception as e:
                print('Resource Manager Error', e)
                break

if __name__ == '__main__':
    resourceManager = ResourceManager(RESOURCE_SERVER_ADDRESS)
    resourceManager.start()
    resourceManager.join()