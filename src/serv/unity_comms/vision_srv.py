#!/usr/bin/env python3

from yolo_clnt import detect
import socket

def callback(conn):
    response = detect()
    conn.sendall(bytes(response))
    conn.shutdown(socket.SHUT_WR)

def print_shutdown():
    SHUTDOWN_MSG = "User wants to shutdown, cleaning up resources"
    print(SHUTDOWN_MSG)

def handle_request(conn, sock):
    try:
        while True:
            data = conn.recv(1024)
            if not data:
                break
            callback(conn)
    except KeyboardInterrupt:
        print_shutdown()
        conn.shutdown(socket.SHUT_RDWR)
        sock.shutdown(socket.SHUT_RDWR)
    finally:
        conn.close()
        sock.close()

def setup_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('0.0.0.0', 7002))
    server_socket.listen(1)
    print("Vision service is listening on 0.0.0.0:7002...")
    return server_socket

def connect_sock(server_socket):
    try:
        conn, addr = server_socket.accept()
        print(f"Connected by {addr}")
        return conn
    except KeyboardInterrupt:
        print("Closed before connection could be made")
        exit()
        
def main():
    server_socket = setup_server()
    conn = connect_sock(server_socket)
    handle_request(conn, server_socket)
    server_socket.close()

if __name__ == "__main__":
    main()