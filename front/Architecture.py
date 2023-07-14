import pandas as pd
import streamlit as st
from dotenv import load_dotenv
from PIL import Image
from services.utils import initialize

load_dotenv()

COLLECTION_NAME = "embeddings"
DISTANCE_METRIC = "Cosine"
VECTORS_COUNT = 1536
BATCH_SIZE = 100

if __name__ == '__main__': 

    title = "Azure OpenAI Demos"
    st.set_page_config(page_title=title, layout="wide")
    image = Image.open('assets/microsoft.png')
    st.image(image, width=200)

    st.header(title)

    initialize()

    if 'collections' not in st.session_state:
        st.session_state["collections"] = []            


    col1, col2 = st.columns([1, 1], gap="large")
    styles = """
                <style>
                .green { color: green }
                .red { color: red }
                .bold { font-weight: bold }
                </style>
                """
    st.markdown(styles, unsafe_allow_html=True)

    image = Image.open('assets/scrcpy_ft7ADG15kt.png')

    # Display the image
    st.image(image, caption='Architecture')

       