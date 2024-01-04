import streamlit as st
import os
import openai
from langchain.llms import OpenAI
import textstat as ts
import language_tool_python
import requests

# ... [Rest of your imports and functions]

def grammar_checker(text):
    api_url = "https://api.languagetool.org/v2/check"
    payload = {
        'text': text,
        'language': 'en-US'
    }
    response = requests.post(api_url, data=payload)
    if response.status_code == 200:
        return response.json().get('matches', [])
    else:
        st.error("Failed to connect to the LanguageTool API.")
        return []

st.title("Writing Help")

placeholder = 'Your text goes here....'
text = st.text_area('Text Field', placeholder, height=200)
left, right = st.columns([5, 1])
scan = left.button('Check Readability')
grammar = right.button('Check Grammar')

if scan:
    st.write('Text Statistics')
    st.write(readability_checker(text))
elif grammar:
    matches = grammar_checker(text)
    for match in matches:
        message = match.get('message')
        error_text = match['context']['text'][match['offset']:match['offset'] + match['length']]
        suggestions = [r['value'] for r in match.get('replacements', [])]

        st.markdown(f"• **{message}** `{error_text}` {' '.join(suggestions)}")

        for suggestion in suggestions:
            if st.button(f"Apply '{suggestion}' to '{error_text}'"):
                text = text[:match['offset']] + suggestion + text[match['offset'] + match['length']:]
                st.text_area('Text Field', text, height=200)
