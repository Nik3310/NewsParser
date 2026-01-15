import requests
from bs4 import BeautifulSoup
import re
import json
import os


class NimedeValideerija:
    """
    Klass, mis tegeleb leitud tekstist valepositiivsete tulemuste eemaldamisega.
    Selle eesmärk on eristada pärisnimed üldnimedest ja pealkirjade algustest.
    """

    def __init__(self):
        # Sõnad, mis sageli algavad suure tähega, kuid ei ole inimese nimed
        self.must_nimekiri = [
            "Reklaam", "Postimees", "Delfi", "Õhtuleht", "Telli", "Loe", "Fotod", "Video",
            "Kuidas", "Miks", "Millal", "Kelle", "Milleks", "Kuna", "Kas", "Siis", "Vaata",
            "Eesti", "Tallinn", "Tartu", "Pärnu", "Euroopa", "Vene", "Ukraina", "Soome",
            "Plaan", "Uus", "Suur", "Foto", "Otse", "Blogi", "Lugeja", "Kiri", "Juhtkiri",
            "Arvamus", "Majandus", "Kultuur", "Sport", "Ilm", "Telekava", "Täna", "Homme"
        ]

    def on_inimese_nimi(self, nime_string):
        """
        Kontrollib, kas leitud sõnade jada on tõenäoliselt inimese nimi.

        :param nime_string: Leitud tekstiosa.
        :return: True, kui tekst vastab nimele, False kui see on praht.
        """
        sonad = nime_string.split()

        # 1. Kontrollime, ega nimes pole keelatud sõnu
        for sona in sonad:
            puhas_sona = sona.strip(".,!-–\"„“")
            if puhas_sona in self.must_nimekiri:
                return False

        # 2. Välistame "Plaan B" tüüpi kombinatsioonid (üksik täht lõpus ilma punktita)
        if len(sonad[-1]) == 1 and sonad[-1].isupper():
            if not nime_string.endswith('.'):
                return False

        # 3. Nimi ei tohi olla üleni suurte tähtedega (nt "FOTOD", "UUDISED")
        if nime_string.isupper() and len(nime_string) > 5:
            return False

        # 4. Spetsiifilised fraasid, mis tihti valesti tuvastatakse
        valed_fraasid = ["Kuidas Eesti", "Eesti Ekspress", "Telli Postimees"]
        if any(fraas in nime_string for fraas in valed_fraasid):
            return False

        return True


class UudisteSkanner:
    """
    Klass uudisteportaalide veebilehtede allalaadimiseks ja sealt nimede otsimiseks.
    """

    def __init__(self, url, domeen):
        """
        Skanneri algseadistamine.

        :param url: Portaali täielik aadress.
        :param domeen: Domeeni nimi faili salvestamiseks.
        """
        self.url = url
        self.domeen = domeen
        self.valideerija = NimedeValideerija()
        self.paised = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        # Regulaaravaldis: 2-4 sõna, algavad suurtähega (sh täpitähed), lubatud on sidekriips
        self.nime_muster = r'\b[A-ZŠŽÕÄÖÜ][a-zšžõäöü-]+(?:\s+[A-ZŠŽÕÄÖÜ][a-zšžõäöü.-]*){1,3}\b'

    def lae_html(self):
        """
        Laeb veebilehe HTML sisu alla.
        """
        try:
            vastus = requests.get(self.url, headers=self.paised, timeout=10)
            vastus.raise_for_status()
            return BeautifulSoup(vastus.text, 'html.parser')
        except Exception as e:
            print(f"Viga lehe {self.url} laadimisel: {e}")
            return None

    def otsi_nimed(self):
        """
        Leiab lehelt pealkirjad ja eraldab sealt valideeritud nimed.

        :return: List leitud andmetega (nimi, pealkiri, link).
        """
        soup = self.lae_html()
        if not soup:
            return []

        tulemused = []
        # Otsime pealkirjade märgenditest h1...h6 ja linkidest
        margendid = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'a'])

        for margend in margendid:
            tekst = margend.get_text().strip()
            # Puhastame teksti liigsetest tühikutest
            tekst = " ".join(tekst.split())

            leitud_nimed = re.findall(self.nime_muster, tekst)

            for nimi in leitud_nimed:
                if self.valideerija.on_inimese_nimi(nimi):
                    # Otsime linki artiklile
                    link = margend['href'] if margend.name == 'a' and margend.has_attr('href') else None
                    if not link:
                        vanem_link = margend.find_parent('a')
                        link = vanem_link['href'] if vanem_link and vanem_link.has_attr('href') else self.url

                    # Korrigeerime suhtelised lingid
                    if link.startswith('/'):
                        link = f"{self.url.rstrip('/')}{link}"
                    elif not link.startswith('http'):
                        link = self.url

                    tulemused.append({
                        "name": nimi,
                        "headline": tekst,
                        "url": link
                    })

        # Eemaldame duplikaadid (sama nimi samas pealkirjas)
        unikaalsed = []
        nahtud = set()
        for t in tulemused:
            identifikaator = (t['name'], t['headline'])
            if identifikaator not in nahtud:
                unikaalsed.append(t)
                nahtud.add(identifikaator)

        return unikaalsed

    def salvesta_json(self, andmed):
        """
        Salvestab leitud andmed JSON-faili.
        """
        failinimi = f"{self.domeen}.json"
        with open(failinimi, 'w', encoding='utf-8') as f:
            json.dump(andmed, f, ensure_ascii=False, indent=4)
        print(f"Fail {failinimi} on loodud. Leiti {len(andmed)} nime.")


class Rakendus:
    """
    Peamine klass rakenduse töö juhtimiseks (CLI kasutajaliides).
    """

    def __init__(self):
        self.portaalid = {
            "1": ("https://www.delfi.ee", "delfi"),
            "2": ("https://www.postimees.ee", "postimees"),
            "3": ("https://www.ohtuleht.ee", "ohtuleht")
        }

    def kaima(self):
        """Käivitab programmi menüü."""
        print("=== Eesti Uudiste Nimede Otsija ===")
        print("Vali portaal skaneerimiseks:")
        print("1. Delfi")
        print("2. Postimees")
        print("3. Õhtuleht")
        print("4. Kõik portaalid")
        print("0. Välju")

        valik = input("\nSisesta number: ")

        if valik == "4":
            for võti in self.portaalid:
                self.tootle_portaal(võti)
        elif valik in self.portaalid:  # <--- SIIN OLI VIGA (oli portals)
            self.tootle_portaal(valik)
        elif valik == "0":
            print("Programmi lõpp.")
        else:
            print("Vigane valik!")

    def tootle_portaal(self, voti):
        """
        Viib läbi ühe portaali skaneerimise ja salvestamise.
        """
        url, domeen = self.portaalid[voti]
        print(f"\nAlustan portaali {domeen} skaneerimist...")
        skanner = UudisteSkanner(url, domeen)
        andmed = skanner.otsi_nimed()
        skanner.salvesta_json(andmed)


if __name__ == "__main__":
    # Käivitame rakenduse
    app = Rakendus()
    app.kaima()