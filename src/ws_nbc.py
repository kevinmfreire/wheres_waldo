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

def web_scraper(url, number_of_articles=1):
    # Request
    r1 = requests.get(url)
    print(r1.status_code)

    # We'll save in coverpage the cover page content
    coverpage = r1.content

    # Soup creation
    soup1 = BeautifulSoup(coverpage, 'html5lib')

    # News identification
    coverpage_news = []
    for tag in soup1.find_all('h2', class_='styles_headline__ice3t'):
        for anchor in tag.find_all('a'):
            coverpage_news.append(anchor)

    print('Number of articles found: {}'.format(len(coverpage_news)))

    ## Let's extract the text from the article
    # Empty lists for content, links and titles
    news_contents = []
    list_links = []
    list_titles = []

    for n in np.arange(0, number_of_articles):
            
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

    # return [list_titles, news_contents, list_links]
    return nbc_articles

def save_to_dataframe(title, content, link, save_path):
    """Let's put them into:
    * A dataset which will be the input of the models (df_features)
    * a dataset with the title and the link (df_show_info)
    """

    # df_show_info
    nbc_articles = pd.DataFrame(
        {'Article Title': title,
        'Article Content': content,
        'Article Link': link})

    print(nbc_articles)
    nbc_articles.to_csv(save_path + 'ws_nbc.csv')

if __name__ == '__main__':
    
    # url definition
    url = 'https://www.nbcnews.com/'
    save_path = '../data/ws_data/'
    number_of_articles = 5

    titles, contents, links = web_scraper(url, number_of_articles)
    
    # Save to dataframe for visibility of output
    save_to_dataframe(titles, contents, links, save_path)