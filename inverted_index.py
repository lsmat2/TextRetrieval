import math
print("Inverted index constructed in reducer.py")

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

bm25_k = 5
bm25_b = 0.2

def build_vocabulary():
    vocabulary = {}
    with open("term_lexicon.txt", "r") as file:
        for line in file:
            term, tf, numdocs = line.split(',', 2)
            vocabulary[term] = int(tf)
    # Sort by decreasing term frequency
    most_frequent_words = sorted(vocabulary.items(), key=lambda x: x[1], reverse=True)[:200]
    return most_frequent_words

def count_word_in_doc(word, docid):
    with open("/root/testout/part-00000", "r") as file:
        for line in file:
            term, current_docid, tf = line.split(' ', 2)
            if docid == current_docid and word == term:
                return int(tf)
    return 0

def doc_frequency(word):
    with open("term_lexicon.txt", "r") as file:
        for line in file:
            term, tf, numdocs = line.split(',', 2)
            if word == term:
                return int(numdocs)
    return 0

def doc_length(docid):
    with open("doc_lexicon.txt", "r") as file:
        for line in file:
            current_docid, length = line.split(',', 1)
            if docid == current_docid:
                return int(length)
    return 0

def count_word_in_query(word, query):
    return query.split().count(word)

def doc_relevance(query, docid):
    query_words = set(query.split(" "))
    score = 0
    for word in query_words:
        # get individual components
        cwd = count_word_in_doc(word, docid)
        if cwd == 0: continue
        cwq = count_word_in_query(word, query)
        df = doc_frequency(word)
        doc_len = doc_length(docid)
        # compute idf
        idf = math.log((NUM_DOCS+1)/df)
        # compute tf with length normalization
        tf = cwq*((bm25_k + 1) * cwd) / (cwd + bm25_k*(1-bm25_b+bm25_b*(doc_len/AVDL)))
        # compute score
        score += tf * idf
    return score