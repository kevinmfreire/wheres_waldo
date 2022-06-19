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


if __name__ == '__main__':
    url = 'https://www.nbcnews.com/'

    # ner_model = hf_ner()
    spacner = spacy_ner()

    title, content, link = web_scraper(url, 1)
    spacy_results = spacner(content[0])

    for word in spacy_results.ents:
        print(word.text,word.label_)

    displacy.serve(spacy_results, style="ent")
    # print(spacy_results.text, spacy_results.label_)