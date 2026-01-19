import requests
from bs4 import BeautifulSoup
import re
import json
import os
from urllib.parse import urlparse
from name_validator import NameValidator


class NewsScraper:
    """
    Klass veebilehtedelt andmete kogumiseks ja salvestamiseks.
    """

    def __init__(self, url):
        """
        Initsialiseerib skanneri seaded.
        """
        self.url = url
        self.validator = NameValidator()
        self.headers = {'User-Agent': 'Mozilla/5.0'}
        self.NAME_PATTERN = r'\b[A-ZŠŽÕÄÖÜ][a-zšžõäöü-]+(?:\s+[A-ZŠŽÕÄÖÜ][a-zšžõäöü.-]*){1,3}\b'

        # Määrame asukoha: üks tase üles ja siis kausta json_results
        self.OUTPUT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "json_results"))

    def get_filename_from_url(self):
        """
        Genereerib domeeni põhjal failinime.
        """
        parsed = urlparse(self.url)
        domain = parsed.netloc.lower().replace('www.', '').split('.')[0]
        return f"{domain}.json"

    def scrape_data(self):
        """
        Kraabib veebilehelt pealkirjad ja nimed, eemaldades duplikaadid.
        """
        try:
            response = requests.get(self.url, headers=self.headers, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')
            results = []
            seen = set()

            for tag in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'a']):
                text = " ".join(tag.get_text().split())
                if not text:
                    continue

                found = re.findall(self.NAME_PATTERN, text)
                valid = [n for n in found if self.validator.is_human_name(n)]

                if valid:
                    link = tag['href'] if tag.name == 'a' and tag.has_attr('href') else self.url
                    if link.startswith('/'):
                        base = f"{urlparse(self.url).scheme}://{urlparse(self.url).netloc}"
                        link = f"{base}{link}"

                    names_str = ", ".join(valid)
                    entry_id = (names_str, text, link)

                    if entry_id not in seen:
                        results.append({
                            "names": names_str,
                            "headline": text,
                            "url": link
                        })
                        seen.add(entry_id)

            return results
        except Exception as e:
            print(f"Viga ({self.url}): {e}")
            return []

    def save_results(self, data):
        """
        Salvestab tulemused JSON faili juurkausta json_results alamkausta.
        """
        if not os.path.exists(self.OUTPUT_PATH):
            os.makedirs(self.OUTPUT_PATH)

        filename = self.get_filename_from_url()
        full_path = os.path.join(self.OUTPUT_PATH, filename)

        with open(full_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)