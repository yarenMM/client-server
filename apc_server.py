import socket
import os
from _thread import *

ServerSocket = socket.socket()
host = '127.0.0.1'
port = 1233

inx = 0
out = 0
inside = 0

try:
    ServerSocket.bind((host, port))
except socket.error as e:
    print(str(e))

print('Waiting for a Connection..')
#ServerSocket.listen(5)
ServerSocket.listen()


def threaded_client(connection):
    global inx
    global out
    global inside

   # connection.send(str.encode('Welcome to the Servern'))
    while True:
        data = connection.recv(2048)
        reply = data.decode('utf-8')
        if not data:
            break

       # replysplit = reply.split(",")
        #inx = inx + replysplit[0]
        #out = out + replysplit[1]
       # inside = inside + replysplit[3]
        if reply == "1":
            inx += 1
        if reply == "0":
            out += 1
        inside = inx - out
        print('In: {}, Out: {}, Inside: {}'.format(inx,out,inside))
       # print('In: {}, Out: {}, Inside: {}'.format(inx,out,inside))

        #print(reply)

        #connection.sendall(str.encode(reply))
    connection.close()

while True:
    Client, address = ServerSocket.accept()
    print('Connected to: ' + address[0] + ':' + str(address[1]))
    start_new_thread(threaded_client, (Client, ))

ServerSocket.close()