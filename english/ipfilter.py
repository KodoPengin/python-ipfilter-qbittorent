import os
import requests
import gzip
import shutil
import datetime
import ipaddress
import re
from tqdm import tqdm

# List definitions, more can be added
LISTS = [
    ("Level 1", "http://list.iblocklist.com/?list=ydxerpxkpcfqjaybcssw&fileformat=p2p&archiveformat=gz"),
    ("Anti-Infringement", "http://list.iblocklist.com/?list=dufcxgnbjsdwmwctgfuj&fileformat=p2p&archiveformat=gz"),
    ("Spamhaus DROP", "http://list.iblocklist.com/?list=zbdlwrqkabxbcppvrnos&fileformat=p2p&archiveformat=gz"),
    ("CINS Army", "http://list.iblocklist.com/?list=npkuuhuxcsllnhoamkvm&fileformat=p2p&archiveformat=gz"),
    ("badpeers", "http://list.iblocklist.com/?list=cwworuawihqvocglcoss&fileformat=p2p&archiveformat=gz"),
    ("spyware", "http://list.iblocklist.com/?list=llvtlsjyoyiczbkjsxpf&fileformat=p2p&archiveformat=gz"),
    ("ads (optional)", "http://list.iblocklist.com/?list=dgxtneitpuvgqqcpfulq&fileformat=p2p&archiveformat=gz")
]

def is_valid_ip(ip_str):
    try:
        ipaddress.ip_address(ip_str)
        return True
    except ValueError:
        return False

def convert_to_ipfilter_format(source_path, destination_path, log_lines, append=False, list_name=""):
    mode = 'a' if append else 'w'
    converted = 0
    skipped = 0
    corrected = 0

    with open(source_path, 'r', encoding='utf-8') as src, \
         open(destination_path, mode, encoding='utf-8') as dst:

        for line_num, line in enumerate(src, start=1):
            original_line = line.strip()
            if not original_line or original_line.startswith('#'):
                continue

            match = re.search(r'(\d{1,3}(?:\.\d{1,3}){3})\s*-\s*(\d{1,3}(?:\.\d{1,3}){3})$', original_line)
            if not match:
                skipped += 1
                log_lines.append(f"[{list_name}] [ERROR] Line {line_num}: Invalid IP range → {original_line}")
                continue

            ip_start, ip_end = match.groups()
            if not (is_valid_ip(ip_start) and is_valid_ip(ip_end)):
                skipped += 1
                log_lines.append(f"[{list_name}] [ERROR] Line {line_num}: Invalid IP address → {original_line}")
                continue

            description = original_line[:match.start()].rstrip(' :').strip()
            converted_line = f"{ip_start} - {ip_end} , 000 , {description}"
            dst.write(converted_line + '\n')
            converted += 1

            if not original_line.endswith(f"{ip_start}-{ip_end}"):
                corrected += 1
                log_lines.append(
                    f"[{list_name}] [CORRECTED] Line {line_num}:\n  Original  : {original_line}\n  Converted : {converted_line}"
                )

    log_lines.append(f"[{list_name}] Summary: {converted} processed, {corrected} corrected, {skipped} skipped\n")

def download_and_process_lists(block_list_path):
    block_list_path_resolved = os.path.abspath(block_list_path)
    final_ipfilter_file = os.path.join(block_list_path_resolved, 'ipfilter.dat')
    temp_file = os.path.join(block_list_path_resolved, 'temp_download.gz')
    raw_file = os.path.join(block_list_path_resolved, 'ipfilter_raw.p2p')
    log_file_path = os.path.join(block_list_path_resolved, 'log.txt')
    log_lines = []

    # Header with timestamp
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_lines.append(f"===== IPFilter update started: {now} =====\n")

    if os.path.exists(final_ipfilter_file):
        answer = input(f"The file '{final_ipfilter_file}' already exists. Overwrite? (y/n): ").strip().lower()
        if answer != 'y':
            print("Aborted. The file was not overwritten.")
            return

    print("The following IP filter lists will be downloaded and merged:\n")
    for name, _ in LISTS:
        print(f"- {name}")
    print()

    first_list = True
    for name, url in LISTS:
        print(f"\n→ Downloading list: {name}")
        log_lines.append(f"[{name}] Download started")

        try:
            response = requests.get(url, headers={'User-Agent': 'curl/8.7.1'}, stream=True)
            total_size = int(response.headers.get('content-length', 0))
            block_size = 1024

            with open(temp_file, 'wb') as f, tqdm(total=total_size, unit='iB', unit_scale=True) as bar:
                for data in response.iter_content(block_size):
                    f.write(data)
                    bar.update(len(data))

            with gzip.open(temp_file, 'rb') as f_in:
                with open(raw_file, 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)

            log_lines.append(f"[{name}] Download successful")
            convert_to_ipfilter_format(
                raw_file,
                final_ipfilter_file,
                log_lines,
                append=not first_list,
                list_name=name
            )

            first_list = False
            os.remove(raw_file)

        except Exception as e:
            log_lines.append(f"[{name}] Download failed: {str(e)}")

    if os.path.exists(temp_file):
        os.remove(temp_file)

    log_lines.append(f"\n===== Processing completed =====\n")

    with open(log_file_path, 'w', encoding='utf-8') as log:
        log.write('\n'.join(log_lines))

    print("\n✅ All lists downloaded and merged.")
    print(f"→ Output file: {final_ipfilter_file}")
    print(f"→ Log file   : {log_file_path}")

    print("\nTo use the IP filter in qBittorrent:")
    print("* Go to: Tools → Options → Connection → IP Filtering")
    print(f"* Set the filter file to: '{final_ipfilter_file}'")

# Run script
block_list_path = os.getcwd()
download_and_process_lists(block_list_path)
