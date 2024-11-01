from openai import OpenAI
import streamlit as st
from os import walk


"""General Purpose functions"""

### me
def make_call_get_response():
    prompt_type = st.session_state.prompt_type
    dataframe = st.session_state.dataframe
    question_number = st.session_state.question_number
    api_key = st.session_state.api_key

    try:
        llm_client = LLM_client(prompt_type,dataframe.iloc[1:,5+int(question_number)].to_list())
        st.session_state.response_title = f"**Question:** {dataframe.iloc[0,5+int(question_number)]}"
        llm_client.get_LLM_repsonse(api_key)
        st.session_state.llm_response = llm_client.response
        # print(st.session_state.response_title)
        # print(st.session_state.llm_response)
        print(llm_client.response_json)

    except IndexError:
        st.error("Choose a column that has non-empty rows!")
    except Exception as e:
        st.error(f"Something went wrong. This incident has been reported. We will fix it! This is all we know -{str(e)}")


"""LLM Client Class"""
class LLM_client(object):

    def __init__(self,prompt_type, student_response):
        prompt_map = {
            "Summarize Per Question": 'general.txt',
            "Analyze Superficiality Per Question": 'superficial.txt'
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

        prompt = self.make_prompt()

        msg_to_gpt = [
            {
                "role":"user",
                "content": prompt
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
        print("output len",len(llm_output))
        self.response = llm_output[0].message.content #''.join([output.message.content for output in llm_output[:-1]])

        self.response_json = llm_output[-1].message.content
