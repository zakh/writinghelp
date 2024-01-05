import streamlit as st
import requests
import textstat as ts
import os
from openai import OpenAI


def grammar_checker(text):
    api_url = "https://api.languagetool.org/v2/check"
    payload = {
        'text': text,
        'language': 'en-US'
    }
    response = requests.post(api_url, data=payload)
    if response.status_code == 200:
        matches = response.json().get('matches', [])
        all_messages = ""
        if not matches:
            return f"**No grammer errors found.**"
        for match in matches:
            message = match.get('message')
            error_text = match['context']['text'][match['offset']:match['offset'] + match['length']]
            suggestions = []

            if message == "Possible spelling mistake found.":
                suggestions = [r['value'] for r in match.get('replacements', [])][:3]

            formatted_message = f"**{message}** `{error_text}`"

            if suggestions:
                formatted_message += " (Suggestions:"
                for suggestion in suggestions:
                    formatted_message += f" `{suggestion}`"
                formatted_message += ")"
            all_messages += formatted_message + "\n\n"
            
    return all_messages
    


def make_it_longer(text):
    client = OpenAI(
        api_key=os.environ.get("OPENAI_API_KEY"),
    )
    prompt = "Please rephrase the following text to make it longer while preserving its meaning and detail: \n\n" += text
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        model="gpt-3.5-turbo",
    )
    return chat_completion.choices[0].message.content
    


st.title("Writing Help")


if 'text' not in st.session_state:
    st.session_state.text = 'Your text goes here....'

text_area = st.text_area('Text Field', st.session_state.text, key='text')
grammar = st.button('Check Grammar')
longer = st.button('Make it longer')

if grammar:
    st.markdown(grammar_checker(st.session_state.text))
elif longer:
    st.write(make_it_longer(st.session_state.text))
    

