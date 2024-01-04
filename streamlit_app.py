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

    return response




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
    matches = grammar_checker(text)
    for match in matches:
        message = match['message']
        error_text = match['context']['text'][match['offset']:match['offset'] + match['length']]
        suggestions = [r['value'] for r in match['replacements']]

        st.markdown(f"**{message}** {error_text} {' '.join(suggestions)}")

        for suggestion in suggestions:
            if st.button(f"Apply '{suggestion}' to '{error_text}'"):
                text = text[:match['offset']] + suggestion + text[match['offset'] + match['length']:]
                st.text_area('Text Field', text, height=200)



