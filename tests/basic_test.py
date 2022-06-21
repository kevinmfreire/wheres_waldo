import unittest
import sys
sys.path.append('../src/')

# All the functions and class we want to test
import ws_nbc, ner_model

class Testing(unittest.TestCase):

    def test_0_get_unique_results(self):
        a = {'NAME': ['Kevin', 'Joe'], 'ORGANIZATION': ['Apple','Amazon'], 'LOCATION': ['Canada', 'USA']}
        test = 'My name is Kevin and my friends name is Joe.  I work for Apple and my friend works for Amazon.  I live in Canada and my friend lives in USA'
        model = ner_model.model()
        ner_results = model.ner(test)
        b = ner_model.get_unique_results(ner_results)
        self.assertEqual(a,b)

    def test_1_web_scraper(self):
        url = 'https://www.nbcnews.com/politics/biden-says-considering-gas-tax-holiday-rcna34419'
        scraper = ws_nbc.web_scrape(url)
        # content = Testing.bs.scrape_news_article
        content = scraper.scrape_news_article
        self.assertIsNotNone(content)

    def test_2_n_scraper(self):
        url = 'https://www.nbcnews.com/'
        scraper = ws_nbc.web_scrape(url)
        content = scraper.scrape_N_articles(num_articles=1)
        self.assertIsNotNone(content)

if __name__ == '__main__':
    unittest.main()