import requests
import numpy as np
import pandas as pd
import argparse
from bs4 import BeautifulSoup

class WebScrape:
    '''
    This web scrapping class allows you to scrape a single news article of your choice,
    or you can scrape multiple news article and store it to a dataframe.  You need to initialize the 
    class with the specific url and depending on your choice, run to scrape one article or more than one. 
    Keep in mind that the scrape_N_articles() also allows you to scrape one article, however it is a
    random article from the landing page of NBC News.

    def __init__()              ---->   Initialize requests and obtains content from landing page of URL

    def scrape_news_article()   ---->   Web Scrapping of a single news article

    def scrap_N_articles()      ---->   Web Scrapping of multipl articles of the NBC home page

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

        article_dict = {'article link': self.url, 'article content': final_article}

        return article_dict

    def scrape_n_articles(self, num_articles=1):
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
            final_article = ""
            for p in np.arange(0, len(x)):
                paragraph = x[p].get_text()
                list_paragraphs.append(paragraph)
                final_article = " ".join(list_paragraphs)
                
            news_contents.append(final_article)

        # df_show_info
        nbc_articles = pd.DataFrame({
            # 'Article Title': list_titles,
            'article link': list_links,
            'article content': news_contents})

        return nbc_articles

if __name__ == '__main__':

    parser= argparse.ArgumentParser()
    parser.add_argument('--nbc_url', type=str, default='https://www.nbcnews.com/')
    parser.add_argument('--nbc_article_url', type=str, default='https://www.nbcnews.com/politics/biden-says-considering-gas-tax-holiday-rcna34419')
    parser.add_argument('--save_path', type=str, default='../data/ws_data/')
    parser.add_argument('--num_articles', type=int, default=5)
    args = parser.parse_args()

    # Scrape a single article
    nbc_article = WebScrape(args.nbc_article_url)
    article = nbc_article.scrape_news_article()

    # Scrape N articles
    nbc_news = WebScrape(args.nbc_url)
    nbc_articles = nbc_news.scrape_n_articles(num_articles=args.num_articles)

    # Save to dataframe for visibility of output
    nbc_articles.to_csv(args.save_path + 'ws_nbc.csv')