class NimedeValideerija:
    """
    Klass nime tuvastamiseks ilma staatilise musta nimekirjata.
    Kasutab struktuurset loogikat.
    """

    def on_inimese_nimi(self, nime_string):
        """
        Kontrollib, kas tekst vastab nime struktuurile.
        """
        sonad = nime_string.split()

        # Nimi peab olema 2-4 sõna pikk
        if not (2 <= len(sonad) <= 4):
            return False

        for sona in sonad:
            # Puhastame sõna kirjavahemärkidest
            puhas = sona.strip(".,!-–\"„“")

            # Sõna peab algama suurtähega ja ülejäänud peavad olema väikesed
            # (See välistab "REKLAAM" või "UUDISED" tüüpi pealkirjad)
            if not (puhas[0].isupper() and puhas[1:].islower()):
                # Lubame sidekriipsuga nimesid nagu Mari-Liis
                if "-" in puhas:
                    osad = puhas.split("-")
                    if not all(o[0].isupper() for o in osad if o):
                        return False
                else:
                    return False

            # Välistame liiga lühikesed osad (nt "A B"), mis pole initsiaalid
            if len(puhas) < 2 and not puhas.endswith('.'):
                return False

        return True