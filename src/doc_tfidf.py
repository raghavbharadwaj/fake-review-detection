import nltk
import string
import os

from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.stem.porter import PorterStemmer

path = 'words'
token_dict = {}
stemmer = PorterStemmer()
def stem_tokens(tokens, stemmer):
	stemmed = []
	for item in tokens:
		stemmed.append(stemmer.stem(item))
	return stemmed
def tokenize(text):
	tokens = nltk.word_tokenize(text)
	stems = stem_tokens(tokens, stemmer)
	return stems
for subdir, dirs, files in os.walk(path):
	for file in files:
		file_path = subdir + os.path.sep + file
		shakes = open(file_path, 'r')
		text = shakes.read()
		lowers = text.lower()
		no_punctuation = lowers.translate(None, string.punctuation)
		token_dict[file] = no_punctuation
       
tfidf = TfidfVectorizer(tokenizer=tokenize, stop_words='english')
tfs = tfidf.fit_transform(token_dict.values())
p_s = tfs * tfs.T
print(p_s)
