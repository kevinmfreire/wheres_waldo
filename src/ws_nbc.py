# -*- coding: utf-8 -*-
"""WS_NBC.ipynb
# Web Scrapping NBC News
"""
import requests
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd

## Obtain List of news from the coverpage
def clean_text(contents):
    body= contents.replace('n', ' ')
    body= contents.replace('t', ' ')
    body= contents.replace('r', ' ')
    body= contents.replace('\xa0', ' ')
    return body

class web_scrape:
    '''
    This web scrapping class allows you to scrape a single news article of your choice,
    or you can scrape multiple news article and store it to a dataframe.  You need to initialize the 
    class with the specific url and depending on your choice run to scrape one article or more than one. 
    Keep in mind that the scrape_N_articles() also allows you to scrape one article, however it is a
    random article from the landing page of NBC News.
    '''
    def __init__(self, url):
        self.url = url
        self.request = requests.get(self.url)

        # We'll save in coverpage the cover page content
        self.coverpage = self.request.content

        # Soup creation
        self.soup = BeautifulSoup(self.coverpage, 'html5lib')

    def scrape_news_article(self):
        x = self.soup.find_all('p', {'class':['','endmark']})

        # Unifying the paragraphs
        list_paragraphs = []
        for p in np.arange(0, len(x)):
            paragraph = x[p].get_text()
            list_paragraphs.append(paragraph)
            final_article = " ".join(list_paragraphs)
        clean_article = clean_text(final_article)

        article_dict = {'article link': self.url, 'article content': clean_article}

        return article_dict

    def scrape_N_articles(self, num_articles=1):
        # News identification
        coverpage_news = []
        for tag in self.soup.find_all('h2', class_='styles_headline__ice3t'):
            for anchor in tag.find_all('a'):
                coverpage_news.append(anchor)

        print('Number of articles found: {}'.format(len(coverpage_news)))

        ## Let's extract the text from the article
        # Empty lists for content, links and titles
        news_contents = []
        list_links = []
        list_titles = []

        for n in np.arange(0, num_articles):
                
            # Getting the link of the article
            link = coverpage_news[n]['href']
            list_links.append(link)
            
            # Getting the title
            title = coverpage_news[n].get_text()
            list_titles.append(title)
            
            # Reading the content (it is divided in paragraphs)
            article = requests.get(link)
            article_content = article.content
            soup_article = BeautifulSoup(article_content, 'html5lib')
            x = soup_article.find_all('p', {'class':['','endmark']})
            
            # Unifying the paragraphs
            list_paragraphs = []
            for p in np.arange(0, len(x)):
                paragraph = x[p].get_text()
                list_paragraphs.append(paragraph)
                final_article = " ".join(list_paragraphs)
                
            # Clean the content from any additional html tags
            clean_article = clean_text(final_article)
            news_contents.append(clean_article)

        # df_show_info
        nbc_articles = pd.DataFrame({
            # 'Article Title': list_titles,
            'Article Link': list_links,
            'Article Content': news_contents})

        return nbc_articles

if __name__ == '__main__':
    
    # url definition
    url = 'https://www.nbcnews.com/'
    article_url = 'https://www.nbcnews.com/politics/biden-says-considering-gas-tax-holiday-rcna34419'
    save_path = '../data/ws_data/'
    number_of_articles = 5

    # Scrape a single article
    nbc_article = web_scrape(article_url)
    article = nbc_article.scrape_news_article()

    # Scrape N articles
    nbc_news = web_scrape(url)
    nbc_articles = nbc_news.scrape_N_articles(num_articles=number_of_articles)

    # Save to dataframe for visibility of output
    nbc_articles.to_csv(save_path + 'ws_nbc.csv')