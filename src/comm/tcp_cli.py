import socket

class TCPClient:
    def __init__(self, host='localhost', port=6000, payload_size=4):
        self.host = host
        self.port = port
        self.payload_size = payload_size
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        try:
            self.client_socket.connect((self.host, self.port))
            print(f"Connected to {self.host} on port {self.port}")
        except Exception as e:
            print(f"Error connecting to server: {e}")

    def send_data(self, data):
        try:
    
            if len(data) != self.payload_size:
                print("Data must be exactly", self.payload_size, "bytes long.")
                return
            self.client_socket.sendall(data)
            print("Data sent:", data)
        except Exception as e:
            print(f"Error sending data: {e}")

    def receive_response(self):
        try:
            response = self.client_socket.recv(self.payload_size)
            if response:
                print("Received response:", response)
                return response
            else:
                print("No response received.")
        except Exception as e:
            print(f"Error receiving response: {e}")

    def close(self):
        self.client_socket.close()
        print("Connection closed.")

if __name__ == "__main__":
    client = TCPClient(host='localhost', port=7000, payload_size=4)
    client.connect()
    client.send_data()
    client.receive_response()
    client.close()
