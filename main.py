import streamlit as st
from utils import *
import pandas as pd
from os import path
from io import StringIO

uploaded_file = st.file_uploader("upload the file to be processed",type=['.csv'])

st.session_state['feedback_counter'] = 0
st.session_state['feedback'] = ''

# st.text_input("Provide OpenAI API Key",key="api_key", value="")

if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()
    # To convert to a string based IO:
    stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))

    # To read file as string:
    string_data = stringio.read()
    # Can be used wherever a "file-like" object is accepted:
    st.session_state.dataframe = pd.read_csv(uploaded_file,header=None)
    st.selectbox("Select Prompt Options",key="prompt_type",index=None,options=["Summarize Per Question","Analyze Superficiality Per Question"])

if 'dataframe' in st.session_state and not(st.session_state.prompt_type == None):
    st.selectbox("Provide the Question number to summarize",key="question_number",options=[2*k+1 for k in range(0,st.session_state.dataframe.shape[0])])
# question_number = st.number_input("Provide the Question number to summarize on (every odd number)",value=None)

if st.button("Generate",key="",on_click=make_call_get_response):
    try:
        st.button("Edit The Feedback",disabled=True,on_click=toggle_feedback_counter)
        st.button("Copy Feedback",disabled=True,on_click=copy_feedback)
        st.session_state['feedback'] = st.session_state.llm_response
        
        if not(st.session_state.feedback_counter): 
            st.markdown(st.session_state.response_title)
            st.markdown(st.session_state['feedback'])

        if st.session_state.feedback_counter: ## odd number, clicked
            st.markdown(st.session_state.response_title)
            st.text_area("Editing AI Generated Feedback...",
                            value=st.session_state['feedback'])

        # clear_session_state()
    except Exception as e:
        st.error(f"Nothing to generate-{str(e)}")

