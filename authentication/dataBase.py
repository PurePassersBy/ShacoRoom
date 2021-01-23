import pymysql

class conn():
    def __init__(self):
        self.conn = pymysql.connect(host='localhost', port=3306, user='root', password='123456', db='shacoUsers',
                                    charset='utf8', )
        self.cur = self.conn.cursor()
        # 获取数据库中的用户数量count
        # 新用户注册其id为count+1
        self.count=self.cur.execute('SELECT COUNT(*) AS NumberOfUsers FROM shacoUsers')

    def test(self):
        self.cur.execute("SELECT VERSION()")
        data = self.cur.fetchone()
        print("Database version:%s" % data)

    def close(self):
        self.cur.close()
        self.conn.close()

    def insert(self,nameInsert,mailInsert,passwordInsert):

        sql='insert into shacoUsers(id,name,mail,password) values(%d,%s,%s,%s);'
        # 将用户提交的昵称、邮箱地址、密码提交,用户的ID为当前表行数+1
        self.count += 1
        self.cur.execute(sql,[self.count,nameInsert,mailInsert,passwordInsert])
        self.conn.commit()

    def delete(self):
        sql = "delete from shacoUsers where id=%d;"
        self.cur.execute(sql,[self.count])
        self.conn.commit()




