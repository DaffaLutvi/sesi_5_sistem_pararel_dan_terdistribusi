import socket
import threading


HOST = '127.0.0.1'  
PORT = 55555        

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

clients = []
nicknames = []

def broadcast(message, _client=None):
    """Mengirim pesan ke semua client yang terhubung"""
    for client in clients:
        if client != _client:
            try:
                client.send(message)
            except:
                index = clients.index(client)
                clients.remove(client)
                client.close()
                nickname = nicknames[index]
                broadcast(f"{nickname} telah keluar dari chat.\n".encode('utf-8'))
                nicknames.remove(nickname)
                break

def handle_client(client):
    """Menangani koneksi tiap client"""
    while True:
        try:
            message = client.recv(1024)
            broadcast(message, client)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast(f"{nickname} telah keluar dari chat.\n".encode('utf-8'))
            nicknames.remove(nickname)
            break

def receive_connections():
    """Menerima banyak koneksi client"""
    print("Server berjalan dan menunggu koneksi...")
    while True:
        client, address = server.accept()
        print(f"Koneksi baru dari {address}")

        client.send("NICK".encode('utf-8'))
        nickname = client.recv(1024).decode('utf-8')
        nicknames.append(nickname)
        clients.append(client)

        print(f"Nickname client: {nickname}")
        broadcast(f"{nickname} bergabung ke chat!\n".encode('utf-8'))
        client.send("Terhubung ke server!\n".encode('utf-8'))

        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()

receive_connections()
