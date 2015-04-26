import nltk
import string
import os
import sklearn
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics.pairwise import linear_kernel
from nltk.stem.porter import PorterStemmer
import numpy
import math

path = '/var/root/projects/nlp_project/fake-review-detection/src/subset-1'
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
#p_s = tfs * tfs.T
for eachfile in sorted(os.listdir(path)):
	eachopen = open(path+'/'+eachfile,'r')
	str1 = str(eachopen.read())
	parentname = str(eachopen).split(',')[0].split('/')[-1].split('\'')[0]
	u = []		
	response = tfidf.transform([str1])
	for col in response.nonzero()[1]:
		u.append(response[0, col])
	for eachfile1 in sorted(os.listdir(path)):
		eachopen1 = open (path+'/'+eachfile1,'r')
		str2 = str(eachopen1.read())
		v = []
		temp_u = u
		response2 = tfidf.transform([str2])
		for col in response2.nonzero()[1]:
			v.append(response2[0, col])
		if len(u) < len(v):
			v = v[:len(u)]
		if len(v) < len(u):
			temp_u = u[:len(v)]
		dist = numpy.dot(temp_u,v)
		childname = str(eachopen1).split(',')[0].split('/')[-1].split('\'')[0]
		print(parentname+':'+childname+':'+str(dist))
		eachopen1.close()
	eachopen.close()

