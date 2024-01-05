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
        st.write("API Response:", response.json())  # Debug print

        return response.json().get('matches', [])
    else:
        st.error("Failed to connect to the LanguageTool API.")
        return []






st.title("Writing Help")


if 'text' not in st.session_state:
    st.session_state.text = 'Your text goes here....'

text_area = st.text_area('Text Field', st.session_state.text, key='text')
grammar = st.button('Check Grammar')

if grammar:
    st.write(st.session_state.text)
    #matches = grammar_checker(st.session_state.text)
    #if not matches:
    #    st.write("No grammar suggestions found.")

    #for match in matches:
    #    message = match.get('message')
    #    error_text = match['context']['text'][match['offset']:match['offset'] + match['length']]
    #    suggestions = [r['value'] for r in match.get('replacements', [])][:3]  # Limit to top 3 suggestions
    #
    #    st.markdown(f"• **{message}** `{error_text}`")
    #
    #    suggestion_buttons = st.columns(len(suggestions))
    #    for i, suggestion in enumerate(suggestions):
    #        if suggestion_buttons[i].button(suggestion):
    #            st.session_state.text = apply_correction(st.session_state.text, match, suggestion)
    #            st.experimental_rerun()

