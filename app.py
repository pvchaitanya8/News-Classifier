from flask import Flask, render_template, request, jsonify
import pickle
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from newspaper import Article
import pymongo
import datetime

# Replace placeholders with actual values
MONGO_URI = "mongodb://localhost:*****"
client = pymongo.MongoClient(MONGO_URI)
db = client["news_classifier_db"]
collection = db["articles"]

class_labels = ["World News", "Sports News", "Business News", "Sci/Tech News"]

vectorizer = TfidfVectorizer()
df = pd.read_csv(r"data\test.csv")
X = vectorizer.fit_transform(df["Description"])
loaded_model = pickle.load(open(r"model\my_svm_model.pkl", "rb"))

app = Flask(__name__)

def predict_category(new_article):
    global vectorizer, loaded_model
    if "http" in new_article:
        try:
            article = Article(new_article, user_agent="your_user_agent")
            article.download()
            article.parse()
            new_article_text = article.text
        except Exception as e:
            print(f"Error extracting text from URL: {e}")
            return None
    else:
        new_article_text = new_article

    new_article_features = vectorizer.transform([new_article_text])
    prediction = loaded_model.predict(new_article_features)[0]

    try:
        res = class_labels[int(prediction)-1]
        store_article(new_article_text, new_article if "http" in new_article else None, res, datetime.datetime.now())
        return res
    except IndexError:
        print(f"Invalid prediction: {prediction}")
        return "Error: Unexpected prediction result."

def store_article(text, url, category, timestamp):
    article = {
        "text": text,
        "url": url,
        "category": category,
        "timestamp": timestamp,
    }
    collection.insert_one(article)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    if request.method == "POST":
        article_text = request.form["article_text"]

        if not article_text:
            return render_template("index.html", error="Please enter some text.")

        try:
            prediction = predict_category(article_text)
            return render_template("result.html", prediction=prediction)
        except Exception as e:
            return render_template("index.html", error="An error occurred: " + str(e))

    return render_template("index.html")

@app.route("/api/classify", methods=["POST"])
def classify_article():
    data = request.get_json()
    text = data.get("text")
    url = data.get("url")

    if not text and not url:
        return jsonify({"error": "Please provide either text or URL."}), 400

    prediction = predict_category(text or url)

    if prediction:
        return jsonify({"category": prediction})
    else:
        return jsonify({"error": "Failed to predict category."}), 500

@app.route("/api/articles/<category>", methods=["GET"])
def get_articles_by_category(category):
    articles = collection.find({"category": category})
    return jsonify({"articles": [article for article in articles]})

if __name__ == "__main__":
    app.run(debug=True)
