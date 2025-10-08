#Importing NLTK modules for part-of speech tagging and chunking 
from nltk import pos_tag, RegexpParser

#Allows importing from Jupyter notebooks 
import import_ipynb

#Importing NLTK word and sentence tokenizers 
from nltk.tokenize import word_tokenize, sent_tokenize

#Downloading the punkt tokeinzer module (used for sentence and word tokenization)
import nltk
nltk.download('punkt_tab')
# Download NLTK's averaged perceptron tagger, which assigns part-of-speech labels (like noun, verb, adjective) to each word
nltk.download('averaged_perceptron_tagger_eng')

# importing dorian gray text from project using utf-8 encoding to ensure special characters are read correctly
text = open("dorian_gray.txt",encoding='utf-8').read().lower()

# Tokenize text into sentences
sentences = sent_tokenize(text)

# Define chunk grammars
np_grammar = "NP: {<DT>?<JJ>*<NN>}"
vp_grammar = "VP: {<DT>?<JJ>*<NN><VB.*><RB.?>?}"

# Create chunk parsers
np_parser = RegexpParser(np_grammar)
vp_parser = RegexpParser(vp_grammar)

# Process each sentence: tokenize, tag, chunk
for sentence in sentences[:5]:  # Limiting  to first 5 for readability sake
    words = word_tokenize(sentence)
    tagged = pos_tag(words)

    np_chunked = np_parser.parse(tagged)
    vp_chunked = vp_parser.parse(tagged)

   

#Outputs custom grammar rules applied to each sentence
    print("Noun Phrase Chunk Tree:")
    print(np_chunked)

    print("Verb Phrase Chunk Tree:")
    print(vp_chunked)

