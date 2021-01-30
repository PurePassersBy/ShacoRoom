import socket
import threading
import struct
import json
import time
from time import strftime, localtime

import pymysql


def get_localtime():
    return strftime("%Y-%m-%d %H:%M:%S", localtime())



class Connect(threading.Thread):
    def __init__(self, address, data):
        super().__init__()
        self._server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._server.connect(address)
        # self._server.listen(5)
        # data为需要sql执行的语句
        self.data = data

    def _send_sql(self,data):
        print(f"{get_localtime()}  SQL Request sending thread starts...")
        while True:
            try:
                data_json = json.dumps(data)  # 把字典序列化
                data_str = data_json.encode()  # 转换成二进制比特流
                self._server.send(struct.pack('i', len(data_str)))  # 发送数据包大小
                self._server.send(data_str)
                print('Waiting for response from server...')
                # 等待服务端响应
                pack_size = struct.unpack("i", self._server.recv(4))[0]
                pack_str = self._server.recv(pack_size)
                print(f'Receive pack from server:{pack_str}')
                pack = json.loads(pack_str.decode())
                count = pack['count']
                result = pack['result']
                print(f'数据库相关行数：{count}\n修改结果:{result}')
                return
            except Exception as e:
                print('sql error', e)
                break

    def run(self):
        threading.Thread(target=self._send_sql, args=(self.data,)).start()


SERVER_ADDRESS = ('39.106.169.58', 3980)

if __name__ == '__main__':
    table = 'userinfo'
    column = 'id'
    sql = f'select * from {table} where {column} = %s;'
    args = ['4']
    data = {'sql': sql, 'args': args}
    conn = Connect(SERVER_ADDRESS, data)
    conn.start()
