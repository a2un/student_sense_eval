# @title
import streamlit as st
from utils import *
default_path = './'

# selected_questions = [36,46]

st.file_uploader("Submit Questions File ",key="questions_file",type=['.csv'])

st.file_uploader("Submit Student Responses from Canvas in .csv ",key="student_response_file", type=['.csv'])

load_data()

if st.session_state.questions_file != None and \
    st.session_state.student_response_file != None:

    st.multiselect("Which questions would you like to analyze?",key="selected_questions",
                    options=st.session_state.questions_df.questions)

    if len(st.session_state.selected_questions) > 0:
        
        st.write(st.session_state.selected_questions)
        questions = st.session_state.questions_df.loc[[ind for ind,_ in enumerate(st.session_state.selected_questions)],'questions'].to_list()
        filenames = st.session_state.questions_df.loc[[ind for ind,_ in enumerate(st.session_state.selected_questions)],'filename'].to_list()


        for filename,question in zip(filenames,questions):
            st.write("### Selected Question")
            # st.write(filename.split('/')[-1])
            st.write(question)
            student_response = get_student_response(filename,question)
            
            st.markdown("### Student response")
            st.write(student_response)

            st.markdown("### Student Prompts")
            guidance_and_prompts = get_guidance_and_prompts(question)
            st.write(guidance_and_prompts)

            st.selectbox("##Select student prompt to match with",key="studentPrompt",
                        options = guidance_and_prompts["student_prompts"])

            # for student_prompt in guidance_and_prompts['student_prompts']:
            st.markdown("### Selected Student Prompt")
            st.write(st.session_state.studentPrompt)
            student_matched_response = match_student_responses(f"{guidance_and_prompts['instructions_or_guidance']}{st.session_state.studentPrompt}",student_response)
            st.markdown("### Matched Student Responses")
            st.write(student_matched_response)

clear_session_state()