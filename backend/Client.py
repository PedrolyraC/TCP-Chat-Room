import socket
from threading import Thread
from datetime import datetime

SERVER_HOST = socket.gethostbyname(socket.gethostname())
SERVER_PORT = 5002

separator_token = "<SEP>"

s = socket.socket()
print(f"[*] Connecting to {SERVER_HOST}:{SERVER_PORT}...")

s.connect((SERVER_HOST, SERVER_PORT))
print("[+] Connected.")

userIp = socket.gethostbyname(socket.gethostname())

def listen_for_messages():
    while True:
        message = s.recv(256).decode()
        print("\n {}".format(message))
        
t = Thread(target=listen_for_messages)
t.daemon = True
t.start()

while True:
    to_send = input()
    
    if to_send.lower() == 'q':
        break
    date_now = datetime.now().strftime('%Y/%m/%d %H:%M:%S')
    to_send = f"[{date_now}] {userIp}{separator_token}{to_send}"
    s.send(to_send.encode())
    
s.close()
