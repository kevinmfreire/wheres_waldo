import spacy
import json
import argparse
from ws_nbc import WebScrape

class Model:
    '''
    This class initializes the Spacy pipline for NER.  You can initialize it by calling
    model = model() then to pass a text you call model.ner(text).  To get a dataframe of
    N number of articles then you call model.get_ner_for_all(articles).
    '''
    def __init__(self):
        self.model = spacy.load("en_core_web_sm")

    def ner(self, content):
        return self.model(content)

    def get_ner_for_all(self, article):
        ''''
        This function is used to obtain NER results for each content in the article
        and is place in a new dataframe.
        '''
        final_out = article.copy()
        for index, row in final_out.iterrows():
            spacy_results = self.model(row['article content'])
            article_ner = get_unique_results(spacy_results)
            final_out.iloc[[index], [1]] = [article_ner]
        return final_out

def get_unique_results(model_output):
    '''
    This function prepares a dictionary:

    article = {
        'NAME' : [...],
        'ORGANIZATION' : [...],
        'LOCATION' : [...]
    }

    It then appends the desired entities from the NER model output into the dictionary.  The entities are,
    ORG (company, organizations, etc.), PERSON (Name or person), and GPE (Location).
    '''

    article = {'NAME':[], 'ORGANIZATION':[], 'LOCATION':[]}

    for word in model_output.ents:
        if word.label_ == 'PERSON' and (word.text not in article["NAME"]):
            article["NAME"].append(word.text)
        elif word.label_ == 'ORG' and (word.text not in article["ORGANIZATION"]):
            article["ORGANIZATION"].append(word.text)
        elif word.label_ == 'GPE' and (word.text not in article["LOCATION"]):
            article["LOCATION"].append(word.text)
    return article

def save_to_json(results, path):
    outputDict = results.set_index('article link').to_dict()['article content']

    with open(path+'output.json', 'w') as fp:
        json.dump(outputDict, fp,  indent=4)

def save_to_csv(results, path):
    results.set_index('article link').to_csv(path+'output.csv')

if __name__ == '__main__':

    parser= argparse.ArgumentParser()
    parser.add_argument('--nbc_url', type=str, default='https://www.nbcnews.com/')
    parser.add_argument('--nbc_article_url', type=str, default='https://www.nbcnews.com/politics/biden-says-considering-gas-tax-holiday-rcna34419')
    parser.add_argument('--save_path', type=str, default='../data/model_output/')
    parser.add_argument('--num_articles', type=int, default=5)
    args = parser.parse_args()

    spacy_ner = Model()
    nbc_news = WebScrape(args.nbc_url)
    nbc_article = WebScrape(args.nbc_article_url)

    # For multiple Articles
    multi_article = nbc_news.scrape_n_articles(num_articles=args.num_articles)
    output = spacy_ner.get_ner_for_all(multi_article)

    # For a single article
    article = nbc_article.scrape_news_article()
    model_out = spacy_ner.ner(article.get('article content'))
    unique_results = get_unique_results(model_out)

    save_to_json(output, args.save_path)
    save_to_csv(output, args.save_path)