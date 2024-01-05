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
    
def apply_correction(text, match, suggestion):
    return text[:match['offset']] + suggestion + text[match['offset'] + match['length']:]



if 'text' not in st.session_state:
    st.session_state.text = 'Your text goes here....'

text_area = st.text_area('Text Field', st.session_state.text, height=200)
left, right = st.columns([5, 1])
scan = left.button('Check Readability')
grammar = right.button('Check Grammar')

if scan:
    st.write('Text Statistics')
    st.write(readability_checker(text_area))
elif grammar:
    matches = grammar_checker(text_area)
    for match in matches:
        message = match.get('message')
        error_text = match['context']['text'][match['offset']:match['offset'] + match['length']]
        suggestions = [r['value'] for r in match.get('replacements', [])][:3]  # Limit to top 3 suggestions

        st.markdown(f"• **{message}** `{error_text}`")

        suggestion_buttons = st.columns(len(suggestions))
        for i, suggestion in enumerate(suggestions):
            if suggestion_buttons[i].button(suggestion):
                st.session_state.text = apply_correction(text_area, match, suggestion)
                st.rerun()