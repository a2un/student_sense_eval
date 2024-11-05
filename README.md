# Student Sense Eval

Download this repository as a .zip and unzip.

1. Instructions to run locally

```{python}
cd /path/to/student_sense_eval
python3 -m venv ./student_sense_eval_env
python3 -m pip install -r requirements.txt
streamlit run main.py
```

If re-running the app without installation

MACOS / Linux
```{python}
source ./student_sense_eval_env/bin/activate
streamlit run main.py
```

Windows
```{python}
source ./student_sense_eval_env/Scripts/activate.bat
python3 -m streamlit run main.py
```


2. Once the app is running, it will launch a tab on your default browser automatically. 

3. In the webform, fill these fields:
    - OpenAI API Key will be provided to you
    - Select the type of prompt to ChatGPT from the drop down
    - Question number is every odd number
    - A file to upload will be provided to you

4. The response from ChatGPT will be automatically presented below the fields.

