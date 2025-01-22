import json
import os

import sys
sys.path.append('../') # adding the path of the project to access


class Handler:
    arguments = dict()
    frame = {}
    arguments=[]
    
    def __init__(self, arguments, json_file):
        self.arguments = arguments  # Processed Input from the Fetcher
        print(f"request : {arguments} , json_file : {json_file}")
        # Load the correct frame from the specified JSON file
        self.load_from_json(json_file)
        
        self.autoFill()  # Fills the slots in frame if there exist arguments in it

    def autoFill(self):
        """ Automatically fill in values if needed. """
        # In case we want to pre-fill some fields based on initial input or pre-defined logic
        pass

    def fill(self):
        """ Fill all the placeholders in the frame, and generate the command. """
        if "arguments" not in self.frame:
            return ["Error: No 'arguments' key found in the frame.", 0]

        # For each argument, ask for user input if it's not filled yet
        for arg, (prompt, value) in self.frame["arguments"].items():
            if value is None:
                if self.arguments.get(arg, []):
                    self.frame["arguments"][arg][1] = self.arguments[arg][0]  # Using the first element from self.arguments
                else:
                    user_input = input(f"{prompt}: ")
                    if user_input not in ["exit", "quit"]:
                        self.frame["arguments"][arg][1] = user_input
                    else:
                        return ["The creation of payload is terminated", 0]  # 0 indicates failure to create payload
        return self.generate_command(), 1  # Return the command with status

    def generate_command(self):
        """ Generate the command dynamically based on the representation and arguments. """
        # Copy the representation and replace placeholders with actual values
        command = self.frame["representation"]
        
        # Replace each placeholder in the representation with the user input
        for arg, (prompt, value) in self.frame["arguments"].items():
            if value is not None:
                command = command.replace(f"<{arg}>", value)
        
        return command

    def load_from_json(self, filename):
        """ Load the command frame dictionary from the specified JSON file. """
        print(f">>>>>>>>> {filename}")
        
        if not os.path.exists(filename):
            print(f"Error: File '{filename}' not found.")
            self.frame = {}
            return

        try:
            with open(filename, 'r') as json_file:
                self.frame = json.load(json_file)
            print(f"Command frame loaded from {filename}")
            
            # Check if 'arguments' key is present
            if "arguments" not in self.frame:
                print("Error: 'arguments' key not found in the frame.")
                self.frame = {}
            
        except FileNotFoundError:
            print(f"Error: File '{filename}' not found.")
            self.frame = {}
        except json.JSONDecodeError:
            print(f"Error: Failed to decode JSON from file '{filename}'.")
            self.frame = {}


# Main script logic to select the frame dynamically based on the command
if __name__ == "__main__":  # this method only for testing ,it is only called when i run this file

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
