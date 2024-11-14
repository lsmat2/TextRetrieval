import requests
from bs4 import BeautifulSoup
import re
from nltk import PorterStemmer
print("5_crawler.py")
stemmer = PorterStemmer()


def process_text(text:str) -> str:
    ### Remove punctuation, digits, and special characters, convert to lowercase

    text = text.lower()
    punctuation = [",", ".", "!", "?", "(", ")", "[", "]", "{", "}", ":", ";", "'", '"', "`", "“", "”"]
    digits = [str(i) for i in range(10)]
    special_chars = ["\n", "\t", "\r", "\x0b", "\x0c"]
    removable_chars = punctuation + digits + special_chars
    for char in removable_chars:
        text = text.replace(char, "")
    return text

def tokenize_text(text:str) -> list[str]:
    ### Tokenize text into words

    words = text.split(" ")
    for i in range(len(words)): words[i] = stemmer.stem(words[i])
    return words

seed_url = "https://en.wikipedia.org/wiki/Music"
r = requests.get(seed_url)
html = r.text
soup = BeautifulSoup(html, 'html.parser')

all_elements = [element for element in soup.find_all(['p', 'a', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6'])] # Finds all associated tags
p_elements = soup.find_all('p') # Finds all <p> tags in entire HTML document
# str_elements = [str(element) for element in p_elements] # Convert all elements to strings (includes hrefs)
# text_elements = [element.get_text() for element in p_elements] # Extract words, removes other tags (only text)

# Combine all text elements into one string or process individually
# all_text = "\n".join(elements)
# print(all_text)
out_links = []
seen_links = set()

for element in p_elements: # For each paragraph element:

    for link in element.find_all('a'): # For each <a> tag in the paragraph element:

        # Process the link and add to queue if it is a new link
        href = link.get('href')
        if href is None: continue
        if not re.match(r"^/wiki/", href): continue
        if href in seen_links: continue
        print(f"Found new link to add to queue: {href}")
        seen_links.add(href)
        out_links.append(href)

    text = element.get_text()
    text = process_text(text)
    print(f"Processed text: {text}")
