import socket
import threading
import struct
import pickle

CHUNK = 1024
PAYLOAD_SIZE = struct.calcsize("L")
RESOURCE_SERVER_ADDRESS = ('0.0.0.0', 3979)

header_struct = struct.Struct('i1024s')
data_struct = struct.Struct('1024s')


class ResourceManager(threading.Thread):
    def __init__(self, addr):
        super().__init__()
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind(addr)
        self.server.listen(50)

    def fetch_and_store(self, conn):
        print('fetch file...')
        picked_header = self.server.recv(CHUNK)
        header_str = header_struct.unpack(picked_header)
        header = pickle.loads(header_str)
        user_id = header['user_id']
        file_size = header['file_size']
        with open(f'./resource/portrait/{user_id}.jpg', 'wb') as f:
            recv_size = 0
            while recv_size < file_size:
                data = self.server.recv(CHUNK)
                f.write(data)
                recv_size += len(data)
                print('recv_pre: ',recv_size/file_size)
        conn.close()
        print('fetch done')

    def run(self):
        print('ResourceManager starts...')
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