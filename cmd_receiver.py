# this is file runs on side of the linux that run command


from flask import Flask, request, jsonify
import subprocess

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
            return jsonify({"output": result.stdout}), 200
        else:
            return jsonify({"error": result.stderr}), 500

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=12345)
