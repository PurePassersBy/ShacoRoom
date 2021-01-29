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


class ResourceManager(threading.Thread):
    def __init__(self, addr):
        super().__init__()
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind(addr)
        self.server.listen(20)

    def fetch_and_store(self, conn):
        print('fetch file...')
        header_size = struct.unpack('i', conn.recv(4))[0]
        header_str = conn.recv(header_size)
        header = json.loads(header_str.decode())
        user_id = header['user_id']
        file_size = header['file_size']
        file_path = f'./resource/portrait/{user_id}.jpg'
        with open(file_path, 'wb') as f:
            recv_size = 0
            while recv_size < file_size:
                data = conn.recv(CHUNK)
                f.write(data)
                recv_size += len(data)
        conn.close()
        print('fetch done')

    def run(self):
        print(f"{get_localtime()}  ResourceManager starts...")
        while True:
            try:
                conn, addr = self.server.accept()
                print('ResourceManager accept one...')
                threading.Thread(target=self.fetch_and_store, args=(conn,)).start()
            except:
                print('Resource Error')
                break

if __name__ == '__main__':
    resourceManager = ResourceManager(RESOURCE_SERVER_ADDRESS)
    resourceManager.start()
    resourceManager.join()