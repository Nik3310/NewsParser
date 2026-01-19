import tkinter as tk
from scraper import UudisteSkanner


class UudisteApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Uudisteotsija")

        self.portaalid = [
            ("https://www.delfi.ee", "delfi"),
            ("https://www.postimees.ee", "postimees"),
            ("https://www.ohtuleht.ee", "ohtuleht")
        ]

        tk.Label(root, text="Programm skaneerib portaale automaatselt...").pack(pady=20)
        self.staatus = tk.Label(root, text="Ootel")
        self.staatus.pack()

        # Käivita automaatne skaneerimine 1 sekund peale akna avanemist
        self.root.after(1000, self.skaneeri_koik)

    def skaneeri_koik(self):
        for url, domeen in self.portaalid:
            self.staatus.config(text=f"Töötlen: {domeen}")
            self.root.update()

            skanner = UudisteSkanner(url, domeen)
            tulemused = skanner.skaneeri()
            skanner.salvesta(tulemused)

        self.staatus.config(text="Kõik failid salvestatud kausta 'json_tulemused'", fg="green")


if __name__ == "__main__":
    root = tk.Tk()
    app = UudisteApp(root)
    root.mainloop()