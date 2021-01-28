import pymysql


class Connect:
    def __init__(self):
        # self.conn = pymysql.connect(host='192.168.1.105', port=3306, user='root', password='123456', db='shacousers',
        #                            charset='utf8', )
        self.conn = pymysql.connect(host='39.106.169.58', port=3306, user='Shaco', password='Badwoman',
                                    db='ShacoRoomDB',
                                    charset='utf8', )
        self.cur = self.conn.cursor()
        # 获取数据库中的用户数量count
        # 新用户注册其id为count+1
        self.count = self.cur.execute('SELECT * from userinfo')
        # 解决中文编码问题
        self.cur.execute("ALTER TABLE userinfo CONVERT TO CHARACTER SET utf8;")
        # 防止直接用str代替sql表属性名出现错误
        self.search_property = {'id': 'select * from userinfo where id = %s;',
                                'name': 'select * from userinfo where name = %s;',
                                'mail': 'select * from userinfo where mail = %s;',
                                'password': 'select * from userinfo where password = %s;'}

        self.edit_property = {'name':'update userinfo set name = %s WHERE id = %s;',
                              'mail':'update userinfo set mail = %s WHERE id = %s;',
                              'password':'update userinfo set password = %s WHERE id = %s;',}

    def test(self):
        """
        检测数据库是否连接成功，打印数据库版本号
        :param
        :return
        """
        self.cur.execute("SELECT VERSION()")
        data = self.cur.fetchone()
        print("Database version:%s" % data)

    def close(self):
        """
        关闭cur与connect
        :param
        :return
        """
        self.cur.close()
        self.conn.close()

    def insert(self, nameInsert, mailInsert, passwordInsert):
        """
        向数据库插入数据，不允许留空
        :param nameInsert:用户名
        :param mailInsert:邮箱
        :param passwordInsert:密码
        :return bool:查询结果
        """
        try:
            sql = 'insert into userinfo(id,name,mail,password) values(%s,%s,%s,%s);'
            # 将用户提交的昵称、邮箱地址、密码提交,用户的ID为当前表行数+1
            self.count += 1
            self.cur.execute(sql, [self.count, str(nameInsert), str(mailInsert), str(passwordInsert)])
            print("提交新用户数据成功,当前数据库储存用户数：" + str(self.count))
            print("提交的内容:" + "id:" + str(self.count) + "  name:" + nameInsert + "  mail:"
                  + mailInsert + "  password:" + passwordInsert)
            self.conn.commit()
        except Exception:
            # 发生错误，回滚
            print("提交新用户数据发生错误")
            self.conn.rollback()

    def search(self, prop, content):
        """
        在数据库查询数据，输入要查询的属性，以及对应内容，返回该用户的所有数据
        :param prop:在数据库中的名称：id、name、mail、password
        :param content:具体内容
        :return results:一个n维数组[n][id, name, mail, password]
        """
        # 将输入转化成str

        prop = str(prop)
        content = str(content)
        for i in self.search_property.keys():
            if str(i) == prop:
                try:
                    sql = str(self.search_property[prop])
                    rows = self.cur.execute(sql, [content])
                    results = self.cur.fetchall()
                    if rows:
                        print('共查询到符合条件的 ' + str(rows) + '条')
                        print(results)
                        return results
                    else:
                        print('没有查询到符合条件的数据')
                        return None
                except Exception:
                    # 发生错误，回滚
                    print('查询发生错误')
                    self.conn.rollback()
                    return None
        # 如果表中没有相应property 则说明用户使用函数错误
        print('使用search函数错误，search(property, content)property应为数据表中的属性')
        return None

    def delete(self, id_delete):
        """
        删除数据库的最后一条
        :param id_delete:代删除的id
        :return
        """
        try:
            sql = "delete from userinfo where id = %s;"
            rows = self.cur.execute(sql, [id_delete])
            if rows:
                self.count -= 1
                print('删除成功，数据库共有' + str(self.count) + '条数据')
                self.conn.commit()
            else:
                print('未查到此ID，删除失败')
        except Exception:
            # 发生错误，回滚
            print('删除发生错误')
            self.conn.rollback()

    def delete(self):
        """
        无输入参数时，删除数据库的最后一条
        :param
        :return
        """
        try:
            sql = "delete from userinfo where id = %s;"
            rows = self.cur.execute(sql, [self.count])
            if rows:
                self.count -= 1
                print('删除成功，数据库共有' + str(self.count) + '条数据')
                self.conn.commit()
            else:
                print('未查到此ID，删除失败')
        except Exception:
            # 发生错误，回滚
            print('删除发生错误')
            self.conn.rollback()

    def edit(self, id_edit, prop, content):
        """
        在数据库更改数据，输入要更改的属性，以及修改后的对应内容，返回该用户的所有数据
        :param prop: 在数据库中的名称：id、name、mail、password
        :param id_edit: 要修改的用户id
        :param content:具体内容
        :return results:一个n维数组[n][id, name, mail, password]
        """
        id_edit = int(id_edit)
        prop = str(prop)
        content = str(content)
        for i in self.search_property.keys():
            if str(i) == prop:
                try:
                    # 储存修改前的数据
                    search_sql = 'select * from userinfo where id = %s;'
                    rows = self.cur.execute(search_sql, [id_edit])
                    results_pre = self.cur.fetchall()
                    if rows:
                        # 对目标数据进行修改
                        sql = self.edit_property[prop]
                        self.cur.execute(sql, [content, id_edit])
                        # 获得修改后的数据
                        self.cur.execute(search_sql, [id_edit])
                        results = self.cur.fetchall()
                        print('共查询到符合条件的待修改数据 ' + str(rows) + '条')
                        print('修改前：' + str(results_pre))
                        print('修改后' + str(results))
                        self.conn.commit()
                        return results
                    else:
                        print('没有查询到符合条件的待修改数据的ID')
                        return None
                except Exception:
                    # 发生错误，回滚
                    print('更改发生错误')
                    self.conn.rollback()
                    return None
        # 如果表中没有相应property 则说明用户使用函数错误
        print('使用edit函数错误，edit(property, content)property应为数据表中的属性')
        return None
