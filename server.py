import socket
import cv2
import pickle
import struct

import pyshine as ps
import imutils
import threading

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host_ip = ''
port = 9999
server_socket.bind((host_ip, port))
server_socket.listen(5)
print(f"Server listening on port {port}")

def show_client(addr, client_socket):
    try:
        print(f"Client {addr} connected!!!")
        if client_socket:
            data = b''
            payload_size = struct.calcsize("Q")
            while True:
                while len(data) < payload_size:
                    packet = client_socket.recv(4*1024)
                    if not packet:
                        break
                    data += packet
                packed_msg_size = data[:payload_size]
                data = data[payload_size:]
                msg_size = struct.unpack("Q", packed_msg_size)[0]
                
                while len(data) < msg_size:
                    data += client_socket.recv(4*1024)
                frame_data = data[:msg_size]
                data = data[msg_size:]
                frame = pickle.loads(frame_data)
                text = f'Client: {addr}'
                frame = ps.putBText(frame, text, 10, 10, vspace=10, hspace=1, font_scale=0.5, background_RGB=(255,0,0), text_RGB=(255,250,250))
                cv2.imshow(f'From {addr}', frame)
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q'):
                    break
            client_socket.close()
    except:
        print(f'Client {addr} disconnected')
        pass

while True:
    client, addr = server_socket.accept()
    thread = threading.Thread(target=show_client, args=(addr, client))
    thread.start()
    # print(f"Total clients active {threading.activeCount - 1}")