# qBittorrent IPFilter Updater

Dieses Python-Skript lädt mehrere IP-Blocklisten von [I-Blocklist](https://www.iblocklist.com/) herunter, wandelt sie in das von **qBittorrent** unterstützte Format um und fasst sie in einer einzigen Datei `ipfilter.dat` zusammen.

## Funktionen

- Automatischer Download und Verarbeitung bekannter IP-Blocklisten  
- Zusammenführung aller Einträge in eine gültige `ipfilter.dat`  
- Erkennung und Korrektur typischer Formatfehler  
- Validierung aller IP-Adressen und Bereiche  
- Fortschrittsanzeige während des Downloads (`tqdm`)  
- Erstellung eines detaillierten Protokolls (`log.txt`) mit Statistik und Fehlern  

## Verwendete Blocklisten

Folgende Listen werden standardmäßig eingebunden:

- Level 1  
- Anti-Infringement  
- Spamhaus DROP  
- CINS Army  
- badpeers  
- spyware  
- ads (optional)

Alle Listen werden im `.gz`-Format heruntergeladen und einzeln verarbeitet.

## Anwendung

### Voraussetzungen

- Python 3.6 oder höher  
- Notwendige Pakete:
  ```bash
  pip install requests tqdm
