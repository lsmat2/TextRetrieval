import math
print("Inverted index constructed in reducer.py")

# { docid -> length(docid) }
def get_doc_lexicon():
    doc_lexicon = {}
    with open("doc_lexicon.txt", "r") as file:
        for line in file:
            docid, length = line.split(',', 1)
            doc_lexicon[docid] = int(length)
    return doc_lexicon

# { term -> (term_frequency, "docid:count, docid:count, ...") }
def build_vocabulary():
    vocabulary = {}
    with open("/root/testout/part-00000", "r") as file:
        for line in file:
            # Retrieve info
            term, tf, docids_and_counts = line.split('\t', 2)
            # Process docids_and_counts string into an object
            obj_list = []
            docids_and_counts = docids_and_counts.replace("[", "").replace("]", "")
            docid_str_list = docids_and_counts.split(", ")
            for docid_df_pair in docid_str_list:
                docid_df_pair = docid_df_pair.replace("'", "").replace("'", "")
                docid, count = docid_df_pair.split(":")
                pair = (int(docid), int(count))
                obj_list.append(pair)
            # Add term info to vocabulary
            vocabulary[term] = (int(tf), obj_list)
    # Sort by decreasing term frequency
    most_frequent_words = sorted(vocabulary.items(), key=lambda x: x[1][0], reverse=True)[:200]
    top_200vocab = {}
    for word in most_frequent_words:
        top_200vocab[word[0]] = word[1]
    return top_200vocab

# { term -> collection_probability }
def get_collection_probabilities():
    collection_probs = {}
    total_doc_len = 0
    with open("/root/testout/part-00000", "r") as file:
        for line in file:
            term, tf, _ = line.split('\t', 2)
            # Add term info to vocabulary
            collection_probs[term] = int(tf)
            total_doc_len += int(tf)
    for term in collection_probs:
        collection_probs[term] /= total_doc_len
    return collection_probs