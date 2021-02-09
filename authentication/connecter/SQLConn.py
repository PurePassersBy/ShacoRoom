from time import strftime, localtime

from authentication.connecter.ServerConn import ServerConnect


def get_localtime():
    return strftime("%Y-%m-%d %H:%M:%S", localtime())


class ConnectSQL():
    def __init__(self, server_address):
        self.cur = ServerConnect(server_address)
        self.property_name = ['id', 'name', 'mail', 'password', 'anime', 'biography']

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
            current_id = str(self.cur.get_count() + 1)
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
        :param data: {'id':待修改用户的id, 'name':修改后的名字， 'mail'= 修改后的邮件, ’password' = 修改后的密码，
                            'anime' = , 'biography'= }
        :return 修改后该用户的数据  出错则返回None
        """
        flag = False
        if 'id' in data:
            if self.search(table_name, ['id', data['id']]) is None:
                print(f'未查找到到id为{data["id"]}的用户')
                return None
            for i in data:
                if i not in self.property_name:
                    # 如果表中没有相应property 则说明用户使用函数错误
                    print('使用edit函数错误，edit(table_name, data)中 data["属性名"]应为数据表中的属性')
                    return None
            sql = 'update '+table_name+' set '
            arg = []
            for i in self.property_name:
                if i == 'id':
                    continue
                if i not in data:
                    data[i] = i
                    sql = sql+i+' = '+i+', '
                else:
                    sql = sql+i+' = %s, '
                    arg.append(data[i])
            sql = sql[:-2]
            sql = sql+' '
            sql = sql+'where id = %s;'
            arg.append(data['id'])
            print(sql)
            print(arg)
            # sql = f'update {table_name} set name = %s, mail = %s, password = %s, anime = %s, biography = %s  where id = %s;'
            print(type(sql),type(arg))
            send_data = {'sql': sql, 'args': arg}
            import pymysql
            self.db_conn = pymysql.connect(host='39.106.169.58', port=3306, user='Shaco', password='Badwoman',
                                           db='ShacoRoomDB')
            self.cur = self.db_conn.cursor()
            # send_data = {'sql':f'update userinfo set name = %s, mail = mail, password = password, anime = %s, biography = biography where id = %s;'
            #              ,'args':['admin', '少女终末旅行', '1']}
            self.cur.execute(send_data)
            print(f'修改{self.cur.get_count()}条数据')
            return self.cur.get_result()

        else:
            print('使用edit函数错误，edit(table_name, data)中 data应有键值对data["id"]="待修改用户id"')



        # for i in data:
        #     if i in self.property_name:
        #         try:
        #             if i == 'id':
        #                 flag = True
        #                 if self.search(table_name, ['id', data['id']]) is None:
        #                     print(f'未查找到到id为{data[0]}的用户')
        #                     return None
        #                 else:
        #                     sql = f'update {table_name} set {data[1]} = %s where id = %s;'
        #                     send_data = {'sql': sql, 'args': [data[2], data[0]]}
        #                     print('?')
        #                     self.cur.send_sql('edit', send_data)
        #
        #                     print(f'修改{self.cur.get_count()}条数据')
        #                     return self.cur.get_result()
        #
        #         except Exception as e:
        #             # 发生错误
        #             print(f'修改发生错误:{e}')
        #             return None
        # # 如果表中没有相应property 则说明用户使用函数错误
        # print('使用edit函数错误，edit(table_name, data)中 data[1]应为数据表中的属性')
        # return None
