from inverted_index import build_vocabulary, tfidf_doc_relevance
import numpy as np

print("3_tdif.py")

NUM_DOCS = 0
AVDL = 0
with open("info.txt", "r") as file:
    info_line = True
    for line in file:
        if info_line: 
            info_line = False
            continue
        num_docs, avdl = line.split(', ', 1)
        NUM_DOCS = int(num_docs)
        AVDL = int(avdl)

vocab = build_vocabulary()
print("Vocabulary size:", len(vocab))
for i, word in enumerate(vocab):
    print(i, word)

queries = ["reuters stocks friday", "olympic gold athens", "investment market prices"]

def tfidf(queries):
    for query in queries:
        print("\nQuery:", query)
        relevances = execute_search_TF_IDF(query)
        print("relevances:", relevances)
        print_top_and_bottom_5(relevances)


def execute_search_TF_IDF(query):
    relevances = np.zeros(NUM_DOCS) #Initialize relevances of all documents to 0
    for docid in range(NUM_DOCS):
        relevances[docid] = tfidf_doc_relevance(query, (docid+1))
    return relevances # in the same order of the documents in the dataset

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

tfidf(queries)