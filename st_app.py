import streamlit as st

if __name__ =='__main__':
    st.write("""
            # Named-Entity-Recognition with SpaCy
            Using the Spacy Pretrained model, I created an ML pipline to allow any user to insert the link of an BNC news article and render all entities such as organization, location, name of person, etc.
            """)

    user_input = st.text_input("Insert Nbc News article Link")

    print(user_input)