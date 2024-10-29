import streamlit as st
from utils import LLM_client
import pandas as pd
from os import path
from io import StringIO

api_key = st.text_input("Provide OpenAI API Key")
prompt_type = st.selectbox("Select Prompt Options",options=["Summarize Per Question","Analyze Superficiality Per Question"])
question_number = st.number_input("Provide the Question number to summarize on (every odd number)",value=None)

uploaded_file = st.file_uploader("upload the file to be processed",type=['.csv'])
if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()
    # To convert to a string based IO:
    stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))

    # To read file as string:
    string_data = stringio.read()

    # Can be used wherever a "file-like" object is accepted:
    dataframe = pd.read_csv(uploaded_file)

    llm_client = LLM_client(prompt_type,dataframe.iloc[:,5+int(question_number)].to_list())

    response = llm_client.get_LLM_repsonse(api_key)
    # print(response)
    st.markdown(response)
