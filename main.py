from flask import Flask, render_template, request, jsonify
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import pandas as pd
import importlib
import Fetcher
import Handlers.Handler_control as Handler

app = Flask(__name__)

<<<<<<< HEAD
<<<<<<< Updated upstream
=======
=======
>>>>>>> fe13c5b6ae8ed4da8c09bb0d0f397bc6c8fea7dd
class Handler_interface(Handler.Handler):  # extended functionality 
    def __init__(self,message,hndlr):
        ftc_dict=Fetcher.Fetch(message).get_all()   # getting all the fetched arguments from the fetcher
        print("Handler_interface initialized.")
        super().__init__(ftc_dict,hndlr)


<<<<<<< HEAD
>>>>>>> Stashed changes
=======



>>>>>>> fe13c5b6ae8ed4da8c09bb0d0f397bc6c8fea7dd
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
    
    # Find the most relevant keyword and similarity score
    most_relevant_keyword, similarity_score = find_relevant_keyword('mappings.csv', message)
    
    if similarity_score < 0.4:
        response = "I didn't get you. Could you please rephrase?"
    else:
        try:
            # Dynamically import the handler module
            handler_obj = Handler_interface(message,"Handlers/frames/"+most_relevant_keyword+".json")
            response = handler_obj.fill()  # Call the fill method and get the response
        except ModuleNotFoundError:
            response = f"No handler found for the keyword: {most_relevant_keyword}"

    return jsonify({'response': response})

if __name__ == "__main__":
    app.run(debug=True)