from flask import Flask, render_template, request, jsonify
import model_handler as mh
app = Flask(__name__)

# Define some basic responses for the chatbot
responses = {
    "hello": "Hi there! How can I help you today?",
    "how are you": "I'm just a bot, but I'm doing great! How about you?",
    "bye": "Goodbye! Have a great day!",
    "default": "Sorry, I didn't quite understand that."
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    user_message = request.form['message'].lower()
    model_prediction=mh.get_prediction(user_message)
    # ------> filtration module - it checks whether it is payload creation query or genaral chat,
    # if payload creation then excution points to other funtion that attempts to exucute the payload if not pass
    return jsonify({'response':model_prediction})

if __name__ == '__main__':
    app.run(debug=True)
