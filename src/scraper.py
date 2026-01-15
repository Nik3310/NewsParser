import requests
from bs4 import BeautifulSoup
import re
import json
from validator import NimedeValideerija


class UudisteSkanner:
    """
    Klass veebilehtede laadimiseks ja pealkirjade töötlemiseks.
    """

    def __init__(self, url, domeen):
        self.url = url
        self.domeen = domeen
        self.valideerija = NimedeValideerija()
        self.paised = {'User-Agent': 'Mozilla/5.0'}
        self.nime_muster = r'\b[A-ZŠŽÕÄÖÜ][a-zšžõäöü-]+(?:\s+[A-ZŠŽÕÄÖÜ][a-zšžõäöü.-]*){1,3}\b'

    def skaneeri(self):
        """
        Laeb lehe ja otsib nimed. Tagastab listi tulemustega.
        """
        try:
            vastus = requests.get(self.url, headers=self.paised, timeout=10)
            soup = BeautifulSoup(vastus.text, 'html.parser')
            tulemused = []

            for el in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'a']):
                tekst = " ".join(el.get_text().split())
                nimed = re.findall(self.nime_muster, tekst)

                for nimi in nimed:
                    if self.valideerija.on_inimese_nimi(nimi):
                        link = el['href'] if el.name == 'a' and el.has_attr('href') else self.url
                        if link.startswith('/'): link = f"{self.url.rstrip('/')}{link}"

                        tulemused.append({"name": nimi, "headline": tekst, "url": link})
            return tulemused
        except Exception as e:
            print(f"Viga {self.domeen} skaneerimisel: {e}")
            return []

    def salvesta(self, andmed):
        """Salvestab andmed JSON faili."""
        with open(f"{self.domeen}.json", 'w', encoding='utf-8') as f:
            json.dump(andmed, f, ensure_ascii=False, indent=4)