import requests
from bs4 import BeautifulSoup
import re
import json
import os
from validator import NimedeValideerija


class UudisteSkanner:
    def __init__(self, url, domeen):
        self.url = url
        self.domeen = domeen
        self.valideerija = NimedeValideerija()
        self.paised = {'User-Agent': 'Mozilla/5.0'}
        self.nime_muster = r'\b[A-ZŠŽÕÄÖÜ][a-zšžõäöü-]+(?:\s+[A-ZŠŽÕÄÖÜ][a-zšžõäöü.-]*){1,3}\b'

    def skaneeri(self):
        try:
            vastus = requests.get(self.url, headers=self.paised, timeout=10)
            soup = BeautifulSoup(vastus.text, 'html.parser')
            koik_tulemused = []

            # Otsime pealkirju
            for el in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'a']):
                pealkiri = " ".join(el.get_text().split())
                leitud_nimed = re.findall(self.nime_muster, pealkiri)

                # Kui pealkirjas on MITU nime, teeme igaühe kohta eraldi kirje
                for nimi in leitud_nimed:
                    if self.valideerija.on_inimese_nimi(nimi):
                        link = el['href'] if el.name == 'a' and el.has_attr('href') else self.url
                        if link.startswith('/'):
                            link = f"{self.url.rstrip('/')}{link}"

                        koik_tulemused.append({
                            "name": nimi,
                            "headline": pealkiri,
                            "url": link
                        })
            return koik_tulemused
        except Exception as e:
            print(f"Viga: {e}")
            return []

    def salvesta(self, andmed):
        # Loo kaust 'json_tulemused', kui seda veel pole
        kaust = "json_tulemused"
        if not os.path.exists(kaust):
            os.makedirs(kaust)

        faili_tee = os.path.join(kaust, f"{self.domeen}.json")
        with open(faili_tee, 'w', encoding='utf-8') as f:
            json.dump(andmed, f, ensure_ascii=False, indent=4)