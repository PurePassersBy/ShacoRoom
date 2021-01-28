from authentication.DAO.dataBase import Connect

# 运行主窗口
if __name__ == "__main__":
    test = Connect()
    # 查找mail 中 是614446871@qq.com 的用户
    res = test.search('mail', '614446871@qq.com')
    # 增加用户名为 shaco 邮箱为 614446871@qq.com 密码为 123123 的用户
    test.insert('shaco', '614446871@qq.com', '123123')
    # 查找mail 中 是614446871@qq.com 的用户， 用户信息用res储存
    res = test.search('mail', '614446871@qq.com')
    # res格式如下
    print(res)
    # 编辑用户id 为 res中第一条数据中 第一个属性（即ID）, 把 name 这一属性 修改为 xuans
    test.edit(str(res[0][0]), 'name', 'xuans')
    # 无参删除：删除数据库最后一条数据
    test.delete()
    # 查找mail 中 是614446871@qq.com 的用户,被删除
    test.search('mail', '614446871@qq.com')

    test.close()