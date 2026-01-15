# Uudisteportaalide pealkirjade nimede tuvastaja

## Kirjeldus
See projekt on Pythonis kirjutatud skript, mis laeb Eesti uudisteportaalide avalehed ning otsib sealt pealkirjadest inimeste nimesid.  
Programm toetab portaale **postimees.ee**, **delfi.ee** ja **ohtuleht.ee**.  
Leitud nimed kogutakse kokku ja salvestatakse iga portaali kohta eraldi JSON-faili.  
Rakendust saab kasutada käsurea (CLI) kaudu (või GUI kaudu, kui projektis on graafiline liides).

## Nõuded
- Python 3.10 või uuem
- Python paketid:
  - requests
  - beautifulsoup4

Kõik vajalikud paketid on loetletud failis `requirements.txt`.

## Paigaldus
1. Klooni repositoorium:
   ```bash
   git clone <repo-url>
   cd <repo-kaust>


## Loo virtuaalkeskkond
```bash
1. python -m venv venv
        (Windows)                  (Linux)
2. venv\Scripts\activate / source venv/bin/activate
```

## Paigalda sõltuvused:
```bash
pip install requests beautifulsoup4

```

## Käivitamine

```bash 
python main.py
```


Kasutaja saab valida uudisteportaali kas käsurea argumendina või programmi käivitamisel menüüst.

(Kui projektis on GUI, siis: programmi käivitamisel avaneb graafiline kasutajaliides, kus saab rippmenüüst valida portaali.)

Näide väljundist

Programmi töö tulemus salvestatakse JSON-faili.
Iga portaali kohta luuakse eraldi fail:

"postimees.json"

"delfi.json"

"ohtuleht.json"

Näide postimees.json failist:
