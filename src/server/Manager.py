import socket
from time import strftime, localtime, sleep
import threading
from queue import Queue

msg_queue = Queue()


def get_localtime():
    return strftime("%Y-%m-%d %H:%M:%S", localtime())


class Command():
    def __init__(self, id):
        self._id = id
    def getId(self):
        return self._id


class Manager(threading.Thread):
    def __init__(self, address=('0.0.0.0',3976), max_connections = 20):
        super().__init__()
        self._addr = address
        self._max_connections = max_connections
        self._server = None
        self._init_server()

    def _init_server(self):
        self._server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._server.bind(self._addr)
        self._server.listen(self._max_connections)

    def run(self):
        print(f"{get_localtime()}  Manager starts...")
        dispatcher = Dispatcher()
        dispatcher.setDaemon(True)
        dispatcher.start()
        while True:
            conn, addr = self._server.accept()
            conn = Connection(conn, addr)
            conn.start()


class Dispatcher(threading.Thread):
    def __init__(self):
        super().__init__()
        self._user2conn = dict()

    def _broadcast(self, msg, sender=None):
        if sender != None:
            msg = f'{sender} {msg}'
        msg = f'{get_localtime()} {msg}'
        for conn in self._user2conn.values():
            conn.send(msg.encode('utf-8'))

    def _direct_message(self, msg, sender, receiver):
        msg = f'{sender} @you : {msg}'
        msg = f'{get_localtime()}  {msg}'
        if receiver not in self._user2conn:
            self._user2conn[sender].send(f'{get_localtime()}  INFO: {receiver} not online'.encode('utf-8'))
            return
        self._user2conn[receiver].send(msg.encode('utf-8'))

    def _video_call_request(self, sender, receiver):
        if receiver not in self._user2conn:
            self._user2conn[sender].send(f'{get_localtime()}  INFO: {receiver} not online'.encode('utf-8'))
            return
        self._user2conn[receiver].send(f'{get_localtime()}  INFO: {sender} want to make a video chat with you. (#agree_{sender}/#refuse_{sender})'.encode('utf-8'))

    def _video_call_response(self, sender, receiver, msg):
        if receiver not in self._user2conn:
            self._user2conn[sender].send(f'{get_localtime()}  INFO: {receiver} not online'.encode('utf-8'))
            return
        if msg == 0:
            self._user2conn[receiver].send(f'{get_localtime()}  INFO: {sender} refuse your video chat'.encode('utf-8'))
        else:
            self._user2conn[receiver].send(f'{get_localtime()}  INFO: {sender} agree your video chat'.encode('utf-8'))
            self._user2conn[receiver].send(f'#VideoChat Permission'.encode('utf-8'))
            self._user2conn[sender].send(f'#VideoChat Permission'.encode('utf-8'))

    def _handle_exit(self, user, safe):
        if safe:
            self._user2conn[user].send(f'#Exit Permission'.encode('utf-8'))
        self._user2conn[user].close()
        del self._user2conn[user]

    def run(self):
        print(f"{get_localtime()}  Dispatcher starts...")
        while True:
            if not msg_queue.empty():
                type, sender, receiver, msg = msg_queue.get()
                if type == 0:
                    if msg == None:
                        self._handle_exit(sender, receiver)
                        self._broadcast(f'{sender} exits room')
                        print(f'{get_localtime()}  {sender} exits safely...')
                    else:
                        self._user2conn[sender] = msg
                        self._broadcast(f'{sender} enters room')
                elif type == 1:
                    if receiver == None:
                        self._broadcast(msg, sender)
                    else:
                        self._direct_message(msg, sender, receiver)
                elif type == 2:
                    self._video_call_request(sender, receiver)
                elif type == 3:
                    self._video_call_response(sender, receiver, msg)


class Connection(threading.Thread):
    def __init__(self, conn, addr, buffer_size=1024):
        super().__init__()
        self._conn = conn
        self._addr = addr
        self._buffer_size = buffer_size
        self._encoding = 'utf-8'
        self._username = None

    def _send_exit_msg(self, safe=0):
        msg_queue.put((0, self._username, safe, None))
    def _send_create_msg(self):
        msg_queue.put((0, self._username, None, self._conn))
    def run(self):
        self._username = self._conn.recv(self._buffer_size).decode(self._encoding)
        self._send_create_msg()
        while True:
            try:
                msg = self._conn.recv(self._buffer_size).decode(self._encoding)
                if msg[0] == '@':
                    pos = msg.find(' ')
                    if pos==-1:
                        msg_queue.put((1, self._username, msg[1:], ''))
                    else:
                        msg_queue.put((1, self._username, msg[1:pos], msg[pos:]))
                elif msg == '#exit':
                    self._send_exit_msg(1)
                    return
                elif '#video_chat_' in msg:
                    msg_queue.put((2, self._username, msg[len('#video_chat_'):], None))
                elif '#agree_' in msg:
                    msg_queue.put((3, self._username, msg[len('#agree_'):], 1))
                elif 'refuse_' in msg:
                    msg_queue.put((3, self._username, msg[len('#refuse_'):], 0))
                else:
                    msg_queue.put((1, self._username, None, msg))
            except Exception as e:
                self._send_exit_msg(0)
                print(f'{get_localtime()}  {self._username} dirty shutdown : {e}')
                break
