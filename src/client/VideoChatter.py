import threading
import socket
import struct
import sys
import time
import numpy as np

import cv2

FX = 0.4
INTERVAL = 3
CHUNK = 8192
ENCODE_PARAM = [int(cv2.IMWRITE_JPEG_QUALITY), 30]

class VideoChatter(threading.Thread):
    def __init__(self, addr):
        super().__init__()
        self._addr = addr
        self._client = None
    def run(self):
        self._client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._client.connect(self._addr)
        receiver = VideoReceiver(self._client)
        sender = VideoSender(self._client)
        receiver.start()
        sender.start()

class VideoSender(threading.Thread):
    def __init__(self, conn):
        super().__init__()
        self.socket = conn
        self.cap = None

    def __del__(self):
        self.socket.close()
        self.cap.release()

    def run(self):
        self.cap = cv2.VideoCapture(0)
        #self.cap = cv2.VideoCapture('video_result.mp4')
        print('VideoSender Starts')
        while self.cap.isOpened():
            last = time.time()
            ret, frame = self.cap.read()
            rframe = cv2.resize(frame, (0, 0), fx=FX, fy=FX)
            #print(sys.getsizeof(frame), sys.getsizeof(rframe))
            #img_encode = cv2.imencode('.jpg', rframe)[1]
            img_encode = cv2.imencode('.jpg', rframe, ENCODE_PARAM)[1]
            #print('test', sys.getsizeof(test))
            #print('jpg', sys.getsizeof(img_encode))
            data_encode = np.array(img_encode)
            str_encode = data_encode.tostring()
            #data = pickle.dumps(rframe)
            #zdata = zlib.compress(data, zlib.Z_BEST_COMPRESSION)
            #print(sys.getsizeof(data), sys.getsizeof(zdata))
            #print('压缩图片',time.time() - last)
            last = time.time()
            try:
                self.socket.sendall(struct.pack("L", len(str_encode)) + str_encode)
            except Exception as e:
                print(type(e),e)
                break
            #print('传输图片',time.time() - last)
            time.sleep(0.1)
            #for i in range(INTERVAL):
            #    self.cap.read()


class VideoReceiver(threading.Thread):
    def __init__(self, conn):
        super().__init__()
        self.socket = conn

    def __del__(self):
        self.socket.close()
        try:
            cv2.destroyAllWindows()
        except:
            pass

    def run(self):
        data = ''.encode('utf-8')
        payload_size = struct.calcsize("L")
        cv2.namedWindow('Video Chat', cv2.WINDOW_NORMAL)
        print('VideoReceiver Starts')

        while True:
            try:
                while len(data) < payload_size:
                    data += self.socket.recv(CHUNK)
                packed_size = data[:payload_size]
                data = data[payload_size:]
                msg_size = struct.unpack("L", packed_size)[0]
                while len(data) < msg_size:
                    data += self.socket.recv(CHUNK)
                #nparr = np.fromstring(data[:msg_size], np.uint8)
                nparr = np.asarray(bytearray(data[:msg_size]), np.uint8)
                img_decode = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
                #cframe_data = data[:msg_size]
                #frame_data = zlib.decompress(cframe_data)
                #frame = pickle.loads(frame_data)
                data = data[msg_size:]
                cv2.imshow('Video Chat', img_decode)
                if cv2.waitKey(100) & 0xFF == 27:
                    break
            except Exception as e:
                print(e)
                break