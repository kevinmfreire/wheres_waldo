import sqlite3
import pandas as pd
import sys
import argparse
sys.path.append('src/')
from src import ws_nbc, ner_model

'''
This script has been optimized to handle one or more news article from NBC News.

User Arguments:
                --multi_article (Default = False)
                --num_articles (if multi_article is set to True you can place the amount of articles you want to extract)

User Inputs:
                Article URL if multi_article is False
                SQL commands
                        SELECT * FROM article
                        SELECT NAME FROM article
                        SELECT ORGANIZATION FROM article
                        SELECT LOCATION FROM article
                        ... 

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
    df = pd.DataFrame(dict([(k,pd.Series(v)) for k,v in article.items()]), dtype=object)
    return df

def dict_to_df(ner_unique):
    return pd.DataFrame(dict([(k,pd.Series(v)) for k,v in ner_unique.items()]))

if __name__ == '__main__':

    parser= argparse.ArgumentParser()
    parser.add_argument('--multi_article', type=bool, default=False)
    parser.add_argument('--num_articles', type=int, default=5)
    args = parser.parse_args()

    spacy_ner = ner_model.Model()

    if args.multi_article:
        nbc_news = 'https://www.nbcnews.com/'
        nbc_article = ws_nbc.WebScrape(nbc_news)
        article = nbc_article.scrape_n_articles(num_articles=args.num_articles)
        print("Scraping {} articles from NBC News Webpage".format(args.num_articles))
        model_out = spacy_ner.get_ner_for_all(article)
        df = pd.DataFrame()
        for i in range(0,len(model_out)):
            article_df = ner_to_df(model_out['article content'][i])
            df = pd.concat([df, article_df])
    else:
        article_url = input("Input NBC News article url: ")
        nbc_article = ws_nbc.WebScrape(article_url)
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