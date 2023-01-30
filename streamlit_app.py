import streamlit as st
from utils import *


st.header("Text summarizer")
review = st.text_area("Enter the text to be summarized")
percentage = st.number_input("Enter the percentage to be summarized (from 0.1 to 1)", step=0.1)

if st.button('Summarize'):

    if review.isspace() or len(review) == 0:
        st.markdown('**No text provided!** Please enter some text and then hit Summarize')
        
    else:
        original_text =  review
        summariz_freq = summarize_by_freq(original_text, percentage)
        summariz_luhn = summarize_by_luhn(original_text, percentage)


        st.header("Summarization by using Frequency Algorithm")
        st.markdown(summariz_freq)
        st.header("Summarization by using Luhn Algorithm")
        st.markdown(summariz_luhn)