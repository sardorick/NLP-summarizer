import streamlit as st
from utils import *
from wordcloud import WordCloud
from PIL import Image

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

        st.header("WordCloud representation of the text")
        plt.figure(figsize=(20, 20))
        plt.axis('off')
        plt.imshow(WordCloud().generate(original_text))
        plt.savefig('static/wordcloud_streamlit.png', bbox_inches='tight', pad_inches = 0)
        img1 = Image.open("static/wordcloud_streamlit.png")
        st.image(img1)
        st.header("Summarization by using Frequency Algorithm")
        st.markdown(summariz_freq)
        st.header("Summarization by using Luhn Algorithm")
        st.markdown(summariz_luhn)

