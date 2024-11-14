import math
import numpy as np
from nltk.stem import PorterStemmer
from inverted_index import build_vocabulary, get_doc_lexicon, get_collection_probabilities
print("4_jm_smoothing.py")


LAMBDA = 0.5 # Jelinek-Mercer smoothing parameter [0, 1]
# 0: no smoothing (no consideration for words not in doc), 1: full smoothing (depends only on collection probabilities)
NUM_DOCS = 0
AVDL = 0
TOTAL_DOC_LEN = 0
vocab = build_vocabulary()
doc_lexicon = get_doc_lexicon()
collection_lm = get_collection_probabilities()
stemmer = PorterStemmer()
with open("info.txt", "r") as file:
    info_line = True
    for line in file:
        if info_line: 
            info_line = False
            continue
        num_docs, avdl, total_doc_len = line.split(', ', 2)
        NUM_DOCS = int(num_docs)
        AVDL = float(avdl)
        TOTAL_DOC_LEN = int(total_doc_len)

# Helper Functions
def print_document(rank, relevance, doc_id):
    print(f"{rank} docid {doc_id}, score: {relevance}")

def print_top_and_bottom_5(relevance_docs):
    temp_relevance_docs = relevance_docs.copy()
    print("\nTop 5 most relevant documents:\n-----------------------")
    for i in range(5):
        top_index = 0
        for j in range(len(temp_relevance_docs)):
            if temp_relevance_docs[j] > temp_relevance_docs[top_index]: top_index = j
        print_document(i+1, temp_relevance_docs[top_index], top_index)
        temp_relevance_docs[top_index] = -1

    print("\nBottom 5 least relevant documents:\n-----------------------")
    for i in range(5):
        bottom_index = 0
        for j in range(len(temp_relevance_docs)):
            if temp_relevance_docs[j] < temp_relevance_docs[bottom_index] and temp_relevance_docs[j] > -1: bottom_index = j
        print_document(i+1, temp_relevance_docs[bottom_index], bottom_index)
        temp_relevance_docs[bottom_index] = 9999

def generate_queries(num_queries):
    queries = []
    for _ in range(num_queries):
        query_length = np.random.randint(4, 6)  # Random query length between 3 and 6 words
        query = " ".join(np.random.choice(list(vocab.keys()), query_length))
        queries.append(query)
    return queries

def add_query_to_vocab(word):
    global vocab
    with open("/root/testout/part-00000", "r") as file:
        for line in file:
            term, tf, docids_and_counts = line.split('\t', 2)
            if term == word:
                # Process docids_and_counts string into an object
                obj_list = []
                docids_and_counts = docids_and_counts.replace("[", "").replace("]", "")
                docid_str_list = docids_and_counts.split(", ")
                for docid_df_pair in docid_str_list:
                    docid_df_pair = docid_df_pair.replace("'", "").replace("'", "")
                    docid, count = docid_df_pair.split(":")
                    pair = (int(docid), int(count))
                    obj_list.append(pair)
                # Add term info to vocab
                vocab[term] = (int(tf), obj_list)
                return 1
    return 0

def count_word_in_doc(word, docid):
    word_info = vocab[word]
    docids_and_counts = word_info[1]
    for docid_and_count in docids_and_counts:
        if int(docid_and_count[0]) == docid:
            return int(docid_and_count[1])
    return 0

def prob_word_in_doc1(word, docid):
    cwd = count_word_in_doc(word, docid)
    doc_len = doc_lexicon[str(docid)]
    if doc_len == 0: doc_len = 1 # Avoid division by 0 when 'doc_len' is 0 due to preprocessing
    pwc = collection_lm[word]
    # Jelinek-Mercer Term Smoothing
    JM_score = (1 - LAMBDA) * (cwd / doc_len) + (LAMBDA * pwc)
    # print(f"word: {word}, cwd: {cwd}, doc_len: {doc_len}, pwc: {pwc}, JM_score: {JM_score}")
    return JM_score

def prob_word_in_doc2(word, docid):
    cwd = count_word_in_doc(word, docid)
    doc_len = doc_lexicon[str(docid)]
    pwc = collection_lm[word]
    # Jelinek-Mercer Term Smoothing (alternative)
    JM_score = math.log(1 + ((1-LAMBDA)/LAMBDA) * (cwd / (doc_len*pwc)))
    return JM_score


# Computing Probabilistic Relevance with JM Smoothing
def JM_doc_relevance(query, docid):
    query_words = query.split()
    score = 0
    for word in query_words:
        word = stemmer.stem(word.strip())
        if word not in vocab: 
            if add_query_to_vocab(word) == 0: continue # if we don't find this word anywhere in any document, skip it
        score += prob_word_in_doc1(word, docid)
    return score

def execute_search_JM(query):
    relevances = np.zeros(NUM_DOCS) #Initialize relevances of all documents to 0
    for docid in range(NUM_DOCS):
        relevances[docid] = JM_doc_relevance(query, (docid+1))
    return relevances # in the same order of the documents in the dataset

def JM(queries):
    for query in queries:
        print("\nQuery:", query)
        relevances = execute_search_JM(query)
        print_top_and_bottom_5(relevances)
    
queries = ["reuters stocks friday", "olympic gold athens", "investment market prices"]
JM(queries)
print("\nGiven queries search complete.")
print("\nRunning 1 random query...")
random_queries = generate_queries(1)
JM(random_queries)