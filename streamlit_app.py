import streamlit as st
import requests
import textstat as ts
import os
import openai

api_key = os.environ.get('OPENAI_API_KEY')


# Function to call LanguageTool API for grammar checking
def grammar_checker(text):
    api_url = "https://api.languagetool.org/v2/check"
    payload = {
        'text': text,
        'language': 'en-US'
    }
    response = requests.post(api_url, data=payload)
    if response.status_code == 200:
        matches = response.json().get('matches', [])
        if not matches:
            st.write("No grammar suggestions found.")
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

            st.markdown(f"• {formatted_message}")
        return []
    else:
        st.error("Failed to connect to the LanguageTool API.")
        return []

def make_it_longer(text):






st.title("Writing Help")


if 'text' not in st.session_state:
    st.session_state.text = 'Your text goes here....'

text_area = st.text_area('Text Field', st.session_state.text, key='text')
grammar = st.button('Check Grammar')
st.write(api_key)

if grammar:
    matches = grammar_checker(st.session_state.text)
    

