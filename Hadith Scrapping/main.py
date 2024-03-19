import requests
from bs4 import BeautifulSoup
import random

# Return a random number between 0-97 (book)
def random_book_number():
    with open('books_lables.txt', 'r') as file:
        lines = file.readlines()
        random_index = random.randint(0, len(lines) - 1)
        return lines[random_index].strip()

# Crap and return a random hadith
def random_hadith(book: int):
    response = requests.get(f'https://sunnah.com/bukhari/{book}')
    soup = BeautifulSoup(response.text, 'html.parser')
    all_hadith_containers = soup.find_all('div', class_ = 'actualHadithContainer')
    random_index = random.randint(0, len(all_hadith_containers) - 1)
    random_hadith_container = all_hadith_containers[random_index]
    hadith_text_containers = random_hadith_container.find('div', class_ = 'hadithTextContainers')
    hadith_english_container = hadith_text_containers.find('div', class_ = 'englishcontainer')
    english_full_hadith = hadith_english_container.find('div', class_ = 'english_hadith_full')
    hadith_narrator = english_full_hadith.find('div', class_ = 'hadith_narrated').text.strip()
    hadith_details = english_full_hadith.find('div', class_ = 'text_details').p.text.strip()
    return [hadith_narrator, hadith_details]