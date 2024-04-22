import socket
import cv2
import pickle
import struct

import pyshine as ps
import imutils

camera = 0

if camera:
    vid = cv2.VideoCapture(0)
else:
    vid = cv2.VideoCapture('3.mkv')

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host_ip = ''
port = 9999
client_socket.connect((host_ip, port))
client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
if client_socket :
    print("Connected to server!!")
    while (vid.isOpened()) :
        try:
            img, frame = vid.read()
            frame = imutils.resize(frame, width=380)
            a = pickle.dumps(frame)
            message = struct.pack("Q", len(a)) + a
            client_socket.sendall(message)
            key = cv2.waitKey(1) & 0xFF
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                client_socket.close()
        except :
            print("!!!DONE!!!")
            break
