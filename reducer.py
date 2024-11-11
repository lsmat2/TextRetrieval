# Code based on https://blog.devgenius.io/big-data-processing-with-hadoop-and-spark-in-python-on-colab-bff24d85782f
from operator import itemgetter
import sys

current_word = None
current_count = 0
word = None
current_numdocs_in = 0
file = open("term_lexicon.txt", "w")

# input comes from STDIN
for line in sys.stdin:
    # remove leading and trailing whitespace
    line = line.strip()
    line=line.lower()

    # parse the input we got from mapper.py
    word, val = line.split('	', 1)
    docid, count = val.split(' ', 1)
    
    try: count = int(count)
    except ValueError: continue #count was not a number, so silently ignore/discard this line

    # this IF-switch only works because Hadoop sorts map output by key (here: word) before it is passed to the reducer
    if current_word == word:
        current_count += count
        current_numdocs_in += 1
        print('%s %s %s' % (word, docid, count))
        
    else:
        if current_word: 
            file.write('%s, %s, %s\n' % (current_word, current_count, current_numdocs_in))
        current_count = count
        current_word = word
        current_numdocs_in = 1
        print('%s %s %s' % (word, docid, count))
        
# do not forget to output the last word if needed!
if current_word == word:
    print('%s %s %s' % (word, docid, count))
file.close()