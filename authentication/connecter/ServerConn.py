import socket
import threading
import struct
import pickle
from time import strftime, localtime


def get_localtime():
    return strftime("%Y-%m-%d %H:%M:%S", localtime())


class ServerConnect(threading.Thread):
    def __init__(self, address):
        super().__init__()
        self._server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._server.connect(address)
        # data为需要sql执行的语句
        self._notion_success = {
            'search': '符合查找条件的数据为：',
            'insert': '插入成功，插入的数据为：',
            'edit': '修改成功，修改后的数据为：',
            'delete': '删除成功，删除后的数据为：'
        }
        self._notion_fail = {
            'search': '未查找到符合条件的数据',
            'insert': '插入失败',
            'edit': '修改失败',
            'delete': '删除失败'
        }
        self.result = None
        self.count = 0

    def send_sql(self, sql_type, data):
        """
        向服务器发送sql请求，
        :param :
        :return:返回查询结果，查询失败则返回None
        """
        print(f"{get_localtime()}  SQL Request sending  starts...")
        try:
            data_str = pickle.dumps(data)
            self._server.send(struct.pack('i', len(data_str)))  # 发送数据包大小
            self._server.send(data_str)
            print('Waiting for response from server...')
            # 等待服务端响应
            pack_size = struct.unpack("i", self._server.recv(4))[0]
            pack_str = self._server.recv(pack_size)
            print(f'Received pack from server')
            pack = pickle.loads(pack_str)
            self.count = pack['count']
            self.result = pack['result']
            if self.count:
                print(f'{self._notion_success[sql_type]}{self.result}')
                return self.get_result()
            else:
                print(f'{self._notion_fail[sql_type]}')
                return None

        except Exception as e:
            print('sql error', e)

    def get_result(self):
        return self.result

    def get_count(self):
        return self.count
