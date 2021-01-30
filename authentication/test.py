from authentication.DAO.dataBase import ConnectSQL
import time

SERVER_ADDRESS = ('39.106.169.58', 3980)

if __name__ == '__main__':
    table_name = 'userinfo'
    data_search = ['name', 'test']
    data_insert = ['test','213123123','123123@qad']
    data_delete = ['name', 'test']
    data_edit = ['9', 'mail', 'ooooook']
    conn = ConnectSQL(SERVER_ADDRESS)
    # conn.search(table_name, data_search)

    conn.insert(table_name, data_insert)
    conn.search(table_name, data_search)
    conn.delete(table_name, data_delete)
    conn.search(table_name, data_search)
    conn.insert(table_name, data_insert)
    conn.edit(table_name, data_edit)
    conn.search(table_name, data_search)
    conn.delete(table_name, data_delete)
    conn.search(table_name, data_search)

