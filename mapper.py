#Code based on https://blog.devgenius.io/big-data-processing-with-hadoop-and-spark-in-python-on-colab-bff24d85782f
import sys
import io
import re
import nltk
import pandas as pd
from nltk.stem import PorterStemmer

nltk.download('stopwords',quiet=True)
from nltk.corpus import stopwords
punctuations = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
stop_words = set(stopwords.words('english'))
input_stream = io.TextIOWrapper(sys.stdin.buffer, encoding='latin1')
stemmer = PorterStemmer()
file = open("doc_lexicon.txt", "w")

NUM_DOCS = 0
AVDL = 0
# 1) transform words to lower-case
# 2) remove punctuation, numbers and excess whitespace
# 3) Remove stop-words & numbers
# 4) and do stemming of the words
# 5) count the words in the documents

# 6) You will need to modify the code to ensure the value not only contains
#    the word frequencies but also the list of documents where the word appears 
#    (see the class slides/discussion for clarification and pseudocode) 
#    because you will need to build the scores for each pair query-document

docid = 1 #actually line id
for line in input_stream:
  # preprocess doc description
  line = line.split(',', 3)[2]
  line = line.strip() # 2
  line = re.sub(r'[^\w\s]', '',line) # 2
  line = line.lower() # 1
  for x in line:
    if x in punctuations:
      line=line.replace(x, " ") # 2

  # tokenize and build word count dict
  wordcounts = {}
  for word in line.split():
    word = word.lower().strip() # 1
    if word in stop_words or word.isnumeric(): continue # 2, 3
    word = re.sub(r'\d+', '', word) # 2
    word = stemmer.stem(word.strip()) # 4
    if len(word) < 3: continue # 3
    if word not in wordcounts: wordcounts[word] = 1 # 5
    else: wordcounts[word] += 1 # 5

  # output word counts and store doc length
  for word in wordcounts:
    print('%s	%s %s' % (word, docid, wordcounts[word])) # (term, docid, tf)
  file.write*('%s, %s\n' % (docid, len(wordcounts)))
  AVDL += len(wordcounts)
  docid +=1
NUM_DOCS = docid - 1
AVDL = int(AVDL / NUM_DOCS)