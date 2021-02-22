from time import strftime, localtime

from authentication.constantName import *
from authentication.connecter.ServerConn import ServerConnect


def get_localtime():
    return strftime("%Y-%m-%d %H:%M:%S", localtime())


class ConnectSQL():
    def __init__(self, server_address):
        self.cur = ServerConnect(server_address)
        self.property_name_userinfo = ['id', 'name', 'mail', 'password', 'anime', 'profile']
        self.property_name_friendinfo = ['id', 'friend']

    def insert(self, table_name, user_data):
        """
        向数据库插入数据，不允许留空
        :param : table_name '需要操作的表名'
        :param : user_data['name','mail','password']--userinfo
                 user_data['id', 'friend']--friendinfo
        :return: 插入失败则返回False
        """
        if table_name == TABLE_NAME_USERINFO:
            try:
                sql = f'select * from {table_name};'
                send_data = {'sql': sql, 'args': None}
                self.cur.send_sql('search', send_data)
                current_id = str(self.cur.get_count() + 1)
                print(current_id)
                # 将用户提交的昵称、邮箱地址、密码提交,用户的ID为当前表行数+1
                sql = f'insert into {table_name}(id,name, mail, password) values({current_id}, %s, %s, %s);'
                data = {'sql': sql, 'args': user_data}
                self.cur.send_sql('insert', data)
                print(f'提交成功，更新{self.cur.get_count()}条数据')
            except Exception as e:
                # 发生错误
                print(f"提交数据到{table_name}发生错误:{e}")
                return False

        if table_name == TABLE_NAME_FRIENDINFO:
            try:
                #
                sql = f'insert into {table_name}(id,friend) values(%s, %s);'
                data = {'sql': sql, 'args': user_data}
                self.cur.send_sql('insert', data)
                print(f'提交成功，更新{self.cur.get_count()}条数据')
            except Exception as e:
                # 发生错误
                print(f"提交数据到{table_name}发生错误:{e}")
                return False

    def search(self, table_name, data):
        """
        在数据库查询数据，输入表名以及一个数组包含 查询的属性 对应内容，返回该用户的所有数据
        :param table_name '需要操作的表名'
        :param data['属性名', '该属性需查找的内容'] data[1]如果为list的话，则为批量查询操作
        :return results:一个n维数组[n][id, name, mail, password] 未查到则返回 None,查询失败而返回False
                ans：一个列表[]，该id所有的好友id 未查到则返回 None,查询失败而返回False
        """
        property_name = [' ']
        if table_name == TABLE_NAME_USERINFO:
            property_name = self.property_name_userinfo
        if table_name == TABLE_NAME_FRIENDINFO:
            property_name = self.property_name_friendinfo
        for i in property_name:
            if i == data[0]:
                try:
                    if isinstance(data[1],list):
                        sql = f"select * from {table_name} where {data[0]} in %s;"
                        args = tuple(int(i) for i in data[1])
                        send_data = {'sql': sql, 'args': (args,)}
                    else:
                        sql = f'select * from {table_name} where {data[0]} = %s;'
                        send_data = {'sql': sql, 'args': data[1]}
                    self.cur.send_sql('search', send_data)
                    if self.cur.get_count():
                        result = self.cur.get_result()
                        print(f'查找成功,共查找到{self.cur.get_count()}条数据')
                        if table_name == TABLE_NAME_USERINFO:
                            return result
                        if table_name == TABLE_NAME_FRIENDINFO:
                            ans = []
                            for i in result:
                                ans.append(i[1])
                            return ans
                    else:
                        print(f'没有查找到{data[0]}为{data[1]}的用户')
                        return None
                except Exception as e:
                    # 发生错误
                    print(f'查询发生错误:{e}')
                    return False
        # 如果表中没有相应property 则说明用户使用函数错误
        print('使用search函数错误，search(table_name, data)data[0]应为数据表中的属性')
        return False

    def delete(self, table_name, data):
        """
        删除数据库中的指定数据,data数据留空则删除最后一条
        :param table_name '需要操作的表名'
        :param data['属性名', '该属性需删除的内容']--userinfo
               data[id， friend]--friendinfo
        :return results:删除的数量  发生错误则返回NFalse
        """
        if table_name == TABLE_NAME_USERINFO:
            try:
                sql = f'delete from {table_name} where {data[0]} = %s;'
                send_data = {'sql': sql, 'args': data[1]}
                self.cur.send_sql('delete', send_data)
                return self.cur.get_count()
            except Exception as e:
                # 发生错误
                print(f'删除发生错误:{e}')
                return False

        if table_name == TABLE_NAME_FRIENDINFO:
            try:
                sql = f'delete from {table_name} where id = %s and friend = %s;'
                send_data = {'sql': sql, 'args': data}
                self.cur.send_sql('delete', send_data)
                return self.cur.get_count()
            except Exception as e:
                # 发生错误
                print(f'删除发生错误:{e}')
                return False

    def edit(self, table_name, data):
        """
        在数据库更改数据，输入要更改的表名，以及需要进行修改操作的用户id，需要修改的属性及内容
        :param table_name '需要操作的表名'
        :param data['待修改用户id'， '属性名'， '该属性修改后的内容']
        :return 修改后该用户的数据  未查找到相关用户则返回None, 查询失败则返回False
        """

        if table_name == TABLE_NAME_FRIENDINFO:
            print('friendinfo 不需要edit操作')
            return False
        for i in self.property_name_userinfo:
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

                except Exception as e:
                    # 发生错误
                    print(f'修改发生错误:{e}')
                    return False
        # 如果表中没有相应property 则说明用户使用函数错误
        print('使用edit函数错误，edit(table_name, data)中 data[1]应为数据表中的属性')
        return False
