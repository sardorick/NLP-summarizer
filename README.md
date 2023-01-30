# Summarizer

This project is a text summarizer that uses Python and the Natural Language Toolkit (NLTK) library to automatically generate a short and concise summary of a given text. The summarizer leverages advanced NLP techniques to analyze the text and identify the most important sentences and information, which are then combined to form the summary. The goal of the project is to make it easier for people to quickly understand the key points of large or complex texts, saving time and improving their overall reading experience.

## Table of contents

* [General Info](#general-info)
* [Technologies](#technologies)
* [Setup](#setup)

## General Info

The project is a Flask web application that has been created in order to use the NLTK library to summarize big bodies of text. For the time being, there are possibilities to summarize the input text, read PDF files and summarize it and to summarize texts from URL links. 
<img src="/static/screen1.jpg" alt="Alt text">


## Technologies

Project is created with:
* Python
* NLTK
* WordCloud
* Pytesseract
* Streamlit
* Matplotlib
* PyPDF2
* Flask
* SQLAlchemy

## Setup

To access the project, I have prepared a Streamlit interface: [Streamlit](https://sardorick-bw1-yelp-database-streamlit-app-sardorbek-dmqnww.streamlit.app/). You can access it and use the functions of the app without needing to launch the whole web app itself. 

In order to access the web application, go to the directory and run the following code on the terminal:
```python app.py```

You can access the Summarizer page of the app to use it. 

## Roadmap

I am planning to implement some features that include being able to summarize texts and paraphrase at the same time.

## Contact

Project Link: [https://github.com/sardorick/NLP-summarizer](https://github.com/sardorick/NLP-summarizer)