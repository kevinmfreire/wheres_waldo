import sqlite3
import pandas as pd
import sys
sys.path.append('./src/')
import ws_nbc, ner_model

'''
This script is only optimized to handle one news article from NBC News.
User Inputs: 
                article url = Copy and paste an NBC news article URL
                sql query:
                    select * from article
                    select NAME from article
                    select ORGANIZATION from article
                    select LOCATION from article

outputs:
                result query
'''

def create_sql_server():
    conn = sqlite3.connect('ner_database')
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS article (NAME, ORGANIZATION, LOCATION)')
    conn.commit()
    return conn, c

def ner_to_df(article):
    dict1 = article['Article Content'][0]
    df = pd.DataFrame(dict([(k,pd.Series(v)) for k,v in dict1.items()]))
    return df

def dict_to_df(ner_unique):
    return pd.DataFrame(dict([(k,pd.Series(v)) for k,v in ner_unique.items()]))

if __name__ == '__main__':

    article_url = input("Input NBC News article url: ")

    spacy_ner = ner_model.model()
    nbc_article = ws_nbc.web_scrape(article_url)

    article = nbc_article.scrape_news_article()
    model_out = spacy_ner.ner(article.get('article content'))
    ner_unique = ner_model.get_unique_results(model_out)
    df = dict_to_df(ner_unique)

    conn, c = create_sql_server()

    df.to_sql('article', conn, if_exists='replace', index = False)

    sql_input = ''
    while sql_input != 'quit':
        sql_input = input("Input search query: ")

        c.execute(sql_input)

        for row in c.fetchall():
            print (row)