import streamlit as st
import requests
import textstat as ts
import os
import openai

api_key = os.environ.get('OPENAI_API_KEY')
openai.api_key = api_key


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

            #st.markdown(f"• {formatted_message}")
        return formatted_message
    else:
        st.error("Failed to connect to the LanguageTool API.")
        return []


def make_it_longer(text):
    # Define the user prompt message
    prompt = "Hello!"
    # Create a chatbot using ChatCompletion.create() function
    completion = openai.ChatCompletion.create(
    # Use GPT 3.5 as the LLM
    model="gpt-3.5-turbo",
    # Pre-define conversation messages for the possible roles
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": prompt}
    ]
    )
    return(completion.choices[0].message)

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
    

