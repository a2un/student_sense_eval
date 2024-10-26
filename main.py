import streamlit as st
from utils import LLM_client
import pandas as pd
from os import path
from io import StringIO

api_key = st.text_input("Provide OpenAI API Key")
prompt_type = st.selectbox("Select Prompt Options",options=["Summarize Per Question","Analyze Superficiality Per Question"])
uploaded_file = st.file_uploader("upload the file to be processed",type=['.xlsx','.csv'])

if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()
    st.write(bytes_data)

    # To convert to a string based IO:
    stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
    st.write(stringio)

    # To read file as string:
    string_data = stringio.read()
    st.write(string_data)

    # Can be used wherever a "file-like" object is accepted:
    dataframe = pd.read_csv(uploaded_file)
    st.dataframe(dataframe)

    llm_client = LLM_client(prompt_type,[])
