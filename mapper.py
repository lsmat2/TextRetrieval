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

# 1) transform words to lower-case
# 2) remove punctuation, numbers and excess whitespace
# 3) Remove stop-words & numbers
# 4) and do stemming of the words
# 5) count the words in the documents

# 6) You will need to modify the code to ensure the value not only contains
#    the word frequencies but also the list of documents where the word appears 
#    (see the class slides/discussion for clarification and pseudocode) 
#    because you will need to build the scores for each pair query-document

total_doc_len = 0
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

  # output key(term) value(docid:word_counts_in_doc)
  for word in wordcounts:
    val = str(docid) + ":" + str(wordcounts[word]) 
    print('%s\t%s' % (word, val)) # (term, docid, tf)
  
  # store doc lengths in separate file
  file.write('%s, %s\n' % (docid, len(wordcounts)))

  # update total doc length and increment doc id
  total_doc_len += len(wordcounts)
  docid +=1

file.close()
# calculate number of documents and average document length
num_docs = docid - 1
avdl = int(total_doc_len / num_docs)
file = open("info.txt", "w")
file.write('NumDocs, AvgDocLength, NumWords:\n%s, %s, %s' % (num_docs, avdl, total_doc_len))
file.close()