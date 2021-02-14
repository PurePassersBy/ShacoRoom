import configparser
import socket
import struct
import pickle
import sys
from time import strftime, localtime, sleep
import threading
from queue import Queue

sys.path.append('../..')
from authentication.constantName import *

msg_queue = Queue()
SERVER_ADDRESS = ('0.0.0.0', 3976)
MAX_CONNECTIONS = 200
CHUNK = 2048


def get_localtime():
    return strftime("%Y-%m-%d %H:%M:%S", localtime())


def send_package(conn, pack):
    pack_str = pickle.dumps(pack)
    conn.send(struct.pack('i', len(pack_str)))
    conn.send(pack_str)


def fetch_package(conn):
    size = struct.unpack('i', conn.recv(4))[0]
    data = ''.encode()
    while len(data) < size:
        if len(data) + CHUNK > size:
            data += conn.recv(size - len(data))
        else:
            data += conn.recv(CHUNK)
    pack = pickle.loads(data)
    return pack


class Manager(threading.Thread):
    def __init__(self, address=SERVER_ADDRESS, max_connections=MAX_CONNECTIONS):
        super().__init__()
        self._server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._server.bind(address)
        self._server.listen(max_connections)

        self._user2conn = dict()

    def dispatch_message(self):
        while True:
            if not msg_queue.empty():
                msg = msg_queue.get()
                if 'to_id' in msg:
                    send_package(self._user2conn[msg['to_id']], msg)
                    send_package(self._user2conn[msg['user_id']], msg)
                else:
                    for conn in self._user2conn.values():
                        send_package(conn, msg)

            sleep(0.1)

    def handle_connect(self, conn):
        header = fetch_package(conn)
        user_id = header['user_id']
        user_name = header['user_name']
        if user_id in self._user2conn:
            # 重复登录，发送下线请求给当前登录用户
            print('sending kickout')
            kickout_package = {
                'user_id': user_id,
                'user_name': user_name,
                'time': get_localtime(),
                'message': '该账号在其他客户端登录，您已被强制下线',
                'system_code': SYSTEM_CODE_KICK_OUT}
            send_package(self._user2conn[user_id], kickout_package)  # 发送下线请求给已存在的用户
            self._user2conn[user_id].close()  # 确认强制下线客户端收到信息后，断开该用户id对应的conn连接
            del self._user2conn[user_id]
            kickout_package['message'] = '该账号已登录，您已将之前登录的人挤下线'
            kickout_package['system_code'] = SYSTEM_CODE_LOGIN_REPEAT
            send_package(conn, kickout_package)
        self._user2conn[user_id] = conn
        header['time'] = get_localtime()
        header['message'] = 'Enters ShacoRoom'
        # 检查是否有待处理的好友请求信息
        self.check_apply(user_id)
        msg_queue.put(header)
        while True:
            try:
                pack = fetch_package(conn)
                if 'system_code' in pack:
                    self.system_code(pack, conn)
                    continue
                pack['time'] = get_localtime()
                msg_queue.put(pack)
            except Exception as e:
                print(f'{get_localtime()}  {user_name} dirty shutdown : {e}')
                if self._user2conn[user_id] == conn:
                    del self._user2conn[user_id]
                pack = {
                    'user_id': user_id,
                    'user_name': user_name,
                    'message': 'Exits ShacoRoom',
                    'time': get_localtime()
                }
                msg_queue.put(pack)
                break

    def check_apply(self, user_id):
        """
        检查该用户是否有待处理的好友请求信息
        查找用的是O(n)的算法，用户数量增加后登入进聊天室
        的初始化过程可能会较长，需要增加动画效果
        :param user_id: 当前用户id
        :return:
        """
        config = configparser.ConfigParser()
        file = config.read('add_friend.ini')
        config_dict = config.defaults()
        print('Checking apply to do...')
        key_name_to_delete = None
        print(config_dict)
        for key_name in config_dict:
            print('Spot friend apply ')
            split_key_name = key_name.split('-');
            send_id = int(split_key_name[0])
            target_id = int(split_key_name[1])
            if target_id == user_id:
                # 该用户id有待处理的好友请求信息
                dict_temp = eval(config_dict[key_name])
                cmd = dict_temp.keys()[0]
                message = dict_temp.values[0]
                print(dict_temp, cmd, message)
                if cmd == 'APPLY':
                    # 需处理好友请求
                    print(f'Sending friend apply to {user_id}')
                    friend_apply_package = {
                        'send_id': send_id,
                        'time': get_localtime(),
                        'message': message,
                        'system_code': SYSTEM_CODE_FRIEND_APPLY}
                    send_package(self._user2conn[int(user_id)], friend_apply_package)

                else:
                    # 需处理好友请求结果
                    print(f'Sending result of friend apply to {user_id}')
                    friend_reply_package = {
                        'send_id': send_id,
                        'time': get_localtime(),
                        'message': message,
                        'system_code': SYSTEM_CODE_RESULT_FRIEND_APPLY}
                    send_package(self._user2conn[int(user_id)], friend_reply_package)

                # 删除服务器待处理好友请求中该用户的记录
                key_name_to_delete = key_name
                break
        if key_name_to_delete is not None:
            del config_dict[key_name_to_delete]
            # 用户上线后必须处理完好友请求，故不会出现send-target即是APPLY也是REPLY的情况
            with open('add_friend.ini', 'w') as configfile:
                config.write(configfile)



    def system_code(self, pack, conn):
        """
        处理该用户收到的的系统信息
        :param pack:
        :param conn: 该用户对应的socket接口
        :return:
        """
        print('Processing system code...')
        if pack['system_code'] == SYSTEM_CODE_FRIEND_APPLY:
            config = configparser.ConfigParser()
            file = config.read('add_friend.ini')
            config_dict = config.defaults()
            send_id = pack['send_id']
            target_id = pack['target_id']
            key_name = str(send_id) + '-' + str(target_id)
            text = pack['message']
            if key_name in config_dict:
                # 重复发送好友请求
                print(f'send repeat friend apply information to sender:{send_id}')
                repeat_apply_package = {
                    'time': get_localtime(),
                    'send_id': send_id,
                    'message': '您向此用户发送过好友请求，请耐心等待他予以回复',
                    'system_code': SYSTEM_CODE_REPEAT_FRIEND_APPLY}
                send_package(conn, repeat_apply_package)
            else:
                # 发送好友请求的正常情况
                if int(target_id) in self._user2conn:
                    # 当前好友请求目标用户在线
                    print(f'send  friend apply information to target:{target_id}')
                    friend_apply_package = {
                        'send_id': send_id,
                        'time': get_localtime(),
                        'message': text,
                        'system_code': SYSTEM_CODE_FRIEND_APPLY}
                    send_package(self._user2conn[int(target_id)], friend_apply_package)
                else:
                    # 当前好友请求目标用户不在线
                    print(f'write {send_id}-{target_id}:[APPLY]{text} into add_friend.ini')
                    dict_value = {'APPLY': text}
                    config_dict[key_name] = dict_value
                    # 添加好友请求键值对：'发送-目标'--请求信息[类型：内容]
                    with open('add_friend.ini', 'w') as configfile:
                        config.write(configfile)

        if pack['system_code'] == SYSTEM_CODE_RESULT_FRIEND_APPLY:
            config = configparser.ConfigParser()
            file = config.read('add_friend.ini')
            config_dict = config.defaults()
            send_id = pack['send_id']
            target_id = pack['target_id']
            message = pack['message']
            key_name = str(send_id) + '-' + str(target_id)
            if target_id in self._user2conn:
                # 当前好友请求发送用户在线
                print(f'send result of friend apply information to target:{target_id}')
                result_package = {
                    'send_id': send_id,
                    'target_id': target_id,
                    'time': get_localtime(),
                    'message': message,
                    'system_code': SYSTEM_CODE_RESULT_FRIEND_APPLY}
                send_package(self._user2conn[int(target_id)], result_package)
            else:
                # 当前好友请求发送用户不在线
                print(f'write {send_id}-{target_id}:[REPLY]{message} into add_friend.ini')
                dict_value = {'REPLY': message}
                config_dict[key_name] = dict_value
                # 添加好友请求回复键值对：'发送-目标'--好友请求结果[请求类型：内容]
                with open('add_friend.ini', 'w') as configfile:
                    config.write(configfile)

        if pack['system_code'] == SYSTEM_CODE_DELETE_FRIEND:
            config = configparser.ConfigParser()
            file = config.read('delete_friend.ini')
            config_dict = config.defaults()
            send_id = pack['send_id']
            send_name = pack['send_name']
            target_id = pack['target_id']
            message = pack['message']
            key_name = str(send_id) + '-' + str(target_id)
            if target_id in self._user2conn:
                # 当前好友请求发送用户在线
                print(f'send result of delete friend information to target:{target_id}')
                result_package = {
                    'send_id': send_id,
                    'target_id': target_id,
                    'send_name': send_name,
                    'time': get_localtime(),
                    'message': message,
                    'system_code': SYSTEM_CODE_RESULT_DELETE_FRIEND}
                send_package(self._user2conn[int(target_id)], result_package)
            else:
                # 当前好友请求发送用户不在线
                print(f'write {send_id}-{target_id}:{message} into delete_friend.ini')
                config_dict[key_name] = message
                # 添加好友请求回复键值对：'发送-目标'--好友请求结果[请求类型：内容]
                with open('delete_friend.ini', 'w') as configfile:
                    config.write(configfile)

    def run(self):
        print(f"{get_localtime()}  Manager starts...")
        dispatcher = threading.Thread(target=self.dispatch_message)
        dispatcher.setDaemon(True)
        dispatcher.start()
        while True:
            conn, addr = self._server.accept()
            handler = threading.Thread(target=self.handle_connect, args=(conn,))
            handler.setDaemon(True)
            handler.start()

# class Dispatcher(threading.Thread):
#     def __init__(self):
#         super().__init__()
#         self._user2conn = dict()
#
#     def _broadcast(self, msg, sender=None):
#         if sender is not None:
#             msg = f'{sender} {msg}'
#         msg = f'{get_localtime()} {msg}'
#         for conn in self._user2conn.values():
#             conn.send(msg.encode('utf-8'))
#
#     def _direct_message(self, msg, sender, receiver):
#         msg = f'{sender} @you : {msg}'
#         msg = f'{get_localtime()}  {msg}'
#         if receiver not in self._user2conn:
#             self._user2conn[sender].send(f'{get_localtime()}  INFO: {receiver} not online'.encode('utf-8'))
#             return
#         self._user2conn[receiver].send(msg.encode('utf-8'))
#
#     def _video_call_request(self, sender, receiver):
#         if receiver not in self._user2conn:
#             self._user2conn[sender].send(f'{get_localtime()}  INFO: {receiver} not online'.encode('utf-8'))
#             return
#         self._user2conn[receiver].send(f'{get_localtime()}  INFO: {sender} want to make a video chat with you. (#agree_{sender}/#refuse_{sender})'.encode('utf-8'))
#
#     def _video_call_response(self, sender, receiver, msg):
#         if receiver not in self._user2conn:
#             self._user2conn[sender].send(f'{get_localtime()}  INFO: {receiver} not online'.encode('utf-8'))
#             return
#         if msg == 0:
#             self._user2conn[receiver].send(f'{get_localtime()}  INFO: {sender} refuse your video chat'.encode('utf-8'))
#         else:
#             self._user2conn[receiver].send(f'{get_localtime()}  INFO: {sender} agree your video chat'.encode('utf-8'))
#             self._user2conn[receiver].send(f'#VideoChat Permission'.encode('utf-8'))
#             self._user2conn[sender].send(f'#VideoChat Permission'.encode('utf-8'))
#
#     def _handle_exit(self, user, safe):
#         if safe:
#             self._user2conn[user].send(f'#Exit Permission'.encode('utf-8'))
#         self._user2conn[user].close()
#         del self._user2conn[user]
#
#     def run(self):
#         print(f"{get_localtime()}  Dispatcher starts...")
#         while True:
#             if not msg_queue.empty():
#                 type, sender, receiver, msg = msg_queue.get()
#                 if type == 0:
#                     if msg == None:
#                         self._handle_exit(sender, receiver)
#                         self._broadcast(f'{sender} exits room')
#                         print(f'{get_localtime()}  {sender} exits safely...')
#                     else:
#                         self._user2conn[sender] = msg
#                         self._broadcast(f'{sender} enters room')
#                 elif type == 1:
#                     if receiver == None:
#                         self._broadcast(msg, sender)
#                     else:
#                         self._direct_message(msg, sender, receiver)
#                 elif type == 2:
#                     self._video_call_request(sender, receiver)
#                 elif type == 3:
#                     self._video_call_response(sender, receiver, msg)
#
#
# class Connection(threading.Thread):
#     def __init__(self, conn, addr, buffer_size=1024):
#         super().__init__()
#         self._conn = conn
#         self._addr = addr
#         self._buffer_size = buffer_size
#         self._encoding = 'utf-8'
#         self._username = None
#
#     def _send_exit_msg(self, safe=0):
#         msg_queue.put((0, self._username, safe, None))
#     def _send_create_msg(self):
#         msg_queue.put((0, self._username, None, self._conn))
#     def run(self):
#         self._username = self._conn.recv(self._buffer_size).decode(self._encoding)
#         self._send_create_msg()
#         while True:
#             try:
#                 msg = self._conn.recv(self._buffer_size).decode(self._encoding)
#                 if msg[0] == '@':
#                     pos = msg.find(' ')
#                     if pos==-1:
#                         msg_queue.put((1, self._username, msg[1:], ''))
#                     else:
#                         msg_queue.put((1, self._username, msg[1:pos], msg[pos:]))
#                 elif msg == '#exit':
#                     self._send_exit_msg(1)
#                     return
#                 elif '#video_chat_' in msg:
#                     msg_queue.put((2, self._username, msg[len('#video_chat_'):], None))
#                 elif '#agree_' in msg:
#                     msg_queue.put((3, self._username, msg[len('#agree_'):], 1))
#                 elif 'refuse_' in msg:
#                     msg_queue.put((3, self._username, msg[len('#refuse_'):], 0))
#                 else:
#                     msg_queue.put((1, self._username, None, msg))
#             except Exception as e:
#                 self._send_exit_msg(0)
#                 print(f'{get_localtime()}  {self._username} dirty shutdown : {e}')
#                 break
