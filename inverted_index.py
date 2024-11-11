import math
from nltk.stem import PorterStemmer
stemmer = PorterStemmer()
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

# { term -> (tf(term), df(term)) }
def get_term_lexicon():
    term_lexicon = {}
    with open("term_lexicon.txt", "r") as file:
        for line in file:
            term, tf, numdocs = line.split(',', 2)
            term_lexicon[term] = (int(tf), int(numdocs))
    return term_lexicon
# { docid -> length(docid) }
def get_doc_lexicon():
    doc_lexicon = {}
    with open("doc_lexicon.txt", "r") as file:
        for line in file:
            docid, length = line.split(',', 1)
            doc_lexicon[docid] = int(length)
    return doc_lexicon
# [ (term, docid, tf), ... ]
def get_postings():
    postings = []
    # with open("/root/testout/part-00000", "r") as file:
    #     for line in file:
    #         term, docid, tf = line.split(' ', 2)
    #         tuple = (term, docid, int(tf))
    #         postings.append(tuple)
    return postings

term_lexicon = get_term_lexicon()
doc_lexicon = get_doc_lexicon()
postings = get_postings()

def build_vocabulary():
    vocabulary = {}
    with open("/root/testout/part-00000", "r") as file:
        for line in file:
            term, tf, docids_and_counts = line.split('\t', 2)
            # print(f"term: {term}, tf: {tf}, docids_and_counts: {docids_and_counts}")
            vocabulary[term] = (int(tf), docids_and_counts)
    # Sort by decreasing term frequency
    most_frequent_words = sorted(vocabulary.items(), key=lambda x: x[1][0], reverse=True)[:200]
    return most_frequent_words

def count_word_in_doc(word, docid):
    index = 0
    while index < len(postings):
        # Go through postings to find wordcount in doc
        posting = postings[index]
        postingterm = posting[0]
        posting_docid = posting[1]
        posting_tf = posting[2]

        # If we find the word in the postings, increment by 1 until finding the matching docid
        # Otherwise, increment by how many postings of incorrect word we have to skip
        if postingterm == word:
            if posting_docid == docid: return posting_tf
        else:  
            if postingterm in term_lexicon: index += (term_lexicon[postingterm][1] - 1)
        index += 1    
    return 0

def doc_frequency(word):
    if word in term_lexicon: return term_lexicon[word][1]
    else: return 0

def doc_length(docid):
    return float(doc_lexicon[docid])

def count_word_in_query(word, query):
    return query.split().count(word)

def tfidf_doc_relevance(query, docid):
    query_words = query.split(" ")
    score = 0
    for word in query_words:
        word = stemmer.stem(word.strip())
        # get individual components
        cwd = count_word_in_doc(word, docid)
        if cwd == 0: continue
        cwq = count_word_in_query(word, query)
        df = doc_frequency(word)
        doc_len = doc_length(docid)
        # compute idf
        idf = math.log((NUM_DOCS+1.0)/df)
        # compute tf with length normalization
        tf = cwq*((bm25_k + 1) * cwd) / (cwd + bm25_k*(1.0-bm25_b+bm25_b*(doc_len/AVDL)))
        print(f"word: {word}, cwd: {cwd}, cwq: {cwq}, df: {df}, doc_len: {doc_len}, idf: {idf}, tf: {tf}")
        # compute score
        score += tf * idf
    print("docid:", docid, "score:", score)
    return score