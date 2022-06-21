# wheres_waldo
### Requirements for this project
* Python 3.x
* TensorFlow 2.x

## Table of content
* [Overview](https://github.com/kevinmfreire/wheres_waldo#overview)
* [Goals](https://github.com/kevinmfreire/wheres_waldo#goals)
* [Practical Applications](https://github.com/kevinmfreire/wheres_waldo#practical-applications)
* [Usage](https://github.com/kevinmfreire/wheres_waldo#usage)
* [Conclusion](https://github.com/kevinmfreire/wheres_waldo#conclusion)
* [Requirements](https://github.com/kevinmfreire/wheres_waldo#requirements)

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
source .virtualenv/wheres_waldo/bin/activate
```
* Install all requirements:
```
pip install -r requirements.txt
```
* If for some reason the spaCy model did not download then run:
```
./package_loader.sh
```
* If you want to see how the web scrapping works go to `src/` directory and run:
```
python ws_nbc.py
```
It will save the dataframe as a `.csv` file to `data/ws_data/` so you can take a look at the output.

* If you would like to see how the model works go to the `.src` directory and run:
```
python ner_model.py
```
The output of the model is saved under `data/model_output/` as a `.json` and `.vsc` file.
* To observe how the model works on a single article and would like to search NAME, ORGANIZATION, and LOCATION mentioned in article then run:
```
python main.py
```
* To observe how the model works on multiple articles and would like to search NAME, ORGANIZATION, and LOCATION mentioned in article then run:
```
python main.py --multi_article True
```
Default value for number of articles is 5, if you want more then add argument `--num_articles` and place desired number.
* To run a basic Unit Test then go to `./tests/` and run:
```
python basic_test.py
```

## Conclusion
The model is a light weight model so it doesn't classify the text perfectly.  By observing the output of the model in `data/model_output/output.json` you can see that it made a few mistakes.  Nevertheless, it works pretty well.  
The model can definitly be imporved.  In regards to the output, I've decided to have the link of the article and the output results of the model tied together.  The purpose of this is because if one would like to see what the article
talks about based on the outputs then they can easily access the article. Keep in mind that the web scrapping will be different everyday because NBC News always has a new story so the results will be different for everyone.  Please feel free to place any contributions and if you have any issues feel free to reach out.