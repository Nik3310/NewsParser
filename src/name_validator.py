class NameValidator:
    """
    Klass nime struktuuri kontrollimiseks.
    Kasutab reegleid, et eristada pärisnimesid muust tekstist.
    """

    def is_human_name(self, name_string):
        """
        Kontrollib, kas tekst vastab nime struktuurile.

        Args:
            name_string (str): Kontrollitav tekstiosa.

        Returns:
            bool: True, kui tekst meenutab nime, muidu False.
        """
        words = name_string.split()

        if not (2 <= len(words) <= 4):
            return False

        for word in words:
            clean_word = word.strip(".,!-–\"„“")
            if not clean_word:
                continue

            if not (clean_word[0].isupper() and (len(clean_word) == 1 or clean_word[1:].islower())):
                if "-" in clean_word:
                    parts = clean_word.split("-")
                    if not all(p and p[0].isupper() for p in parts):
                        return False
                else:
                    return False

            if len(clean_word) < 2 and not clean_word.endswith('.'):
                return False

        return True