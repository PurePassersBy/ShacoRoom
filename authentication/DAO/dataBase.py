import socket
import threading
import struct
import json
from time import strftime, localtime


def get_localtime():
    return strftime("%Y-%m-%d %H:%M:%S", localtime())


# data base serve ('39.106.169.58', 3980)

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
            data_json = json.dumps(data)  # 把字典序列化
            data_str = data_json.encode()  # 转换成二进制比特流
            self._server.send(struct.pack('i', len(data_str)))  # 发送数据包大小
            self._server.send(data_str)
            print('Waiting for response from server...')
            # 等待服务端响应
            pack_size = struct.unpack("i", self._server.recv(4))[0]
            pack_str = self._server.recv(pack_size)
            print(f'Received pack from server')
            pack = json.loads(pack_str.decode())
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


class ConnectSQL():
    def __init__(self, server_address):
        self.cur = ServerConnect(server_address)
        self.property_name = ['id', 'name', 'mail', 'password', 'online']

    def insert(self, table_name, user_data):
        """
        向数据库插入数据，不允许留空
        :param : table_name '需要操作的表名'
        :param : user_data['name','mail','password']
        :return:
        """
        try:
            sql = f'select * from {table_name};'
            send_data = {'sql': sql, 'args': None}
            self.cur.send_sql('search', send_data)
            current_id = str(self.cur.get_count()+1)
            print(current_id)
            # 将用户提交的昵称、邮箱地址、密码提交,用户的ID为当前表行数+1
            sql = f'insert into {table_name}(id,name, mail, password) values({current_id}, %s, %s, %s);'
            data = {'sql': sql, 'args': user_data}
            self.cur.send_sql('insert', data)
            print(f'提交成功，更新{self.cur.get_count()}条数据')
        except Exception:
            # 发生错误
            print("提交新用户数据发生错误")

    def search(self, table_name, data):
        """
        在数据库查询数据，输入表名以及一个数组包含 查询的属性 对应内容，返回该用户的所有数据
        :param table_name '需要操作的表名'
        :param data['属性名', '该属性需查找的内容']
        :return results:一个n维数组[n][id, name, mail, password] 未查到则返回 None
        """
        for i in self.property_name:
            if i == data[0]:
                try:
                    sql = f'select * from {table_name} where {data[0]} = %s;'
                    send_data = {'sql': sql, 'args': data[1]}
                    self.cur.send_sql('search', send_data)
                    if self.cur.get_count():
                        result = self.cur.get_result()
                        print(f'查找成功,共查找到{self.cur.get_count()}条数据')
                        return result
                    else:
                        print(f'没有查找到{data[0]}为{data[1]}的用户')
                        return None
                except Exception:
                    # 发生错误
                    print('查询发生错误')
                    return None
        # 如果表中没有相应property 则说明用户使用函数错误
        print('使用search函数错误，search(table_name, data)data[0]应为数据表中的属性')
        return None

    def delete(self, table_name, data):
        """
        删除数据库中的指定数据,data数据留空则删除最后一条
        :param table_name '需要操作的表名'
        :param data['属性名', '该属性需删除的内容']
        :return results:删除的数量  发生错误则返回None
        """
        try:
            # if data:
            #     # 无参时，删除数据库中的最后一条
            #     sql = f'delete from {table_name} where id like (select top 1 id from {table_name} order by id desc)'
            #     send_data = {'sql': sql, 'args': None}
            #     self.cur.send_sql('delete', send_data)
            #     return self.cur.get_count()

            # 删除数据库中指定内容
            sql = f'delete from {table_name} where {data[0]} = %s;'
            send_data = {'sql': sql, 'args': data[1]}
            self.cur.send_sql('delete', send_data)
            return self.cur.get_count()
        except Exception:
            # 发生错误
            print('删除发生错误')
            return None

    def edit(self, table_name, data):
        """
        在数据库更改数据，输入要更改的表名，以及需要进行修改操作的用户id，需要修改的属性及内容
        :param table_name '需要操作的表名'
        :param data['待修改用户id'， '属性名'， '该属性修改后的内容']
        :return 修改后该用户的数据  出错则返回None
        """
        for i in self.property_name:
            if i == data[1]:
                try:
                    if self.search(table_name, ['id', data[0]]) is None:
                        print(f'未查找到到id为{data[0]}的用户')
                        return None
                    else:
                        sql = f'update {table_name} set {data[1]} = %s where id = %s;'
                        send_data = {'sql': sql, 'args': [data[2], data[0]]}
                        print('?')
                        self.cur.send_sql('edit', send_data)

                        print(f'修改{self.cur.get_count()}条数据')
                        return self.cur.get_result()

                except Exception:
                    # 发生错误
                    print('修改发生错误')
                    return None
        # 如果表中没有相应property 则说明用户使用函数错误
        print('使用edit函数错误，edit(table_name, data)中 data[1]应为数据表中的属性')
        return None
