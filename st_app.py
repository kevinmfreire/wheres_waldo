import streamlit as st
from spacy import displacy
import sys
sys.path.append("src/")
from src import ner_model, ws_nbc

nlp = ner_model.Model()

if __name__ =='__main__':
        st.set_page_config(layout="wide")
        st.write("""
            # Named-Entity-Recognition with SpaCy
            Using the Spacy Pretrained model, I created an Machine Learning pipline to allow any user to insert the link of an NBC 
            news article and render all entities such as organization, location, name of person, etc.

            ## Web Application Demo
            Below you can insert any NBC news article and the NER model will identify all entities.

            ### How it works:
            * I developed a Web Scrapping class that allows me to extract all the content of the given article.  
            * The extracted data then flows through the Spacy pipeline.
            * The pipeline is used for pre processing that data in order to feed into the SpaCy NER Model.
            * Once the model extracted all entities I then display the data with displacy.
            """)

        user_input = st.text_input("Insert Nbc News article Link")

        if user_input:
                nbc_article = ws_nbc.WebScrape(user_input)
                article = nbc_article.scrape_news_article()
                title = article.get('article title')
                model_out = nlp.ner(article.get('article content'))
                html = displacy.render(model_out, style='ent')
                
                st.write('# {}'.format(title))
                st.markdown(html, unsafe_allow_html=True)
