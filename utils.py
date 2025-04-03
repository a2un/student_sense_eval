import streamlit as st
import os
from os.path import exists,join,basename,splitext
from os import walk,chdir,mkdir
import pandas as pd
from openai import OpenAI
from tqdm import tqdm
from json import loads,dumps,dump,load
from ast import literal_eval
import re
path_prefix = st.secrets.path_responses

def load_data():
  return pd.read_csv(st.secrets.qlist_file)

def clear_session_state():
    try:
        for key in st.session_state.keys():
            if not(key in ['feedback_counter','feedback']):
                del st.session_state[key]
    except:
        st.error("We didn't mean for this to happen")

def make_prompt(dir:str,prompt_type:str, question_or_prompt:str,student_response_list:str):

  with open(f'./prompts/{dir}/{prompt_type}.txt') as f:
    return f.read().format(**{
      "question_list":question_or_prompt,
      "student_prompt":question_or_prompt,
      "student_response_list":student_response_list,
      "student_response":student_response_list
    })


def get_student_response(filename:list, question:list):
  student_response = pd.read_csv(join(path_prefix,filename.split('/')[-1]))
  
  student_response = student_response.loc[:,question].to_list()

  return student_response


def get_prompt_names():
  prompt_f = []
  for _,_,fnames in walk('./prompts'):
    for file in fnames:
      prompt_f.append(splitext(file)[0])

  return prompt_f



def get_guidance_and_prompts(question:str):
  # question_splits = []
  
  client = OpenAI(api_key=st.secrets.api_key)
  prompt = make_prompt('','separate_questions', question,[])
  
  print("## LLM Prompt")
  print(prompt)
  
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


  # question_splits.append(response.choices[0].message.content)

  return loads(response.choices[0].message.content)



def match_student_responses(student_prompt:str,student_response_list:str):

    # question_splits = []
  
    client = OpenAI(api_key=st.secrets.api_key)
    prompt = make_prompt('','match_student_response', student_prompt,student_response_list)
    
    print("## LLM Prompt")
    print(prompt)
    
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


    # question_splits.append(response.choices[0].message.content)

    return response.choices[0].message.content
