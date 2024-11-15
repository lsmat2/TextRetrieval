import numpy as np
import math
from inverted_index import build_vocabulary, get_doc_lexicon
from nltk.stem import PorterStemmer
print("3_tdif.py")

stemmer = PorterStemmer()
vocab = build_vocabulary()
doc_lexicon = get_doc_lexicon()
bm25_k = 5
bm25_b = 0.2
NUM_DOCS = 0
AVDL = 0
TOTAL_DOC_LEN = 0
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

# TF-IDF helpers
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
def doc_frequency(word): return len(vocab[word][1])
def doc_length(docid): return doc_lexicon[str(docid)][0]

def tfidf_doc_relevance(query, docid):
    query_words = query.split(" ")
    score = 0
    for word in query_words:
        word = stemmer.stem(word.strip())
        # add query word to vocab if not already
        if word not in vocab:
            if add_query_to_vocab(word) == 0: continue # if we don't find this word anywhere in any document, skip it
        # get individual components
        cwd = count_word_in_doc(word, docid)
        if cwd == 0: continue
        df = doc_frequency(word)
        doc_len = doc_length(docid)
        # compute idf
        idf = math.log((NUM_DOCS+1.0)/df)
        # compute tf with length normalization
        tf = ((bm25_k + 1) * cwd) / (cwd + bm25_k*(1.0-bm25_b+bm25_b*(doc_len/AVDL)))
        # print(f"word: {word}, cwd: {cwd}, df: {df}, doc_len: {doc_len}, idf: {idf}, tf: {tf}")
        # compute score
        score += tf * idf
    # print("docid:", docid, "score:", score)
    return score

# Computing TF-IDF
def tfidf(queries):
    for query in queries:
        print("\nQuery:", query)
        relevances = execute_search_TF_IDF(query)
        print_top_and_bottom_5(relevances)

def execute_search_TF_IDF(query):
    relevances = np.zeros(NUM_DOCS) #Initialize relevances of all documents to 0
    for docid in range(NUM_DOCS):
        relevances[docid] = tfidf_doc_relevance(query, (docid+1))
    return relevances # in the same order of the documents in the dataset

def print_document(rank, relevance, doc_id):
    print(f"{rank} Title: {doc_lexicon[str(doc_id+1)][1]}, Score: {relevance}")

def print_top_and_bottom_5(relevance_docs):
    temp_relevance_docs = relevance_docs.copy()
    print("\nTop 5 most relevant documents:\n-----------------------")
    seen_docids = set()
    for i in range(5):
        top_index = 0
        for j in range(len(temp_relevance_docs)):
            if j in seen_docids: continue
            if temp_relevance_docs[j] >= temp_relevance_docs[top_index]: top_index = j
        print_document(i+1, temp_relevance_docs[top_index], top_index)
        seen_docids.add(top_index)

    print("\nBottom 5 least relevant documents:\n-----------------------")
    for i in range(5):
        bottom_index = 0
        for j in range(len(temp_relevance_docs)):
            if j in seen_docids: continue
            if temp_relevance_docs[j] <= temp_relevance_docs[bottom_index] and temp_relevance_docs[j] > -1: bottom_index = j
        print_document(i+1, temp_relevance_docs[bottom_index], bottom_index)
        seen_docids.add(bottom_index)

def generate_queries(num_queries):
    queries = []
    for _ in range(num_queries):
        query_length = np.random.randint(4, 6)  # Random query length between 3 and 6 words
        query = " ".join(np.random.choice(list(vocab.keys()), query_length))
        queries.append(query)
    return queries

queries = ["reuters stocks friday", "olympic gold athens", "investment market prices"]
tfidf(queries)
print("\nGiven queries search complete.")
print("\nRunning 1 random query...")
random_queries = generate_queries(1)
tfidf(random_queries)