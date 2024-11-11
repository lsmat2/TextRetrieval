from inverted_index import build_vocabulary, count_word_in_doc, doc_frequency, doc_length, count_word_in_query

print("3_tdif.py")

vocab = build_vocabulary()
print("Vocabulary size:", len(vocab))
for i, word in enumerate(vocab):
    print(i, word)

query1 = "olympic gold athens"
query2 = "reuters stocks friday"
query3 = "investment market prices"

def tfidf(query):
    query_words = query.split(" ")
    score = 0
    for word in query_words:
        if word in vocab:
            tf = count_word_in_query(word, query)
            df = doc_frequency(word)
            idf = len(vocab) / df
            score += tf * idf