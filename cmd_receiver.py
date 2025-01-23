"""this is code that runs in the linux server or general system"""
"""but there no need of changing code for the case of windows i.e. independent of os"""

import socket

def server():
    # Set up the server to listen on localhost and port 12345
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("0.0.0.0", 12345))
    server_socket.listen(1)
    print("Server is listening on port 12345...")

    # Accept a connection from the client
    client_socket, client_address = server_socket.accept()
    print(f"Connection established with {client_address}")

    while True:
        # Receive the message from the client
        data = client_socket.recv(1024).decode('utf-8')
        
        if not data:
            break
        
        print(f"Received from client: {data}")
        
        # Send the same message back to the client
        client_socket.send(data.encode('utf-8'))
    
    # Close the connection
    client_socket.close()
    server_socket.close()

if __name__ == "__main__":
    server()
