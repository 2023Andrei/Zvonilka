import socket
import threading

# Простой чат-сервер
HOST = '127.0.0.1'
PORT = 5000
clients = []

def broadcast(msg, sender):
    for client in clients:
        if client != sender:
            try:
                client.send(msg)
            except:
                client.close()
                clients.remove(client)

def handle_client(conn):
    while True:
        try:
            msg = conn.recv(1024)
            if msg:
                broadcast(msg, conn)
        except:
            break
    conn.close()
    clients.remove(conn)

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    print(f"Сервер запущен на {HOST}:{PORT}")

    while True:
        conn, addr = server.accept()
        clients.append(conn)
        thread = threading.Thread(target=handle_client, args=(conn,))
        thread.start()

if __name__ == "__main__":
    main()
