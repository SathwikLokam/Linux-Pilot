

import requests

class HostSetup:
    def __init__(self, host='127.0.0.1', port=4444):
        # Initialize the IP address and port
        self.ip = host
        self.port = port

    def send_and_execute(self,command):
        # Define the API endpoint
        url = f"http://{self.ip}:{self.port}/execute"  # Ensure the URL is valid


        # Prepare the data to send to the server (in JSON format)
        data = {"command": command}

        # Send the POST request to the server
        response = requests.post(url, json=data)

        # Check the response from the server
        if response.status_code == 200:
            # Success - print the output from the command
            print(f"Server Response: {response.json().get('output')}")
            return response.json().get('output')
        else:
            # Error - print the error message
            print(f"Server Error: {response.json().get('error')}")

if __name__ == "__main__":
    # Create an instance of HostSetup
    # the following arguments are based on my configuration of NAT and VMware
    host_setup = HostSetup(host='192.168.130.149', port=12345)  # Adjust the host and port as needed
    # Call the method to send 
    # a command to the server
    host_setup.send_and_execute(input("Enter the command to test: "))
