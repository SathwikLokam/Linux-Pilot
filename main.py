from flask import Flask, render_template, request, jsonify
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import pandas as pd
import subprocess
import Fetcher
import Handlers.Handler_control as Handler
import cmd_sender


# Function to get IP, Port and activate listeners
def getIp_Port_and_activateListeners():
    setup = input("Do you want to connect to the external linux system(Yes/No): ")
    if setup.lower() == "yes" or setup.lower() == "":
        ip = input("Enter the Ip address to connect  : ")
        port = input("Enter the port to connect : ")
        print("\033[92mTrying to connect External Linux\033[0m")
        return ip, port

    # Start cmd_receiver.py in the background without blocking (non-interactive)
    subprocess.Popen(["python", "cmd_receiver.py"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print("\033[92mUsing internal Linux and Activating internal Listeners\033[0m")
    return '127.0.0.1', 4444


app = Flask(__name__)
ip, port = getIp_Port_and_activateListeners()
message_sender = cmd_sender.HostSetup(ip, port)  # arguments are based on NAT and VMware config
modelCall = True
handler_obj = None  # Initialize as None


# Handler_interface to extend functionality of the Handler class
class Handler_interface(Handler.Handler):
    def __init__(self, message, hndlr):
        ftc_dict = Fetcher.Fetch(message).get_all()
        print("Handler_interface initialized.")
        super().__init__(ftc_dict, hndlr)


# Reset function to clear variables
def reset():
    global handler_obj, frame, modelCall
    handler_obj = None  # reset to None
    modelCall = True
    frame = None


# Find relevant keyword using cosine similarity
def find_relevant_keyword(csv_filename, input_sentence):
    df = pd.read_csv(csv_filename)
    sentences = df['description'].tolist()
    keywords = df['keyword'].tolist()

    model = SentenceTransformer('all-MiniLM-L6-v2')
    input_sentence_embedding = model.encode([input_sentence])
    sentence_embeddings = model.encode(sentences)
    similarities = cosine_similarity(input_sentence_embedding, sentence_embeddings)

    most_relevant_idx = np.argmax(similarities)
    most_relevant_keyword = keywords[most_relevant_idx]
    similarity_score = similarities[0][most_relevant_idx]

    return most_relevant_keyword, similarity_score


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/ask", methods=["POST"])
def ask():
    message = request.form["message"]
    global handler_obj, frame, modelCall
    if modelCall:
        reset()
        most_relevant_keyword, similarity_score = find_relevant_keyword('mappings.csv', message)
        
        if similarity_score < 0.4:
            return jsonify({'response': "I didn't get you. Could you please rephrase?"})
        
        modelCall = False
        handler_obj = Handler_interface(message, "Handlers/frames/" + most_relevant_keyword + ".json")
        frame = handler_obj.load_from_json()
        print(frame)
        message = ""  # Reset message after processing

    try:
        for arg, (prompt, value) in frame["arguments"].items():
            if not message:
                return jsonify({'response': prompt})
            if value is None:
                if handler_obj.arguments.get(arg, []):
                    handler_obj.frame["arguments"][arg][1] = handler_obj.arguments[arg][0]
                else:
                    if message not in ["exit", "quit"]:
                        handler_obj.frame["arguments"][arg][1] = message
                        message = ""
                    else:
                        reset()
                        return jsonify({'response': "The creation of payload is terminated"})

        print("Created frame:", handler_obj.frame)
        response = message_sender.send_and_execute(handler_obj.generate_command())
    except ModuleNotFoundError:
        response = f"No handler found for the keyword: {most_relevant_keyword}"

    reset()  # Reset after handling
    return jsonify({'response': response.replace("\n", "<br>")})


if __name__ == "__main__":
    app.run(debug=False)