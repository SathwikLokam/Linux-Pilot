import socket
import json


HOST = '127.0.0.1' #hear i used my local system,making changes specific to linux host ip address that run cmd_receiver.py
PORT = 65432   #this just ephimeral port number,i want to use 1234 port for my project for later case

def handle_message(data):
    try:
        message = json.loads(data)
        print(f"Received message: {message}")
        # Example: Handle a request or respond
        response = {"status": "success", "message": "Hello from the server!"}
        return json.dumps(response)
    except json.JSONDecodeError:
        return json.dumps({"status": "error", "message": "Invalid message format"})

def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"Server listening on {HOST}:{PORT}")
        conn, addr = s.accept()
        with conn:
            print(f"Connected by {addr}")
            data = conn.recv(1024)
            if data:
                print(f"Received data: {data}")
                response = handle_message(data.decode('utf-8'))
                conn.sendall(response.encode('utf-8'))

if __name__ == "__main__":
    start_server()
