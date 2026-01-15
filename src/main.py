from scraper import UudisteSkanner

class Rakendus:
    """
    Peamine klass rakenduse töö juhtimiseks.
    """
    def __init__(self):
        self.portaalid = {
            "1": ("https://www.delfi.ee", "delfi"),
            "2": ("https://www.postimees.ee", "postimees"),
            "3": ("https://www.ohtuleht.ee", "ohtuleht")
        }

    def kaima(self):
        """Käivitab menüü."""
        print("-----------------------------------------")
        print("         --- Nimede Otsija ---           ")
        print("-----------------------------------------")
        print("1. Delfi")
        print("2. Postimees")
        print("3. Õhtuleht")
        print("4. Kõik")
        print("0. Välju")
        print("-----------------------------------------")
        valik = input("Vali: ")

        if valik == "4":
            for v in self.portaalid: self.tootle(v)
        elif valik in self.portaalid:
            self.tootle(valik)

    def tootle(self, voti):
        url, domeen = self.portaalid[voti]
        skanner = UudisteSkanner(url, domeen)
        andmed = skanner.skaneeri()
        skanner.salvesta(andmed)
        print(f"{domeen.capitalize()} skaneeritud. Leiti {len(andmed)} nime.")

if __name__ == "__main__":
    Rakendus().kaima()