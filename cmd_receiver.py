import socket
import json

HOST = '127.0.0.1'
PORT = 65432

def send_message(message):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        message_json = json.dumps(message)
        s.sendall(message_json.encode('utf-8'))
        data = s.recv(1024)
        print(f"Received from server: {data.decode('utf-8')}")

if __name__ == "__main__":
    message = {"type": "request", "data": {"text": "Hello, server!"}}
    send_message(message)
