# https://github.com/Diassisfilho/msn2.git
import socket
import threading
import sys
import argparse

connections = []
lock = threading.Lock()
is_running = True
idendity = ""

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
    try:
        peer_name = sock.getpeername()
        peer_addr = f"{peer_name[0]}:{peer_name[1]}"
    except:
        peer_addr = "unknown"
        
    while is_running:
        try:
            data = sock.recv(1024).decode()
            if not data:
                break
            # print("",end="\r")
            print(f"\r[{peer_addr}]> {decrypt(data)}")
            print(idendity,end="",flush=True)
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
    server_socket.settimeout(1)
    
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
    global is_running, idendity
    
    parser = argparse.ArgumentParser(description='MSN2 - A P2P Chat Application')
    parser.add_argument('-p', '--port', type=int, required=True, help='Port to listen on')
    parser.add_argument('-c', '--connect', nargs='*', help='Peers to connect to in format host:port')
    args = parser.parse_args()

    server_thread = threading.Thread(target=server, args=(args.port,))
    server_thread.start()
    idendity = f"[localhost:{args.port}]> "

    if args.connect:
        for peer in args.connect:
            try:
                host, port = peer.split(':')
                port = int(port)
                s = socket.socket()
                s.connect((host, port))
                with lock:
                    connections.append(s)
                threading.Thread(target=handle_receive, args=(s,)).start()
                print(f"Connected to {host}:{port}")
            except:
                print(f"Failed to connect to {peer}")

    while True:
        try:
            cmd = input(idendity)
            if cmd == "/exit":
                print("Closing connections and exiting...")
                is_running = False
                with lock:
                    for conn in connections:
                        try:
                            conn.close()
                        except:
                            pass
                    connections.clear()
                server_thread.join(timeout=2)
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