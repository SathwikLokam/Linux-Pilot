from flask import Flask, request, jsonify
import subprocess
from time import time
import os

app = Flask(__name__)

@app.route('/execute', methods=['POST'])
def execute_command():
    try:
        # Get the command from the client
        command = request.json.get('command')
        if not command:
            return jsonify({"error": "No command provided"}), 400

        # Execute the command using subprocess
        result = subprocess.run(command, shell=True, text=True, capture_output=True)

        # Check the return code and send appropriate response
        if result.returncode == 0:
            output = result.stdout
            if "echo" in command:
            	return jsonify({"output": output})
            leng=len(output)
            # Check if output length is greater than or equal to 1000 characters
            if leng >= 1000:
                # Ensure the directory exists before creating a file
                os.makedirs('./temp', exist_ok=True)

                # Generate file name with a timestamp
                name_of_file = "./temp/file" + str(int(time())) + ".txt"

                # Write the output to the file and return the appropriate message
                with open(name_of_file, "w") as file:
                    file.write(output)

                # Return response with file path
                return jsonify({
    "output": f'<h1 style="color:rgb(43, 189, 14); font-weight: bold; font-size: 18px;">The length of the response exceeds 1000 characters, so it is saved in {name_of_file}</h1>'+f'\n\n\n\n The command is <i style="color:rgb(38, 171, 200); font-weight: bold; font-size: 18px;">{command}</i>'
}), 200
            if leng==0:
            	output=f'<h1 style="color:rgb(43, 189, 14); font-weight: bold; font-size: 18px;">Action Completed</h1>'
            return jsonify({"output": output+f'\n\n\n\n The command is <i style="color:rgb(38, 171, 200); font-weight: bold; font-size: 18px;">{command}</i>'}), 200
        else:
            return jsonify({"error": result.stderr++f'\n\n\n\n The command is <i style="color:red; font-weight: bold; font-size: 18px;">{command}</i>'}), 500

    except Exception as e:
        print(f"Error occurred: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=12345)
