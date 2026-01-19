import tkinter as tk
from news_scraper import NewsScraper
import os


class NewsApp:
    """
    Rakenduse graafiline liides.
    """

    def __init__(self, root):
        """
        Seadistab akna ja otsib targets.txt faili juurkaustast.
        """
        self.root = root
        self.root.title("Uudisteotsija")
        self.root.geometry("400x200")

        # Liigume src kaustast ühe taseme üles, et leida targets.txt
        self.TARGETS_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "targets.txt"))

        tk.Label(root, text="Süsteem skaneerib veebilehti...").pack(pady=20)
        self.status_label = tk.Label(root, text="Ootel", fg="blue")
        self.status_label.pack()

        self.root.after(1000, self.run_process)

    def get_urls(self):
        """
        Loeb URL-id failist, toetades erinevaid kodeeringuid.
        """
        if not os.path.exists(self.TARGETS_FILE):
            return []

        try:
            with open(self.TARGETS_FILE, 'r', encoding='utf-8') as f:
                return [line.strip() for line in f if line.strip() and not line.startswith('#')]
        except UnicodeDecodeError:
            with open(self.TARGETS_FILE, 'r', encoding='cp1252') as f:
                return [line.strip() for line in f if line.strip() and not line.startswith('#')]

    def run_process(self):
        """
        Käivitab skaneerimise protsessi kõikidele lehtedele.
        """
        urls = self.get_urls()
        if not urls:
            self.status_label.config(text="Viga: targets.txt ei leitud või on tühi!", fg="red")
            return

        for url in urls:
            self.status_label.config(text=f"Töötlen: {url}")
            self.root.update()

            scraper = NewsScraper(url)
            data = scraper.scrape_data()
            scraper.save_results(data)

        self.status_label.config(text="Valmis! Tulemused on kaustas json_results", fg="green")


if __name__ == "__main__":
    root = tk.Tk()
    app = NewsApp(root)
    root.mainloop()