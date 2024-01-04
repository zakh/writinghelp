import streamlit as st
import os
import openai
from langchain.llms import OpenAI
import textstat as ts
import language_tool_python
import requests

openai_api_key = os.getenv("OPENAI_API_KEY")

def readability_checker(w):
    stats = dict(
            flesch_reading_ease=ts.flesch_reading_ease(w),
            flesch_kincaid_grade=ts.flesch_kincaid_grade(w),
            automated_readability_index=ts.automated_readability_index(w),
            smog_index=ts.smog_index(w),
            coleman_liau_index=ts.coleman_liau_index(w),
            dale_chall_readability_score=ts.dale_chall_readability_score(w),
            linsear_write_formula=ts.linsear_write_formula(w),
            gunning_fog=ts.gunning_fog(w),
            word_count=ts.lexicon_count(w),
            difficult_words=ts.difficult_words(w),
            text_standard=ts.text_standard(w),
            sentence_count=ts.sentence_count(w),
            syllable_count=ts.syllable_count(w),
            reading_time=ts.reading_time(w)
    )
    return stats

def grammar_checker(text):
    api_url = "https://api.languagetool.org/v2/check"
    payload = {
        'text': text,
        'language': 'en-US'
    }
    response = requests.post(api_url, data=payload)
    result = []

    if response.status_code == 200:
        data = response.json()
        for match in data.get('matches', []):
            error_text = text[match['offset']: match['offset'] + match['length']]
            suggestions = [suggestion['value'] for suggestion in match.get('replacements', [])]
            
            result.append(f'Error in text => {error_text}')
            result.append(f'Can be replaced with => {suggestions}')
            result.append('--------------------------------------')
    else:
        result.append("Error in connecting to LanguageTool API.")

    return result




st.title("Writing Help")


placeholder = 'Your text goes here....'
text = st.text_area('Text Field', placeholder, height=200)
left, right = st.columns([5, 1])
scan = left.button('Check Readability')
grammar = right.button('Check Gramamar')

if scan:
    st.write('Text Statistics')
    st.write(readability_checker(text))
elif grammar:
    corrections = grammar_checker(text)
    for index, correction in enumerate(corrections):
        error_text, suggestions = correction[0], correction[1]

        # Displaying original error and suggestions
        st.markdown(f"**Error:** ~~{error_text}~~")

        for suggestion in suggestions:
            # Create a unique key for each button using the index and suggestion
            button_key = f"apply_{index}_{suggestion}"
            if st.button(f"Apply '{suggestion}'", key=button_key):
                # Replace the first occurrence of error_text with this suggestion
                text = text.replace(error_text, suggestion, 1)
                # Update the text area with the new text
                st.text_area('Text Field', text, height=200)



