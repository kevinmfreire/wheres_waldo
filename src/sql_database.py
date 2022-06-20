import sqlite3
import pandas as pd

from ner_model import spacy_ner, get_ner_for_all
from ws_nbc import web_scraper

def create_sql_server():
    conn = sqlite3.connect('test_database')
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS articles (Article link, NER results)')
    conn.commit()
    return conn, c

def creat_article_content_df(article):
    dict1 = article['Article Content'][0]
    df = pd.DataFrame(dict([(k,pd.Series(v)) for k,v in dict1.items()]))
    return df

if __name__ == '__main__':
    url = 'https://www.nbcnews.com/'

    spacner = spacy_ner()

    article = web_scraper(url)

    output = get_ner_for_all(article, spacner)

    conn, c = create_sql_server()

    df = creat_article_content_df(output)
    df.to_sql('articles', conn, if_exists='replace', index = False)

    c.execute('''  
    SELECT * FROM articles
            ''')

    for row in c.fetchall():
        print (row)