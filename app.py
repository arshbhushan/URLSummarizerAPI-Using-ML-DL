from flask import Flask, render_template, request, jsonify
from newspaper import Article
import nltk
import time
from werkzeug.utils import url_quote
import os

nltk.download('punkt')

app = Flask(__name__)

def download_with_retry(url, max_retries=3):
    for i in range(max_retries):
        try:
            article = Article(url)
            article.download()
            article.parse()
            article.nlp()
            return article
        except Exception as e:
            print(f"Failed attempt {i + 1}: {e}")
            time.sleep(1)  # Add a delay before retrying

    raise Exception("Failed to download article after multiple retries")

def extract_and_summarize(url):
    article = download_with_retry(url)
    
    title = article.title
    authors = article.authors
    publish_date = article.publish_date
    summary = article.summary

    return {
        'title': title,
        'authors': authors,
        'publish_date': publish_date,
        'summary': summary
    }

@app.route('/process', methods=['POST'])
def process():
    if request.method == 'POST':
        url = request.form['url']

        result = extract_and_summarize(url)

        # Return JSON response
        return jsonify(result)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
