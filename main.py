import streamlit as st
from utils import *
import pandas as pd
from os import path
from io import StringIO
from streamlit.components.v1 import components

uploaded_file = st.file_uploader("Submit Student Responses from Canvas in .csv ",type=['.csv'])

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
    st.selectbox("Which Question Would you like to Analyze?",key="question_number",options=get_column_names())

if 'dataframe' in st.session_state and not(st.session_state.question_number == None) and uploaded_file is not None:
    st.selectbox("What do we ask ChatGPT?",key="prompt_type",options=["1: General Student Resonse Trends","2: Specific Issues w Student Response(s)","3: Specific Issues w Specific Student Response"])
# question_number = st.number_input("Provide the Question number to summarize on (every odd number)",value=None)

if 'dataframe' in st.session_state and not(st.session_state.question_number == None) and \
    uploaded_file is not None: 
    
    if not(st.session_state.prompt_type == "3: Specific Issues w Specific Student Response"):
        st.selectbox("Which Student to Analyze?",key="all_students",options="All Students")
    
    if st.session_state.prompt_type == "3: Specific Issues w Specific Student Response":
        st.selectbox("Which Student to Analyze?",key="student_names",options=get_student_names())



if st.button("Generate",key="",on_click=make_call_get_response):
    try:
        # st.button("Edit The Feedback",on_click=make_it_text)
        st.session_state.feedback_complete = 0
        
        st.session_state['feedback'] = st.session_state.llm_response
        st.text_area("LLM Rubric",value=st.session_state['prompt'])
        st.markdown(st.session_state['response_title'])
        st.markdown(st.session_state['feedback'])
        

        # clear_session_state()
    except Exception as e:
        st.error(f"Nothing to generate-{str(e)}")




