# wheres_waldo
This project was developed to identify the name, address and organization name within content of a News Article.

## Overview
Natural Language Processing (NLP) Models are very popular worldwide as it can be used in many cases such as launguage translation, speech-to-text or vice versa, it can detect fraud,
or even classify highly sensitive data. In other words, it can make our lives easier.

This project is for the purpose of extracting names, organizations and locations from a news article, more specifically NBC News.  It is done by using the spaCy pretrained model `en_core_web_sm`
which is a light weight model for Name Entity Recongnition (NER).  It can extract much more than just the name, location and organization, it can also classify words as either being a date, or law, etc.

 ## Goals
 The following bullet points are the challanges we want to complete.

 * Design and Implement an NLP model using TensorFlow 2.0 to identify name, location, and organization within a text.
 * Write a python application that uses a web scraper to extract text from a news article (NBC news).
 * Use the created model to identify name, location and organization from the extracted text.
 * Store the results in a database (`.csv` and `.json`)
 * Set up a unit test for the code

 ## Practical Applications
 * Extract information on certain artciles on the web to detect privacy misconduct.
 * Analyze multiple articles to find rising trends (e.g What company/person/location is mentioned most).
 * Quickly parse through resume to find name, location and companies that applicant was involved in.

 ## Usage
 * Clone repo:
 ```
git clone https://github.com/kevinmfreire/wheres_waldo.git
 
 ```
* Set up virtual environment:
```
virtualenv .virtualenv/wheres_waldo
```
* Activate Virtual Environment:
```
source .virtualenv/wheres_waldo
```
* Install all requirements:
```
pip install -r requirements.txt
```
* If you want to see how the web scrapping works go to `src/` directory and run:
```
python ws_nbc.py
```
It will save the dataframe as a `.csv` file so you can take a look at the output.

* If you would like to see how the model works go to the `.src` directory and run:
```
python ner_model.py
```
The output of the model is saved under `data/modeloutput/` as a `.json` and `.vsc` file.
