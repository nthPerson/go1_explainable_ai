#!/usr/bin/env python3

import socket

class TCPServer:
    def __init__(self, host='0.0.0.0', port=6000, callback=(), payload_size=4):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.callback = callback
        self.payload_size = payload_size

    def bind(self):
        self.server_socket.bind((self.host, self.port))
        print(f"Server bound to {self.host}:{self.port}")

    def listen(self):
        self.server_socket.listen(1)
        print(f"Server listening on {self.host}:{self.port}")

    def accept_connections(self):
        try:
            connection, client_address = self.server_socket.accept()
            print(f"Connection from {client_address}")
            self.handle_connection(connection)
        except Exception as e:
            print(f"Error accepting connections: {e}")
        finally:
            self.close()

    def handle_connection(self, connection):
        try:
            while True:
                data = connection.recv(self.payload_size)
                if not data:
                    print("No data received, closing connection.")
                    break
                if len(data) == self.payload_size:
                    self.callback(data)
                else:
                    print("Received incomplete data.")
                    break
        except Exception as e:
            print(f"Connection handling error: {e}")
        finally:
            connection.close()

    def run(self):
        try:
            self.bind()
            self.listen()
            self.accept_connections()
        except KeyboardInterrupt:
            print(f"Server shutdown by user, freeing port {self.port}")

    def close(self):
        self.server_socket.close()
        print("Server closed.")

if __name__ == "__main__":
    server = TCPServer()
    server.run()
