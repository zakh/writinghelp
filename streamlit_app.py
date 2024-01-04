import streamlit as st
import os
import openai
from langchain.llms import OpenAI
import textstat as ts
import language_tool_python
openai_api_key = os.getenv("OPENAI_API_KEY")



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
    st.write(grammar_checker(box))


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
    tool = language_tool_python.LanguageTool('en-US', config={'maxSpellingSuggestions': 1})
    check = tool.check(text)
    result = []
    for i in check:
        result.append(i)
        result.append(f'Error in text => {text[i.offset : i.offset + i.errorLength]}')
        result.append(f'Can be replaced with =>  {i.replacements}')
        result.append('--------------------------------------')
    return result