import sqlite3
import pandas as pd

from ner_model import model, get_unique_results
from ws_nbc import web_scrape

def create_sql_server():
    conn = sqlite3.connect('ner_database')
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS articles (NAME, ORGANIZATION, LOCATION)')
    conn.commit()
    return conn, c

def ner_to_df(article):
    dict1 = article['Article Content'][0]
    df = pd.DataFrame(dict([(k,pd.Series(v)) for k,v in dict1.items()]))
    return df

def dict_to_df(ner_unique):
    return pd.DataFrame(dict([(k,pd.Series(v)) for k,v in ner_unique.items()]))

if __name__ == '__main__':
    url = 'https://www.nbcnews.com/'
    article_url = 'https://www.nbcnews.com/politics/biden-says-considering-gas-tax-holiday-rcna34419'

    spacy_ner = model()
    nbc_article = web_scrape(article_url)

    # For a single article
    article = nbc_article.scrape_news_article()
    model_out = spacy_ner.ner(article.get('article content'))
    ner_unique = get_unique_results(model_out)
    df = dict_to_df(ner_unique)

    conn, c = create_sql_server()

    df.to_sql('articles', conn, if_exists='replace', index = False)

    sql_input = ''
    while sql_input != 'quit':
        sql_input = input("Input search query: ")

        c.execute(sql_input)

        for row in c.fetchall():
            print (row)