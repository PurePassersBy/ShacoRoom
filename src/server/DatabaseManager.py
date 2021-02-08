import socket
import threading
import struct
import pickle
from time import strftime, localtime

import pymysql

cur_lock = threading.Lock()


def get_localtime():
    return strftime("%Y-%m-%d %H:%M:%S", localtime())


class DatabaseManager(threading.Thread):
    def __init__(self, addr):
        super().__init__()
        self._server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._server.bind(addr)
        self._server.listen(50)

        self.db_conn = pymysql.connect(host='localhost', port=3306, user='Shaco', password='Badwoman',
                                       db='ShacoRoomDB')
        self.cur = self.db_conn.cursor()

    def do_sql(self, conn):
        print(f'{get_localtime()}: 一个新的连接')
        while True:
            try:
                pack_size = struct.unpack("i", conn.recv(4))[0]
                print(f'pack size: {pack_size}')
                pack_str = conn.recv(pack_size)
                pack = pickle.loads(pack_str)
                sql = pack['sql']
                args = pack['args']
                print(pack)
                with cur_lock:
                    cnt = self.cur.execute(sql, args)
                    res = self.cur.fetchall()
                    self.db_conn.commit()
                send_pack = {
                    'count': cnt,
                    'result': res
                }
                send_pack_str = pickle.dumps(send_pack)
                conn.send(struct.pack('i', len(send_pack_str)))
                conn.send(send_pack_str)
            except Exception as e:
                print('sql error', e)
                break

    def run(self):
        print(f"{get_localtime()}  DatabaseManager starts...")
        while True:
            conn, addr = self._server.accept()
            threading.Thread(target=self.do_sql, args=(conn,)).start()