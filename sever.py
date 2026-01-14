from distutils.log import error
import socket
import sys
from _thread import *

sever = "192.168.0.105"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((sever, port))

except socket.error as e:
    str(e)

s.listen(2) #people to conect = 2
print("Watit forr connection")

def threaded_client(conn):
    reply = ""
    while True:
        try:
            data = conn.recv(2048)
            reply = data.decode("uft-8")

            if not data:
                print("Disconect")
                break
            else: 
                print("Recive: ", reply)
                print("Sending: ", reply)
            conn.sendall(str.encode(reply))
        except: break
    
    print("Lost connection")
    conn.close()


while True:
    conn, addr =s.accept()
    print("Connected to", addr)

    start_new_thread(threaded_client,(conn,))
