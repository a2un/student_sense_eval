from openai import OpenAI
import streamlit as st
from os import walk
import pyperclip as pycpy

"""General Purpose functions"""

def make_it_complete():
    st.session_state.feedback_complete = 1

def summarize(question_text):

    client = OpenAI(api_key=st.secrets.api_key)

    msg_to_gpt = [
            {
                "role":"user",
                "content": f"summarize to 10 word sentence:\n{question_text}"
            }
        ]
        
    response = client.chat.completions.create(
        model = "gpt-4o-mini",
        messages=msg_to_gpt,
        temperature=0,
        max_tokens=1024,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
        
    return response.choices[0].message.content


def get_column_names():
    return [f"{5+q_num}: {summarize(st.session_state.dataframe.iloc[0,5+q_num])}" \
            for q_num in range(st.session_state.dataframe.shape[1]) \
            if 5+q_num < st.session_state.dataframe.shape[1] and \
                q_num %2 == 1]


def get_student_names():
    student_names = ["All Students"]
    student_names.extend([i for i in range(1,len(st.session_state.dataframe))])
    return student_names

### me
def get_student_list(dataframe,question_number,student_id):
    if student_id == "All Students":
        return dataframe.iloc[1:,5+int(question_number)].to_list()
    else:
        return dataframe.iloc[int(student_id),5+int(question_number)].to_list()
    

def make_call_get_response():
    try:
        prompt_type = st.session_state.prompt_type.split(":")[0]
        dataframe = st.session_state.dataframe
        question_number = st.session_state.question_number.split(":")[0]
        student_id = st.session_state.student_names
        api_key = st.secrets.api_key

    
        llm_client = LLM_client(prompt_type,get_student_list(dataframe, question_number,student_id))
        st.session_state.response_title = f"**Question:** {dataframe.iloc[0,5+int(question_number)]}"
        llm_client.get_LLM_repsonse(api_key)
        st.session_state.llm_response = llm_client.response
        # print(st.session_state.response_title)
        # print(st.session_state.llm_response)
        # print(llm_client.response_json)

    except IndexError:
        st.error("Choose a column that has non-empty rows!")
    except AttributeError:
        if not("question_number" in st.session_state) or \
            not("dataframe" in st.session_state) or \
            not("prompt_type" in st.session_state):
            st.error("Please upload a file!")
        if not("response_title" in st.session_state) or \
            not("llm_response" in st.session_state):
            st.error("API key not provided")
    except Exception as e:
        st.error(f"Something went wrong. This incident has been reported. We will fix it! This is all we know -{str(e)}")



def clear_session_state():
    try:
        for key in st.session_state.keys():
            if not(key in ['feedback_counter','feedback']):
                del st.session_state[key]
    except:
        st.error("We didn't mean for this to happen")


"""LLM Client Class"""
class LLM_client(object):

    def __init__(self,prompt_type, student_response):
        prompt_map = {
            "1": 'general.txt',
            "2": 'superficial.txt'
        }

        self.prompt_type = prompt_map[prompt_type]
        self.student_response = student_response
        self.response = ""
        self.response_json = {}

    def make_prompt(self):
        with open(f'./prompts/per_question/{self.prompt_type}','r') as f:
            return f.read().format(**{
                "student_responses": f"{self.student_response!r}"
            })

    def get_LLM_repsonse(self,api_key):

        client = OpenAI(api_key=api_key)

        st.session_state.prompt = self.make_prompt()

        msg_to_gpt = [
            {
                "role":"system",
                "content":"You are the TA for this course: Introduction to Psychological Cognition."
            },
            {
                "role":"user",
                "content": st.session_state.prompt
            }
        ]
        
        response = client.chat.completions.create(
            model = "gpt-4o-mini",
            messages=msg_to_gpt,
            temperature=0,
            max_tokens=1024,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        
        self.post_process(response.choices)


    def post_process(self,llm_output):
        # print("output len",len(llm_output))
        self.response = llm_output[0].message.content #''.join([output.message.content for output in llm_output[:-1]])

        self.response_json = llm_output[-1].message.content
