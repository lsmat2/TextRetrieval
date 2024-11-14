import requests
from bs4 import BeautifulSoup
# BEAUTIFUL SOUP DOCUMENTATION: https://www.crummy.com/software/BeautifulSoup/bs4/doc/
# soup = BeautifulSoup(html, 'html.parser')
# all_elements = [element for element in soup.find_all(['p', 'a', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6'])] # Finds all associated tags
# p_elements = soup.find_all('p') # Finds all <p> tags in entire HTML document
# str_elements = [str(element) for element in p_elements] # Convert all elements to strings (includes hrefs)
# text_elements = [element.get_text() for element in p_elements] # Extract words, removes other tags (only text)
import re
print("5_crawler.py")


def get_text(soup:BeautifulSoup) -> str:
    ### Get the text of the page

    p_elements = soup.find_all('p') # Finds all <p> tags in entire HTML
    text_elements_list = [element.get_text() for element in p_elements] # Extract words, removes other tags (only text)
    text = " ".join(text_elements_list)
    text = process_text(text)
    return text

def process_text(text:str) -> str:
    ### Remove punctuation, digits, and special characters, convert to lowercase

    text = text.lower()
    punctuation = [",", ".", "!", "?", "(", ")", "[", "]", "{", "}", ":", ";", "'", '"', "`", "“", "”"]
    digits = [str(i) for i in range(10)]
    special_chars = ["\n", "\t", "\r", "\x0b", "\x0c"]
    removable_chars = punctuation + digits + special_chars
    for char in removable_chars: text = text.replace(char, "")
    return text

def get_title(soup:BeautifulSoup) -> str:
    ### Get the title of the page

    title_element = soup.find('span', class_='mw-page-title-main')
    if title_element: return title_element.get_text()
    return None

def process_links(soup:BeautifulSoup) -> None:
    p_elements = soup.find_all('p') # Finds all <p> tags in entire HTML
    ### Process links in paragraph elements
    for element in p_elements: # For each paragraph element:

        for link in element.find_all('a'): # For each <a> tag in the paragraph element:

            # Process the link and add to queue if it is a new link
            href = link.get('href')
            if href is None: continue
            if not re.match(r"^/wiki/", href): continue
            if href in seen_links: continue
            seen_links.add(href)
            to_process_links.append("https://en.wikipedia.org"+href)

def process_doc(url:str) -> None:
    ### Process a new doc

    r = requests.get(url)
    html = r.text
    soup = BeautifulSoup(html, 'html.parser')
    title = get_title(soup)
    if title is not None: print(f"Title: {title}")
    text = get_text(soup)
    print(f"Text: {text[:500]}")
    process_links(soup)
    csv_line = f'"1","{title}","{text}"\n'
    csv_file.write(csv_line)

seed_url = "https://en.wikipedia.org/wiki/Hockey"
to_process_links = [seed_url]
seen_links = set()
NUM_DOCS = 100
processed_docs = 0

csv_file = open("crawler.csv", "w")
while processed_docs < NUM_DOCS:
    print(f"\n\nProcessing doc {processed_docs+1}")
    process_doc(to_process_links.pop(0))
    processed_docs += 1
csv_file.close()