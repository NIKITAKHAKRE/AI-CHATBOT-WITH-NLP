from flask import Flask, request, jsonify, render_template
import nltk
import random
import string
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Download necessary NLTK data
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('omw-1.4')

app = Flask(__name__)

# Sample corpus
CORPUS = """
Hello! I am your AI chatbot.
I can help answer questions about Python, AI, or general topics.
Python is a high-level programming language.
Natural Language Processing is a field of AI that helps computers understand human language.
You can use NLTK or spaCy for NLP tasks.
AI stands for Artificial Intelligence.
How can I help you today?
"""

lemmer = WordNetLemmatizer()

def LemTokens(tokens):
    return [lemmer.lemmatize(token.lower()) for token in tokens if token not in string.punctuation]

def LemNormalize(text):
    return LemTokens(nltk.word_tokenize(text.lower()))

GREETING_INPUTS = ("hello", "hi", "greetings", "sup", "what's up", "hey")
GREETING_RESPONSES = ["Hi there!", "Hello!", "Hey!", "Hi! How can I assist you?"]

def greet(sentence):
    for word in sentence.split():
        if word.lower() in GREETING_INPUTS:
            return random.choice(GREETING_RESPONSES)

def generate_response(user_input):
    user_input = user_input.lower()
    sentence_list = nltk.sent_tokenize(CORPUS)
    sentence_list.append(user_input)

    vectorizer = TfidfVectorizer(tokenizer=LemNormalize, stop_words='english')
    tfidf = vectorizer.fit_transform(sentence_list)
    similarity_scores = cosine_similarity(tfidf[-1], tfidf[:-1])
    idx = similarity_scores.argsort()[0][-1]
    flat = similarity_scores.flatten()
    flat.sort()
    req_tfidf = flat[-1]

    if req_tfidf == 0:
        return "I'm sorry, I don't understand that."
    else:
        return sentence_list[idx]

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/get", methods=["GET"])
def get_bot_response():
    user_input = request.args.get("msg")
    if greet(user_input):
        return greet(user_input)
    else:
        return generate_response(user_input)

if __name__ == "__main__":
    app.run(debug=True)
