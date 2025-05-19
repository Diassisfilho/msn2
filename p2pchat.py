import socket
import threading

connections = []
lock = threading.Lock()

def encrypt(text):
    encrypted = ''
    for char in text:
        if char.isalpha():
            shifted = ord(char) + 3
            if char.islower():
                if shifted > ord('z'):
                    shifted -= 26
            else:
                if shifted > ord('Z'):
                    shifted -= 26
            encrypted += chr(shifted)
        else:
            encrypted += char
    return encrypted

def decrypt(text):
    decrypted = ''
    for char in text:
        if char.isalpha():
            shifted = ord(char) - 3
            if char.islower():
                if shifted < ord('a'):
                    shifted += 26
            else:
                if shifted < ord('A'):
                    shifted += 26
            decrypted += chr(shifted)
        else:
            decrypted += char
    return decrypted

def handle_receive(sock):
    while True:
        try:
            data = sock.recv(1024).decode()
            if not data:
                break
            print(decrypt(data))
        except:
            break
    sock.close()
    with lock:
        if sock in connections:
            connections.remove(sock)

def server(listen_port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', listen_port))
    s.listen()
    while True:
        conn, addr = s.accept()
        with lock:
            connections.append(conn)
        threading.Thread(target=handle_receive, args=(conn,)).start()

def main():
    listen_port = int(input())
    server_thread = threading.Thread(target=server, args=(listen_port,))
    server_thread.start()
    while True:
        cmd = input()
        if cmd.startswith("/connect "):
            _, peer = cmd.split(' ', 1)
            host, port = peer.split(':')
            port = int(port)
            s = socket.socket()
            try:
                s.connect((host, port))
                with lock:
                    connections.append(s)
                threading.Thread(target=handle_receive, args=(s,)).start()
            except:
                pass
        else:
            encrypted = encrypt(cmd)
            with lock:
                conns = connections.copy()
            for conn in conns:
                try:
                    conn.send(encrypted.encode())
                except:
                    with lock:
                        if conn in connections:
                            connections.remove(conn)
                    conn.close()

if __name__ == "__main__":
    main()