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
        return response.json().get('matches', [])
    else:
        st.error("Failed to connect to the LanguageTool API.")
        return []

# Function to apply the suggested correction to the text
def apply_correction(text, match, suggestion):
    return text[:match['offset']] + suggestion + text[match['offset'] + match['length']:]

# Function to update the textarea with the applied suggestion
def update_text_area(match, suggestion):
    st.session_state.text = apply_correction(st.session_state.text, match, suggestion)
    st.rerun()

# Readability checker function
def readability_checker(w):
    return dict(
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

# Streamlit app layout
st.title("Writing Help")

# Initialize session state for text
if 'text' not in st.session_state:
    st.session_state.text = 'Your text goes here....'

# Create columns for buttons
left, right = st.columns([5, 1])
scan = left.button('Check Readability')
grammar = right.button('Check Grammar')

# Handling readability check
if scan:
    st.write('Text Statistics')
    st.write(readability_checker(st.session_state.text))

# Handling grammar check
elif grammar:
    matches = grammar_checker(st.session_state.text)
    for match in matches:
        message = match.get('message')
        error_text = match['context']['text'][match['offset']:match['offset'] + match['length']]
        suggestions = [r['value'] for r in match.get('replacements', [])][:3]  # Limit to top 3 suggestions

        st.markdown(f"• **{message}** `{error_text}`")

        # Create a row of buttons for suggestions
        suggestion_buttons = st.columns(len(suggestions))
        for i, suggestion in enumerate(suggestions):
            if suggestion_buttons[i].button(suggestion):
                update_text_area(match, suggestion)

# Text area for input
text_area = st.text_area('Text Field', st.session_state.text, height=200)
