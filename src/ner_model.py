import pandas as pd
import warnings
import spacy
import json

from spacy import displacy
# from transformers import AutoTokenizer, TFBertForTokenClassification
# from transformers import pipeline
from ws_nbc import web_scraper


# def hf_ner():
#     tokenizer = AutoTokenizer.from_pretrained("dslim/bert-base-NER")
#     model = TFBertForTokenClassification.from_pretrained("dslim/bert-base-NER")
#     nlp = pipeline("ner", model=model, tokenizer=tokenizer, framework='tf')

#     return nlp

def spacy_ner():
    NER = spacy.load("en_core_web_sm")
    return NER


def upload_data(path):
    '''
    DATA UPLOAD AND EXPLORATION
    '''
    # Load dataset
    df = pd.read_csv(path, header=0)

    # Drop any unwanted columns
    df.drop(['selected_text', 'textID'], axis=1, inplace=True)

    print('\n\033[1mData Dimension:\033[0m Dataset consists of {} columns & {} records.'.format(df.shape[1], df.shape[0]))
    print(df.describe())
    return df

def get_unique_results(model_output):
    # Prepare dictionary for obtaining only Name, Organization and Location
    article = {'NAME':[], 'ORGANIZATION':[], 'LOCATION':[]}

    # Iterate through each word in the sentence and extract the target entities
    for word in model_output.ents:
        if word.label_ == 'PERSON' and (word.text not in article["NAME"]):
            article["NAME"].append(word.text)
        elif word.label_ == 'ORG' and (word.text not in article["ORGANIZATION"]):
            article["ORGANIZATION"].append(word.text)
        elif word.label_ == 'GPE' and (word.text not in article["LOCATION"]):
            article["LOCATION"].append(word.text)
    return article

def get_ner_for_all(article, model):
    ''''
    This function is used to obtain NER results for each content in the article
    and is place in a new dataframe
    '''
    final_out = article.copy()
    for index, row in final_out.iterrows():
        spacy_results = model(row['Article Content'])
        article_ner = get_unique_results(spacy_results)
        final_out.iloc[[index], [1]] = [article_ner]
    return final_out

def save_to_json(results, path):
    outputDict = results.set_index('Article Link').to_dict()['Article Content']

    with open(path+'output.json', 'w') as fp:
        json.dump(outputDict, fp,  indent=4)

def save_to_csv(results, path):
    results.set_index('Article Link').to_csv(path+'output.csv')

if __name__ == '__main__':
    url = 'https://www.nbcnews.com/'
    saved_output = '../data/model_output/'
    num_articles = 5

    # ner_model = hf_ner()
    spacner = spacy_ner()

    article = web_scraper(url, number_of_articles=num_articles)

    output = get_ner_for_all(article, spacner)

    save_to_json(output, saved_output)
    save_to_csv(output, saved_output)