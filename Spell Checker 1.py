#!/usr/bin/env python
# coding: utf-8

# In[1]:


import re
import nltk
import spacy
import os
from collections import Counter
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from spellchecker import SpellChecker
import streamlit as st

# Download necessary resources
nltk.download("punkt")
nltk.download("stopwords")
nltk.download("wordnet")

# Load spaCy NLP model safely
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    import spacy.cli
    spacy.cli.download("en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")

# Load and preprocess corpus
file_path = "reuters.txt"
if os.path.exists(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        text = file.read().lower()
else:
    text = ""
    print("⚠️ Warning: 'reuters.txt' not found.")

text = re.sub(r'[^a-z\s]', '', text)
tokens = word_tokenize(text)
stop_words = set(stopwords.words("english"))
words = [word for word in tokens if word not in stop_words]
word_counts = Counter(words)

# Remove uncommon words & short words
filtered_words = {word for word, count in word_counts.items() if count > 2}
common_short_words = {"is", "an", "at", "as", "to", "by", "in", "on", "am", "it"}
filtered_words = {word for word in filtered_words if len(word) > 2 or word in common_short_words}

# Remove proper nouns
def remove_proper_nouns(word_list):
    return [word for word in word_list if not any(token.pos_ == "PROPN" for token in nlp(word))]

cleaned_dictionary = remove_proper_nouns(filtered_words)

# Save cleaned dictionary
with open("cleaned_dictionary.txt", "w", encoding="utf-8") as file:
    for word in sorted(cleaned_dictionary):
        file.write(word + "\n")

# Load dictionary safely
dictionary = set()
try:
    with open("cleaned_dictionary.txt", "r", encoding="utf-8") as file:
        dictionary = set(word.strip() for word in file.readlines())
except FileNotFoundError:
    print("⚠️ Warning: 'cleaned_dictionary.txt' not found.")

spell = SpellChecker()

# Spell-checking function
def check_spelling(text):
    words = text.split()
    return {word: spell.correction(word) or "No suggestion" for word in words if word.lower() not in dictionary}

# Streamlit UI
st.title("Spelling Correction System")
user_text = st.text_area("Enter text (max 500 characters):", max_chars=500)

if st.button("Check Spelling"):
    if not user_text.strip():
        st.warning("⚠️ Please enter some text.")
    else:
        corrections = check_spelling(user_text)
        st.error("Misspelled Words Detected:" if corrections else "No errors found!")
        for word, suggestion in corrections.items():
            st.write(f"❌ {word} → ✅ {suggestion}")

