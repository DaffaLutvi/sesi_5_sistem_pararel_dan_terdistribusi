import socket
import threading


HOST = '127.0.0.1'
PORT = 55555

nickname = input("Masukkan nickname: ")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    client.connect((HOST, PORT))
except ConnectionRefusedError:
    print("Gagal terhubung ke server!")
    exit()

def receive_messages():
    """Menerima pesan dari server"""
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if message == 'NICK':
                client.send(nickname.encode('utf-8'))
            else:
                print(message)
        except:
            print("Terputus dari server. Koneksi ditutup.")
            client.close()
            break

def send_messages():
    """Mengirim pesan ke server"""
    while True:
        try:
            message = f"{nickname}: {input('')}"
            client.send(message.encode('utf-8'))
        except:
            print("Gagal mengirim pesan.")
            client.close()
            break


receive_thread = threading.Thread(target=receive_messages)
receive_thread.start()

send_thread = threading.Thread(target=send_messages)
send_thread.start()
