import streamlit as st
import requests
import textstat as ts

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
            st.write("in matches")
            message = match.get('message')
            error_text = match['context']['text'][match['offset']:match['offset'] + match['length']]
            suggestions = []

            if message == "Possible spelling mistake found.":
                st.write("in spelling")
                suggestions = [r['value'] for r in match.get('replacements', [])][:3]

            formatted_message = f"<font color='red'><s>{error_text}</s></font>"
            
            if suggestions:
                st.write("in suggestions")
                formatted_message += " (Suggestions:"
                for suggestion in suggestions:
                    st.write("in for")
                    formatted_message += f" <font color='green'>{suggestion}</font>"
                formatted_message += ")"

            st.write(f"• **{message}** {formatted_message}\n")
        return []
    else:
        st.error("Failed to connect to the LanguageTool API.")
        return []






st.title("Writing Help")


if 'text' not in st.session_state:
    st.session_state.text = 'Your text goes here....'

text_area = st.text_area('Text Field', st.session_state.text, key='text')
grammar = st.button('Check Grammar')

if grammar:
    matches = grammar_checker(st.session_state.text)
    

