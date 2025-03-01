#!/usr/bin/env python
# coding: utf-8

# In[2]:


import re
import os
import nltk
import streamlit as st
from collections import Counter
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from spellchecker import SpellChecker

# Download necessary NLTK resources
nltk.download("punkt")
nltk.download("stopwords")
nltk.download("wordnet")

# Load and preprocess corpus
file_path = "reuters.txt"
if os.path.exists(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        text = file.read().lower()
else:
    text = ""
    print("⚠️ Warning: 'reuters.txt' not found. Using empty text.")

# Clean text by removing special characters
text = re.sub(r'[^a-z\s]', '', text)
tokens = word_tokenize(text)

# Remove stopwords
stop_words = set(stopwords.words("english"))
filtered_words = [word for word in tokens if word not in stop_words]

# Count word frequencies and filter uncommon words
word_counts = Counter(filtered_words)
cleaned_dictionary = {word for word, count in word_counts.items() if count > 2}

# Save the cleaned dictionary
with open("cleaned_dictionary.txt", "w", encoding="utf-8") as file:
    for word in sorted(cleaned_dictionary):
        file.write(word + "\n")

# Load dictionary for spell checking
dictionary = set()
try:
    with open("cleaned_dictionary.txt", "r", encoding="utf-8") as file:
        dictionary = set(word.strip() for word in file.readlines())
except FileNotFoundError:
    print("⚠️ Warning: 'cleaned_dictionary.txt' not found. Using empty dictionary.")

# Initialize spell checker
spell = SpellChecker()

# Function to check spelling
def check_spelling(text):
    words = text.split()
    misspelled = [word for word in words if word.lower() not in dictionary]
    corrections = {word: spell.correction(word) or "No suggestion" for word in misspelled}
    return corrections

# Streamlit UI
st.title("Spelling Correction System")
user_text = st.text_area("Enter text (max 500 characters):", max_chars=500)

if st.button("Check Spelling"):
    if not user_text.strip():
        st.warning("⚠️ Please enter some text before checking spelling.")
    else:
        corrections = check_spelling(user_text)
        if corrections:
            st.error("Misspelled Words Detected:")
            for word, suggestion in corrections.items():
                st.write(f"❌ {word} → ✅ {suggestion}")
        else:
            st.success("No spelling errors found!")

