from flask import Flask, request, render_template
from spacy import displacy
from flaskext.markdown import Markdown
import sys

sys.path.append("src/")

from src import ner_model, ws_nbc

app = Flask(__name__)
nlp = ner_model.Model()
Markdown(app)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict',methods=['POST'])
def predict():
    """Grabs the input values and uses them to make prediction"""
    article_url = request.form['url']
    nbc_article = ws_nbc.WebScrape(article_url)
    article = nbc_article.scrape_news_article()
    title = article.get('article title')
    model_out = nlp.ner(article.get('article content'))
    html = displacy.render(model_out, style='ent')

    # return render_template('index.html', prediction_text=f'Your Article Link "{article_url}" has following NER {html}.')
    return render_template('results.html', article_title=title, prediction_text=html)

if __name__=="__main__":
    app.run(host="0.0.0.0", port=8080)