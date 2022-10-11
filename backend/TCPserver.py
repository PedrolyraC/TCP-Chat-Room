import socket
from threading import Thread


SERVER_HOST = "0.0.0.0"
SERVER_PORT = 5002 # porta usada
separator_token = "<SEP>" # vai ser utilizado para separar mensagem de ip de usuário

client_sockets = set()

s = socket.socket()
# deixa a porta reutilizável
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # pesquisar

s.bind((SERVER_HOST, SERVER_PORT))

s.listen(5)
print(f"[*] Listening as {SERVER_HOST}:{SERVER_PORT}")

def client_listener(cs):
    while True:
        try:
            msg = cs.recv(256).decode('utf-8')
        except Exception as e:
            print(f"[!] Error: {e}")
            client_sockets.remove(cs)
        else:
            msg = msg.replace(separator_token, ": ")
        for client_socket in client_sockets:
            client_socket.send(msg.encode('utf-8'))
            
while True:
    client_socket, client_address = s.accept()
    print(f"[+] {client_address} connected.")
    
    client_sockets.add(client_socket)
    
    thread = Thread(target=client_listener, args=(client_socket,))
    thread.daemon = True
    thread.start()

for cs in client_sockets:
    cs.close()
s.close()
