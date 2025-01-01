from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import pandas as pd
import importlib
def find_relevant_keyword(csv_filename, input_sentence):
    df = pd.read_csv(csv_filename)
    sentences = df['Sentence'].tolist()
    keywords = df['Command'].tolist()
    model = SentenceTransformer('all-MiniLM-L6-v2')
    input_sentence_embedding = model.encode([input_sentence])
    sentence_embeddings = model.encode(sentences)
    similarities = cosine_similarity(input_sentence_embedding, sentence_embeddings)
    most_relevant_idx = np.argmax(similarities)
    most_relevant_keyword = keywords[most_relevant_idx]
    similarity_score = similarities[0][most_relevant_idx]
    return most_relevant_keyword, similarity_score

csv_filename = 'sentences_dict_with_pandas.csv'

while True:
    input_sentence = input("Enter a sentence (or type 'exit' to quit): ")
    
    if input_sentence.lower() == "exit":
        print("Exiting the program.")
        break
    
    most_relevant_keyword, similarity_score = find_relevant_keyword(csv_filename, input_sentence)
    
    if similarity_score < 0.4:
        print("I didn't get you. Could you please rephrase?")
    else:
        print(f"Most relevant keyword: {most_relevant_keyword}")
        print(f"Similarity score: {similarity_score:.4f}")
    
    obj=importlib.import_module("Handlers."+most_relevant_keyword).Handler(input_sentence)
    print(obj.fill())