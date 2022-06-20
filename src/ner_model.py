from transformers import AutoTokenizer, TFBertForTokenClassification
from transformers import pipeline
import pickle as pk
import pandas as pd
import warnings
import onnx
from onnx_tf.backend import prepare
import tensorflow as tf

import spacy
from spacy import displacy

from ws_nbc import web_scraper
'''
This script only has to be run once as it will save the model in a pickle file.
You can load the model using pickle.load(open('model_path', 'rb'))
'''

def hf_ner():

    tokenizer = AutoTokenizer.from_pretrained("dslim/bert-base-NER")
    model = TFBertForTokenClassification.from_pretrained("dslim/bert-base-NER")
    nlp = pipeline("ner", model=model, tokenizer=tokenizer, framework='tf')

    return nlp

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

def load_onnx_model(model_path):
    warnings.filterwarnings('ignore')
    onnx_model = onnx.load(model_path)
    output = prepare(onnx_model)#.run(input)
    return output

def get_unique_results(model_output):
    article = {'NAME':[], 'ORGANIZATION':[], 'LOCATION':[]}
    for word in model_output.ents:
        if word.label_ == 'PERSON' and (word.text not in article["NAME"]):
            article["NAME"].append(word.text)
        elif word.label_ == 'ORG' and (word.text not in article["ORGANIZATION"]):
            article["ORGANIZATION"].append(word.text)
        elif word.label_ == 'GPE' and (word.text not in article["LOCATION"]):
            article["LOCATION"].append(word.text)
    return article

def get_ner_for_all(article):
    final_out = article.copy()
    for index, row in final_out.iterrows():
        spacy_results = spacner(row['Article Content'])
        article_ner = get_unique_results(spacy_results)
        final_out.iloc[[index], [1]] = [article_ner]
    return final_out


if __name__ == '__main__':
    url = 'https://www.nbcnews.com/'

    # ner_model = hf_ner()
    spacner = spacy_ner()

    article = web_scraper(url, 5)

    output = get_ner_for_all(article)
    print(output)