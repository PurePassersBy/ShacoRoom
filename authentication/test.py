from authentication.DAO.dataBase import Connect

# 运行主窗口
if __name__ == "__main__":
    test = Connect()
    res = test.search('mail', '614446871@qq.com')
    test.insert('shaco', '614446871@qq.com', '123123')
    res = test.search('mail', '614446871@qq.com')
    test.edit(str(res[0][0]), 'name', 'xuans')
    test.delete()
    # test.search('mail', '614446871@qq.com')

    test.close()