from authentication.DAO.dataBase import ConnectSQL
import time

SERVER_ADDRESS = ('39.106.169.58', 3980)
TABLE_NAME = 'userinfo'
if __name__ == '__main__':

    data_search = ['name', 'test']
    data_insert = ['test','213123123','123123@qad']
    data_delete = ['name', 'test']

    conn = ConnectSQL(SERVER_ADDRESS)

    conn.search(TABLE_NAME, data_search)
    conn.insert(TABLE_NAME, data_insert)
    conn.search(TABLE_NAME, data_search)
    conn.delete(TABLE_NAME, data_delete)
    conn.search(TABLE_NAME, data_search)
    conn.insert(TABLE_NAME, data_insert)
    result = conn.search(TABLE_NAME, data_search)
    print('result[0][0]:'+str(result[0][0]))
    data_edit = [str(result[0][0]), 'mail', 'ooooook']

    conn.edit(TABLE_NAME, data_edit)
    conn.search(TABLE_NAME, data_search)
    # conn.delete(TABLE_NAME, data_delete)
    # conn.search(TABLE_NAME, data_search)

