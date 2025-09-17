# Vorlesungsfortschritt.py
# @Author: Simon Liebl & Adrian Döring
# Git: Siro098 & adiiii789
# Python Skript for Vorlesungsfortschritt 1.3 (multi-ICS)

from icalendar import Calendar
from datetime import datetime
import os
import requests
import sys
import configparser

DEST_FOLDER = os.path.abspath(__file__).replace("Vorlesungsfortschritt.py", "ical")
OUTPUT_FILE  = os.path.abspath(__file__).replace("Vorlesungsfortschritt.py", r"txtfiles\Vorlesung.txt")
OUTPUT_FILE1 = os.path.abspath(__file__).replace("Vorlesungsfortschritt.py", r"txtfiles\Zahl.txt")
OUTPUT_FILE2 = os.path.abspath(__file__).replace("Vorlesungsfortschritt.py", r"txtfiles\Bar.txt")

def ensure_dirs():
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    os.makedirs(DEST_FOLDER, exist_ok=True)

def parse_ics_urls(value):
    if not value:
        return []
    return [u.strip() for u in value.replace("|", "\n").split("\n") if u.strip()]

def download_ics(url, target_path, timeout=5):
    try:
        resp = requests.get(url, stream=True, timeout=timeout)
        if not resp.ok:
            print(f"HTTP {resp.status_code} bei {url}")
            return False
        with open(target_path, "wb") as f:
            for chunk in resp.iter_content(8192):
                if chunk:
                    f.write(chunk)
        return True
    except Exception as e:
        print(f"Download-Fehler {url}: {e}")
        return False

def write_to_file(vorlesung, percentage, timer_if_upcoming_subject):
    progress_bar_length = 25
    filled_blocks = int(round(progress_bar_length * percentage / 100))
    progress_bar = "[" + "#" * filled_blocks + "-" * (progress_bar_length - filled_blocks) + "]"
    if timer_if_upcoming_subject != "":
        progress_bar = timer_if_upcoming_subject
    try:
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            f.write(f"{vorlesung}\n")
        with open(OUTPUT_FILE1, "w", encoding="utf-8") as f:
            f.write(f"{percentage:.3f} %\n")
        with open(OUTPUT_FILE2, "w", encoding="utf-8") as f:
            f.write(f"{progress_bar}\n")
    except Exception as e:
        print(f"Fehler beim Schreiben der Datei: {e}")

def collect_events_from_files(files):
    now = datetime.now().astimezone()
    current_hit = None
    next_today = None

    for fp in files:
        try:
            with open(fp, "rb") as f:
                cal = Calendar.from_ical(f.read())
            for comp in cal.walk():
                if comp.name != "VEVENT":
                    continue
                start = comp.decoded("dtstart")
                end   = comp.decoded("dtend")
                subj  = comp.decoded("SUMMARY")
                if isinstance(subj, bytes):
                    subj = subj.decode("utf-8", errors="replace")
                if not isinstance(start, datetime) or not isinstance(end, datetime):
                    continue
                if start <= now <= end:
                    if current_hit is None or end < current_hit["end"]:
                        current_hit = {"subject": subj, "start": start, "end": end}
                elif now <= start and now.date() == start.date():
                    if next_today is None or start < next_today["start"]:
                        next_today = {"subject": subj, "start": start, "end": end}
        except Exception as e:
            print(f"Fehler beim Verarbeiten von {fp}: {e}")

    return current_hit, next_today

def main_multi(urls):
    ensure_dirs()
    today = datetime.today().date()
    config_path = os.path.abspath(__file__).replace("Vorlesungsfortschritt.py", "config.txt")
    files = []
    for url in urls:
        name = url.split("/")[-1] or "kalender.ics"
        if not name.lower().endswith(".ics"):
            name += ".ics"
        path = os.path.join(DEST_FOLDER, name)
        files.append(path)
        ok = download_ics(url, path)
        if not ok:
            print(f"Warnung: {url} konnte nicht geladen werden.")

    current_hit, next_today = collect_events_from_files(files)
    if current_hit:
        total = (current_hit["end"] - current_hit["start"]).total_seconds()
        elapsed = (datetime.now().astimezone() - current_hit["start"]).total_seconds()
        pct = max(0.0, min(100.0, (elapsed / total) * 100.0))
        write_to_file(current_hit["subject"], pct, "")
        return
    if next_today:
        delta = (next_today["start"] - datetime.now().astimezone()).total_seconds()
        hours = str(int(delta // 3600)).zfill(2)
        minutes = str(int((delta % 3600) // 60)).zfill(2)
        seconds = str(int(delta % 60)).zfill(2)
        write_to_file(next_today["subject"], 0, f"{hours}:{minutes}:{seconds}")
        return
    write_to_file("Keine Vorlesung aktiv", 0, "")

if __name__ == "__main__":
    config_path = os.path.abspath(__file__).replace("Vorlesungsfortschritt.py", "config.txt")
    if os.path.exists(config_path):
        config = configparser.ConfigParser()
        config.read(config_path)
        urls_val = ""
        if "ICS" in config and "URLs" in config["ICS"]:
            urls_val = config["ICS"]["URLs"]
        urls = parse_ics_urls(urls_val)
        if urls:
            main_multi(urls)
        else:
            write_to_file("Keine Vorlesung aktiv", 0, "")
    else:
        print("Keine Konfiguration gefunden.")