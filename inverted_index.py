from mapper import NUM_DOCS
print("Inverted index constructed in reducer.py")

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