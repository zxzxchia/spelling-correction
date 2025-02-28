#!/usr/bin/env python
# coding: utf-8

# In[6]:


get_ipython().system('python -m spacy download en_core_web_sm')


# In[7]:


import re
import nltk
import spacy
from collections import Counter
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

# Download necessary resources
nltk.download("punkt")
nltk.download("stopwords")
nltk.download("wordnet")

# Load spaCy NLP model
nlp = spacy.load("en_core_web_sm")

# Load and preprocess the Reuters corpus
def load_corpus(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        text = file.read().lower()

    # Remove special characters and numbers
    text = re.sub(r'[^a-z\s]', '', text)

    # Tokenize and remove stopwords
    tokens = word_tokenize(text)
    stop_words = set(stopwords.words("english"))
    words = [word for word in tokens if word not in stop_words]

    return words

# Load words from corpus
words = load_corpus("reuters.txt")

# Count word frequencies
word_counts = Counter(words)

# Remove uncommon words (appearing only once)
filtered_words = {word for word, count in word_counts.items() if count > 2}

# Remove short words (length <= 2) except common words
common_short_words = {"is", "an", "at", "as", "to", "by", "in", "on", "am", "it"}
filtered_words = {word for word in filtered_words if len(word) > 2 or word in common_short_words}

# Remove proper nouns using spaCy NER
def remove_proper_nouns(word_list):
    cleaned_words = []
    for word in word_list:
        doc = nlp(word)
        if not any(token.pos_ == "PROPN" for token in doc):  # If word is NOT a proper noun
            cleaned_words.append(word)
    return cleaned_words

# Apply NER-based filtering
cleaned_dictionary = remove_proper_nouns(filtered_words)

# Save the cleaned dictionary
with open("cleaned_dictionary.txt", "w", encoding="utf-8") as file:
    for word in sorted(cleaned_dictionary):
        file.write(word + "\n")

print(f"✅ Cleaned dictionary created with {len(cleaned_dictionary)} words.")


# In[11]:


from spellchecker import SpellChecker

spell = SpellChecker()

def check_spelling(text):
    words = text.split()
    misspelled = [word for word in words if word.lower() not in dictionary]

    corrections = {}
    for word in misspelled:
        corrections[word] = spell.correction(word) if spell.correction(word) else "No suggestion"

    return corrections



# In[14]:


import streamlit as st

# Sample function to check spelling
def check_spelling(text):
    # Example correction dictionary (this should be replaced with real spell checking logic)
    corrections = {"speling": "spelling", "incorect": "incorrect"}
    words = text.split()
    
    detected_mistakes = {word: corrections.get(word, "No suggestion") for word in words if word in corrections}
    return detected_mistakes

# Function to highlight misspelled words
def highlight_misspelled(text, corrections):
    words = text.split()
    highlighted_text = " ".join([f":red[{word}]" if word in corrections else word for word in words])
    return highlighted_text

# Streamlit UI
st.title("Spelling Correction System")

# User text input
user_text = st.text_area("Enter text (max 500 characters):", max_chars=500)

if st.button("Check Spelling"):
    corrections = check_spelling(user_text)  # Ensure corrections is defined
    
    if corrections:  # Now it won't raise an error
        st.error("Misspelled Words Detected:")
        for word, suggestion in corrections.items():
            st.write(f"❌ {word} → ✅ {suggestion}")

        # Highlight misspelled words in text
        st.markdown(highlight_misspelled(user_text, corrections), unsafe_allow_html=True)
    else:
        st.success("No spelling errors found!")



# In[13]:


def highlight_misspelled(text, corrections):
    words = text.split()
    highlighted_text = " ".join([f":red[{word}]" if word in corrections else word for word in words])
    return highlighted_text

if corrections:
    st.markdown(highlight_misspelled(user_text, corrections), unsafe_allow_html=True)

