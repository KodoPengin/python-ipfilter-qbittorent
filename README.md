# qBittorrent IPFilter Updater

This Python script automatically downloads, merges, and converts multiple IP filter blocklists from [I-Blocklist](https://www.iblocklist.com/) into a single `ipfilter.dat` file for use with **qBittorrent** or compatible clients.

## Features

- Downloads and processes multiple known blocklists (Level 1, Anti-Infringement, Spamhaus, etc.)
- Merges all entries into a single, valid `ipfilter.dat` file
- Automatically corrects common formatting issues
- Validates and logs malformed or corrected entries
- Displays download progress using `tqdm`
- Creates a detailed `log.txt` file with per-list statistics

## Blocklists Included

The following lists are included by default:

- Level 1  
- Anti-Infringement  
- Spamhaus DROP  
- CINS Army  
- badpeers  
- spyware  
- ads (optional)

Each list is fetched as a compressed `.gz` file and processed accordingly.

## Usage

### Prerequisites

- Python 3.6+
- Dependencies:
  ```bash
  pip install requests tqdm
