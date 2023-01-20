import re
import nltk
import heapq
import string
import numpy as np
import networkx as nx
# from goose3 import Goose
from nltk.cluster.util import cosine_distance
import PyPDF2
from PIL import Image
import pytesseract
from wordcloud import WordCloud
import matplotlib.pyplot as plt

nltk.download('stopwords')

stopwords = nltk.corpus.stopwords.words('english')

# Text from image
def text_from_image(path_to_image):
    image = Image.open(path_to_image)
    text = pytesseract.image_to_string(image, lang='eng', config=r"--psm 11 --oem 3")
    text = text.replace('\n', ' ').replace(' .', '.').replace(" '", "'").replace(' ?', '?').replace('|', 'I').replace('  ', ' ')

# Text from pdf
def text_from_pdf(path):
    file = open(path, 'rb')
    pdfdoc = PyPDF2.PdfFileReader(file)
    number_of_pages = pdfdoc.getNumPages()
    full_content = ''
    for i in range(number_of_pages):
        page_content = pdfdoc.getPage(i).extractText()
        full_content = full_content + page_content + ' '
    return full_content

# Text from URL
# def text_from_url(url):
#     goose = Goose()
#     extracted_text = goose.extract(url)
#     cleaned_data = extracted_text.cleaned_text
#     return cleaned_data

# Preprocessing
def preprocess(sentence):
    formatted_text = sentence.lower()
    tokens = []
    for token in nltk.word_tokenize(formatted_text):
        tokens.append(token)
    tokens = [word for word in tokens if word not in stopwords and word not in string.punctuation]
    formatted_text = ' '.join(element for element in tokens)
    return formatted_text

# Summarize by frequency
def summarize_by_freq(original_text, summary_percentage=0.3):
    original_text = re.sub(r'\s+', ' ', original_text)
    processed_text = preprocess(original_text)
    word_frequency = nltk.FreqDist(nltk.word_tokenize(processed_text))
    highest_frequency = max(word_frequency.values())
    sentence_list = nltk.sent_tokenize(original_text)
    percentage = int(summary_percentage * len(sentence_list))
    for word in word_frequency.keys():
        word_frequency[word] = (word_frequency[word] / highest_frequency)
    score_sentences = {}
    for sentence in sentence_list:
        for word in nltk.word_tokenize(sentence.lower()):
            if sentence not in score_sentences.keys():
                score_sentences[sentence] = word_frequency[word]
            else:
                score_sentences[sentence] += word_frequency[word]
    best_sentences = heapq.nlargest(percentage, score_sentences, key=score_sentences.get)
    summary = ' '.join(best_sentences)
    return summary

# Calculate sentences score
def calculate_sentences_score(sentences, important_words, distance):
    scores = []
    sentence_index = 0
    for sentence  in [nltk.word_tokenize(sentence) for sentence in sentences]:
        word_index = []
        for word in important_words:
            try:
                word_index.append(sentence.index(word))
            except ValueError:
                pass
        word_index.sort()
        if len(word_index) == 0:
            continue
        groups_list = []
        group = [word_index[0]]
        i = 1
        while i < len(word_index):
            if word_index[i] - word_index[i-1] < distance:
                group.append(word_index[i])
            else:
                groups_list.append(group[:])
                group = [word_index[i]]
            i += 1
            groups_list.append(group)
        max_group_score = 0
        for g in groups_list:
            important_words_in_group = len(g)
            total_words_in_group = g[-1] - g[0] + 1
            score = 1.0 * important_words_in_group ** 2 / total_words_in_group
            if score > max_group_score:
                max_group_score = score
        scores.append((max_group_score, sentence_index))
        sentence_index += 1
    return scores

# Summarize by luhn
def summarize_by_luhn(original_text, summary_percentage = 0.3):
    original_sentences = [sentence for sentence in nltk.sent_tokenize(original_text)]
    formatted_sentences = [preprocess(original_sentence) for original_sentence in original_sentences]
    words = [word for sentence in formatted_sentences for word in nltk.word_tokenize(sentence)]
    frequency = nltk.FreqDist(words)
    if len(words) > 1500:
        top_n_words = int(len(words) * 0.10)
        distance = int(len(words) * 0.008)
    else:
        top_n_words = 15 
        distance = 8
    top_n_words = [word[0] for word in frequency.most_common(top_n_words)]
    sentences_score = calculate_sentences_score(formatted_sentences, top_n_words, distance)
    sentence_list = nltk.sent_tokenize(original_text)
    best_sentences = heapq.nlargest(int(len(formatted_sentences) * summary_percentage), sentences_score)
    best_sentences = [original_sentences[i] for (score, i) in best_sentences]
    best_sentences_list = []
    for sentence in sentence_list:
        for best_sent in best_sentences:
            if best_sent in sentence:
                best_sentences_list.append(sentence)
    summary = ' '.join(best_sentences_list)
    return summary

# Plotting the wordcloud
def plot_wordcloud(document):
    plt.figure(figsize=(20, 20))
    plt.axis('off')

    plt.imshow(WordCloud().generate(document))
    plt.savefig('static/wordcloud.png', bbox_inches='tight', pad_inches = 0)
    return

# Calculate the similarity of sentences
def calculate_sentence_similarity(sentence1, sentence2):
    words1 = [word for word in nltk.word_tokenize(sentence1)]
    words2 = [word for word in nltk.word_tokenize(sentence2)]
    all_words = list(set(words1+words2))
    vector1 = [0] * len(all_words)
    vector2 = [0] * len(all_words)
    for word in words1:
        vector1[all_words.index(word)] += 1
    for word in words2:
        vector2[all_words.index(word)] += 1
    return 1 - cosine_distance(vector1, vector2)

# Calculate similarity matrix
def calculate_similarity_matrix(sentences):
    similarity_matrix = np.zeros((len(sentences), len(sentences)))
    for i in range(len(sentences)):
        for j in range(len(sentences)):
            if i == j:
                continue
        similarity_matrix[i][j] = calculate_sentence_similarity(sentences[i], sentences[j])
    return similarity_matrix
