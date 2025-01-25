from flask import Flask, render_template, request, jsonify
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import pandas as pd
import importlib
import Fetcher
import Handlers.Handler_control as Handler
import cmd_sender

app = Flask(__name__)
message_sender=cmd_sender.HostSetup("192.168.130.149","12345")  # arguments are based on my configuration of NAT and VMware
modelCall=True
handler_obj=object()

class Handler_interface(Handler.Handler):  # extended functionality 
    def __init__(self,message,hndlr):
        ftc_dict=Fetcher.Fetch(message).get_all()   # getting all the fetched arguments from the fetcher
        print("Handler_interface initialized.")
        super().__init__(ftc_dict,hndlr)


def reset(): #resets all the variables and instances
    global handler_obj
    global frame
    global modelCall
    handler_obj=object()
    modelCall=True
    frame=None



def find_relevant_keyword(csv_filename, input_sentence):
    df = pd.read_csv(csv_filename)
    sentences = df['Sentence'].tolist()
    keywords = df['Command'].tolist()

    # Initialize the model
    model = SentenceTransformer('all-MiniLM-L6-v2')

    # Encode the input sentence
    input_sentence_embedding = model.encode([input_sentence])

    # Encode all sentences from the CSV
    sentence_embeddings = model.encode(sentences)

    # Calculate cosine similarities
    similarities = cosine_similarity(input_sentence_embedding, sentence_embeddings)

    # Find the index of the most relevant sentence
    most_relevant_idx = np.argmax(similarities)

    # Get the most relevant keyword and similarity score
    most_relevant_keyword = keywords[most_relevant_idx]
    similarity_score = similarities[0][most_relevant_idx]

    return most_relevant_keyword, similarity_score
    

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
        message = request.form["message"]
        global handler_obj
        global frame
        global modelCall
        if modelCall:
            reset()
            # Find the most relevant keyword and similarity score
            most_relevant_keyword, similarity_score = find_relevant_keyword('mappings.csv', message)
            
            if similarity_score < 0.4:
                return jsonify({'response':"I didn't get you. Could you please rephrase?"})
            modelCall=False
            
            # Dynamically import the handler module(json)
            handler_obj = Handler_interface(message,"Handlers/frames/"+most_relevant_keyword+".json")
            frame=handler_obj.load_from_json()
            print(frame)
            message="" # made to nothing that represents 'message' is used
                        

        try:
            # For each argument, ask for user input if it's not filled yet
            for arg, (prompt, value) in frame["arguments"].items():
                if message=="":
                    return jsonify({'response': prompt})
                if value is None:
                    if handler_obj.arguments.get(arg, []):
                        handler_obj.frame["arguments"][arg][1] = handler_obj.arguments[arg][0]  # Using the first element from handler_obj.arguments
                    else:
                        if message not in ["exit", "quit"]:
                            handler_obj.frame["arguments"][arg][1] = message
                            message="" # made to nothing that represents 'message' is used
                        else:
                            reset()  
                            return jsonify({'response':"The creation of payload is terminated"})

            print("created frame : ",handler_obj.frame)
            response=message_sender.send_and_execute(handler_obj.generate_command()) # sending to linux
        except ModuleNotFoundError:
            response = f"No handler found for the keyword: {most_relevant_keyword}"

        reset() # reset
        return jsonify({'response': response})

if __name__ == "__main__":
    app.run(debug=True)

