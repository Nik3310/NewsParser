class NimedeValideerija:
    """
    Klass, mis kontrollib, kas leitud tekst on inimese nimi või mitte.
    """

    def __init__(self):
        self.must_nimekiri = [
            "Reklaam", "Postimees", "Delfi", "Õhtuleht", "Telli", "Loe", "Fotod", "Video",
            "Kuidas", "Miks", "Millal", "Kelle", "Milleks", "Kuna", "Kas", "Siis", "Vaata",
            "Eesti", "Tallinn", "Tartu", "Pärnu", "Euroopa", "Vene", "Ukraina", "Soome"
        ]

    def on_inimese_nimi(self, nime_string):
        """
        Kontrollib nime vastavust reeglitele.
        """
        sonad = nime_string.split()
        for sona in sonad:
            if sona.strip(".,!-–\"„“") in self.must_nimekiri:
                return False

        # Välistame üksiku tähe nime lõpus (nt "Plaan B")
        if len(sonad[-1]) == 1 and sonad[-1].isupper() and not nime_string.endswith('.'):
            return False

        return True