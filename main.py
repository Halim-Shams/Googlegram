import requests as re
from bs4 import BeautifulSoup

# Searches the google if ther is a hilight for it
def searcher(q: str):    
    response = re.get(f'https://www.google.com/search?q={q}')
    soup = BeautifulSoup(response.text, 'html.parser')
    span = soup.find_all('span')[9]
    hilights = span.parent
    hilighted_spans = hilights.find_all('span')
    hilighted_response = ''
    for span in hilighted_spans:
        try:  
            hilighted_response += span.string
        except:
            return "Couldn't found a proper hilight :()"

    if len(hilighted_response) > 0:
        return hilighted_response
    else:
        return "Couldn't found a proper hilight :()"
    
searcher('')