import json
import os

import sys
sys.path.append('../') # adding the path of the project to access

class Handler:
    arguments = dict()
    frame = {}
    arguments=[]
    json_file=str()
    
    def __init__(self, arguments, json_file):
        self.json_file=json_file
        self.arguments = arguments  # Processed Input from the Fetcher
        print(f"request : {arguments} , json_file : {json_file}")
        # Load the correct frame from the specified JSON file
        self.load_from_json()
        
        self.autoFill()  # Fills the slots in frame if there exist arguments in it

    def autoFill(self):
        """ Automatically fill in values if needed. """
        # In case we want to pre-fill some fields based on initial input or pre-defined logic
        pass

    def generate_command(self):
        """ Generate the command dynamically based on the representation and arguments. """
        # Copy the representation and replace placeholders with actual values
        command = self.frame["representation"]
        
        # Replace each placeholder in the representation with the user input
        for arg, (prompt, value) in self.frame["arguments"].items():
            if value is not None:
                command = command.replace(f"<{arg}>", value)
        
        return command

    def load_from_json(self):
        """ Load the command frame dictionary from the specified JSON file. """
        print(f">>>>>>>>> {self.json_file}")
        
        if not os.path.exists(self.json_file):
            print(f"Error: File '{self.json_file}' not found.")
            self.frame = {}

        try:
            with open(self.json_file, 'r') as json_file:
                self.frame = json.load(json_file)
            print(f"Command frame loaded from {self.json_file}")
            
            # Check if 'arguments' key is present
            if "arguments" not in self.frame:
                print("Error: 'arguments' key not found in the frame.")
                self.frame = {}
            
        except FileNotFoundError:
            print(f"Error: File '{self.json_file}' not found.")
            self.frame = {}
        except json.JSONDecodeError:
            print(f"Error: Failed to decode JSON from file '{self.json_file}'.")
            self.frame = {}
        
        return self.frame


# Main script logic to select the frame dynamically based on the command
if __name__ == "__main__":

    command = sys.argv[1]  # The command type (e.g., 'ls', 'cat', etc.)
    frame_file = f"{command}.json"  # Dynamic path based on the command

    if not os.path.exists(frame_file):
        print(f"Error: Frame file '{frame_file}' not found.")
        sys.exit(1)

    request = "Sample request"  # Example request (could be dynamic or based on other inputs)
    handler = Handler(request, frame_file)

    # Fill the frame by getting user input
    result, status = handler.fill()

    # Output the result
    print(result)
    if status == 1:
        print("Command successfully generated!")
    else:
        print("Command creation failed.")
