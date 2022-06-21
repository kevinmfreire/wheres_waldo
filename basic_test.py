import unittest
import sys
sys.path.append('src/')
from src import ws_nbc, ner_model

'''
A simple and basic unit test of model and web scrapping.
'''

class Testing(unittest.TestCase):

    def test_0_get_unique_results(self):
        a = {'NAME': ['Kevin', 'Joe'], 'ORGANIZATION': ['Apple','Amazon'], 'LOCATION': ['Canada', 'USA']}
        test = 'My name is Kevin and my friends name is Joe.  I work for Apple and my friend works for Amazon.  I live in Canada and my friend lives in USA'
        model = ner_model.Model()
        ner_results = model.ner(test)
        b = ner_model.get_unique_results(ner_results)
        self.assertEqual(a,b)

    def test_1_web_scraper(self):
        url = 'https://www.nbcnews.com/politics/biden-says-considering-gas-tax-holiday-rcna34419'
        scraper = ws_nbc.WebScrape(url)
        content = scraper.scrape_news_article
        self.assertIsNotNone(content)

    def test_2_n_scraper(self):
        url = 'https://www.nbcnews.com/'
        scraper = ws_nbc.WebScrape(url)
        content = scraper.scrape_n_articles(num_articles=1)
        self.assertIsNotNone(content)

if __name__ == '__main__':
    unittest.main()