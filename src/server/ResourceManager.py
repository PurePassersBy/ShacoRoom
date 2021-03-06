import os
import socket
import threading
import struct
import pickle
from time import strftime, localtime

CHUNK = 1024
PAYLOAD_SIZE = struct.calcsize("L")
RESOURCE_SERVER_ADDRESS = ('0.0.0.0', 3979)
lock = threading.Lock()


def get_localtime():
    return strftime("%Y-%m-%d %H:%M:%S", localtime())


def send_package(conn, pack):
    pack_str = pickle.dumps(pack)
    conn.send(struct.pack('i', len(pack_str)))
    conn.send(pack_str)


def fetch_package(conn):
    size = struct.unpack('i', conn.recv(4))[0]
    pack = pickle.loads(conn.recv(size))
    return pack


def fetch_resource(conn, header):
    user_id = header['user_id']
    file_size = header['file_size']
    file_path = f'./resource/portrait/{user_id}.jpg'
    print(f'接收{user_id}的头像，大小为{file_size}')
    lock.acquire()
    with open(file_path, 'wb') as f:
        recv_size = 0
        while recv_size < file_size:
            if recv_size + CHUNK > file_size:
                data = conn.recv(file_size - recv_size)
            else:
                data = conn.recv(CHUNK)
            f.write(data)
            recv_size += len(data)
    lock.release()
    print('接收头像成功')


def send_resource(conn, user_id):
    portrait_path = f'./resource/portrait/{user_id}.jpg'
    exists = os.path.exists(portrait_path)
    header = {
        'file_size': os.path.getsize(portrait_path) if exists else 0
    }
    print(f'要发送的文件大小{header["file_size"]}')
    send_package(conn, header)
    if not exists:
        return
    lock.acquire()
    with open(portrait_path, 'rb') as f:
        for line in f:
            conn.send(line)
    lock.release()


class ResourceManager(threading.Thread):
    def __init__(self, addr):
        super().__init__()
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind(addr)
        self.server.listen(20)


    def handle_connect(self, conn):
        while True:
            try:
                query = fetch_package(conn)
                print(query)
                type_ = query['type']
                if type_ == 'fetch':
                    user_id = query['user_id']
                    print(f'向用户发送{user_id}的头像')
                    send_resource(conn, user_id)
                    print('发送成功')
                else:
                    fetch_resource(conn, query)

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