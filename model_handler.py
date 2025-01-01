import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
import joblib


model = joblib.load('attack_model_svm.joblib')
vectorizer = joblib.load('vectorizer_svm.joblib')

# Ensure necessary NLTK resources are downloaded
# Uncomment if needed: 
# nltk.download('punkt')
# nltk.download('stopwords')
# nltk.download('wordnet')

# Function to load the saved model and vectorizer

# Text Preprocessing Function
def preprocess_text(text):

    text = text.lower()
    

    text = re.sub(r'[^a-z\s]', '', text)
    

    tokens = word_tokenize(text)
    
    stop_words = set(stopwords.words('english'))
    filtered_tokens = [word for word in tokens if word not in stop_words]
    
    lemmatizer = WordNetLemmatizer()
    lemmatized_tokens = [lemmatizer.lemmatize(word) for word in filtered_tokens]
    
    return ' '.join(lemmatized_tokens)  # Return as a single preprocessed string

# Function to make predictions
def predict_meaning(description, model, vectorizer):

    preprocessed_description = preprocess_text(description)
    

    vectorized_description = vectorizer.transform([preprocessed_description])
    

    prediction = model.predict(vectorized_description)
    return prediction[0]


def get_prediction(test_description):


    #test_description = input("Enter description (or type 'exit' to quit): ")
    

    predicted_meaning = predict_meaning(test_description, model, vectorizer)
    return predicted_meaning
