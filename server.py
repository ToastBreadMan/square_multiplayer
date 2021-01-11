import socket
import _thread

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('127.0.0.1', 4444))
server.listen()
clientList = set()
print('Server running on ip 127.0.0.1, on 4444')


def on_client_connect(conn, addr):
    clientList.add(conn)
    print(f"client connected {addr}")
    try:
        while True:
            msg = conn.recv(1024)
            if msg.decode() == 'exit':
                break
            for client in clientList:
                if client != conn:
                    client.send(msg)
                else:
                    pass
    except:
        pass


while True:
    try:
        conn, addr = server.accept()
        _thread.start_new_thread(on_client_connect, (conn, addr))
    except Exception as e:
        print(e)
        pass
