import pymysql


class conn():
    def __init__(self):
        # self.conn = pymysql.connect(host='192.168.1.105', port=3306, user='root', password='123456', db='shacousers',
        #                            charset='utf8', )
        self.conn = pymysql.connect(host='39.106.169.58', port=3306, user='Shaco', password='Badwoman',
                                    db='ShacoRoomDB',
                                    charset='utf8mb4', )
        self.cur = self.conn.cursor()
        # 获取数据库中的用户数量count
        # 新用户注册其id为count+1
        self.count = self.cur.execute('SELECT * from userinfo')
        # 解决中文编码问题
        self.cur.execute("ALTER TABLE userinfo CONVERT TO CHARACTER SET utf8mb4;")

    def test(self):
        self.cur.execute("SELECT VERSION()")
        data = self.cur.fetchone()
        print("Database version:%s" % data)

    def close(self):
        self.cur.close()
        self.conn.close()

    def insert(self, nameInsert, mailInsert, passwordInsert):
        try:
            sql = 'insert into userinfo(id,name,mail,password) values(%s,%s,%s,%s);'
            # 将用户提交的昵称、邮箱地址、密码提交,用户的ID为当前表行数+1
            self.count += 1
            print(self.count)
            result = self.cur.execute(sql, [int(self.count), str(nameInsert), str(mailInsert), str(passwordInsert)])
            self.conn.commit()
            print("Changed row:%s,", result)
            print("提交新用户数据成功")
        except Exception:
            print("提交新用户数据发生错误")

    def login(self, mail, password):
        try:
            sql = 'select * from userinfo where mail = %s and password = %s'
            rows = self.cur.execute(sql, [mail, password])
            if rows:
                print("邮箱密码正确")
                return True
            else:
                print("邮箱或密码错误")
                return False
        except Exception:
            print("登录邮箱密码查询失败")

    def mailRepeat(self, mail):
        try:
            sql = 'select * from userinfo where mail = %s'
            rows = self.cur.execute(sql, [mail])
            if rows:
                print("邮箱已被注册")
                return True
            else:
                print("邮箱合法")
                return False
        except Exception:
            print("邮箱重复查询失败")

    def delete(self):
        sql = "delete from userinfo where id=%d;"
        self.cur.execute(sql, [self.count])
        self.count -= 1
        self.conn.commit()
