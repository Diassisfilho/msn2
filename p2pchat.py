import socket
import threading
import sys

connections = []
lock = threading.Lock()
is_running = True  # Add this flag to control threads

def encrypt(text):
    encrypted = ''
    for char in text:
        if char.isalpha():
            shifted = ord(char) + 5
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
            shifted = ord(char) - 5
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
    global is_running
    while is_running:  # Check the flag
        try:
            data = sock.recv(1024).decode()
            if not data:
                break
            print("\n[someone:???]> "+decrypt(data))
        except:
            break
    sock.close()
    with lock:
        if sock in connections:
            connections.remove(sock)

def server(listen_port):
    global is_running
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('', listen_port))
    server_socket.listen()
    server_socket.settimeout(1)  # Add timeout to check is_running flag
    
    while is_running:
        try:
            conn, addr = server_socket.accept()
            with lock:
                connections.append(conn)
            threading.Thread(target=handle_receive, args=(conn,)).start()
        except socket.timeout:
            continue
        except:
            break
    
    server_socket.close()

def main():
    global is_running
    listen_port = int(input("insert your port: "))
    server_thread = threading.Thread(target=server, args=(listen_port,))
    server_thread.start()

    while True:
        try:
            cmd = input(f"[localhost:{listen_port}]> ")
            if cmd == "/exit":
                print("Closing connections and exiting...")
                is_running = False  # Set flag to stop threads
                with lock:
                    for conn in connections:
                        try:
                            conn.close()
                        except:
                            pass
                    connections.clear()
                server_thread.join(timeout=2)  # Wait for server thread to finish
                sys.exit(0)
            elif cmd.startswith("/connect "):
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
                    print("Failed to connect to peer")
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
        except KeyboardInterrupt:
            is_running = False
            print("\nClosing connections and exiting...")
            with lock:
                for conn in connections:
                    try:
                        conn.close()
                    except:
                        pass
                connections.clear()
            server_thread.join(timeout=2)
            sys.exit(0)

if __name__ == "__main__":
    main()