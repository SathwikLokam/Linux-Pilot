"""this code is to be works on the side of user"""
"""as my per my configuration i port forwarded ip address i.e. 192.168.130.149 which is address of linux in vmware"""

import socket

def client():
    # Create a TCP socket object
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Connect to the server running on the Linux VM, but we use 'localhost' for NAT port forwarding
    # The traffic on port 12345 from the Windows host will be forwarded by VMware's NAT to the VM
    # 'localhost' (or '127.0.0.1') refers to the Windows host machine, and VMware will handle the forwarding
    # '12345' is the port on which the server in the Linux VM is listening
    # Important: Ensure that the NAT port forwarding rule is set correctly in VMware (host port 12345 -> VM port 12345)
    client_socket.connect(('192.168.130.149', 12345))  # Connect to 192.168.130.149 because of NAT port forwarding
    #if you need a test both terminals in same host change it from 192.168.130.149 to localhost
    
    # Prompt the user to enter a message to send to the server
    message = input("Enter a message to send to the server: ")
    
    #Send the message to the server (encoded as bytes)
    client_socket.sendall(message.encode())  # Send the input message to the server
    
    # Receive the echoed message back from the server
    data = client_socket.recv(1024)  # Receive the response (up to 1024 bytes)
    
    #print the message received from the server (server should echo the same message)
    print(f"Received from server: {data.decode()}")  # Decode and print the received data
    
    # Close the socket after communication is done
    client_socket.close()

if __name__ == "__main__":
    client()  # Call the client function to run the client code
