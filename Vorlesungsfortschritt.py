# Vorlesungsfortschritt.py
# @Author: Simon Liebl & Adrian Döring
# Git: Siro098 & adiiii789
# Python Skript for Vorlesungsfortschritt 1.3 (multi-ICS)

from icalendar import Calendar
from datetime import datetime, timedelta
import os
import requests
import sys

DEST_FOLDER = os.path.abspath(__file__).replace("Vorlesungsfortschritt.py", "ical")
OUTPUT_FILE  = os.path.abspath(__file__).replace("Vorlesungsfortschritt.py", r"txtfiles\Vorlesung.txt")
OUTPUT_FILE1 = os.path.abspath(__file__).replace("Vorlesungsfortschritt.py", r"txtfiles\Zahl.txt")
OUTPUT_FILE2 = os.path.abspath(__file__).replace("Vorlesungsfortschritt.py", r"txtfiles\Bar.txt")

def ensure_dirs():
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    os.makedirs(DEST_FOLDER, exist_ok=True)

def normalize_summary(val):
    if isinstance(val, bytes):
        try:
            return val.decode("utf-8", errors="replace")
        except Exception:
            return str(val)
    return str(val)

def read_config_lines(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return [ln.strip() for ln in f]
    except FileNotFoundError:
        return []
    except Exception:
        return []

def get_value(lines, key):
    for ln in lines:
        if ln.lower().startswith(key.lower()+"="):
            return ln.split("=", 1)[1].strip()
    return ""

def parse_ics_urls(value):
    # akzeptiert Zeilenliste mit | Trennern oder neue Zeilen
    if not value:
        return []
    parts = []
    for chunk in value.replace("\r", "\n").replace("|", "\n").split("\n"):
        u = chunk.strip()
        if u:
            parts.append(u)
    return parts

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
        if WALLPAPER:
            with open(OUTPUT_FILE3, "w", encoding="utf-8") as f:
                if vorlesung == "Keine Vorlesung aktiv":
                    f.write("")
                    return
                if timer_if_upcoming_subject != "":
                    f.write(f"{vorlesung}\n{timer_if_upcoming_subject}\n")
                    return
                f.write(f"{vorlesung}\n{progress_bar}\n{percentage:.3f}%\n")
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
                subj  = normalize_summary(comp.decoded("SUMMARY"))
                if not isinstance(start, datetime) or not isinstance(end, datetime):
                    continue
                # laufend
                if start <= now <= end:
                    # nimm das mit der baldesten Endzeit
                    if current_hit is None or end < current_hit["end"]:
                        current_hit = {"subject": subj, "start": start, "end": end}
                # heute noch kommend
                elif now <= start and now.date() == start.date():
                    if next_today is None or start < next_today["start"]:
                        next_today = {"subject": subj, "start": start, "end": end}
        except Exception as e:
            print(f"Fehler beim Verarbeiten von {fp}: {e}")

    return current_hit, next_today

def main_multi(urls):
    ensure_dirs()
    # täglicher Downloadschutz über ein einziges Datumseintrag
    today = datetime.today().date()
    lines = read_config_lines(config)
    saved = get_value(lines, "datum")
    needs_download = True
    try:
        if saved:
            saved_date = datetime.strptime(saved, "%Y-%m-%d").date()
            needs_download = saved_date < today
    except Exception:
        needs_download = True

    files = []
    for url in urls:
        name = url.split("/")[-1] or "kalender.ics"
        if not name.lower().endswith(".ics"):
            name += ".ics"
        path = os.path.join(DEST_FOLDER, name)
        files.append(path)
        if needs_download:
            ok = download_ics(url, path)
            if not ok:
                print(f"Warnung: {url} konnte nicht geladen werden.")

    if needs_download:
        # datum aktualisieren
        rest = [ln for ln in lines if not ln.startswith("datum=")]
        rest.append(f"datum={today}")
        try:
            with open(config, "w", encoding="utf-8") as f:
                f.write("\n".join(rest) + "\n")
        except Exception as e:
            print(f"Konnte Datum nicht schreiben: {e}")

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

def fetchSetupFile(typ):
    array = []
    try:
        with open(config, 'r', encoding='utf-8') as datei:
            for zeile in datei:
                array.append(zeile.strip())
    except FileNotFoundError:
        print("Config nicht gefunden")
    except Exception as e:
        print(f"Ein Fehler ist aufgetreten: {e}")

    for i in range(len(array)):
        if typ in array[i]:
            return array[i].split("=", 1)[-1].strip()
    return None

if __name__ == "__main__":
    config = os.path.abspath(__file__).replace("Vorlesungsfortschritt.py", "config.txt")
    content = open(config, 'r', encoding='utf-8').read() if os.path.exists(config) else ""
    if content != "":
        WALLPAPER = "Wallpaper An" in content
        if WALLPAPER:
            array = read_config_lines(config)
            wp_path = get_value(array, "wallpaper_datei_pfad")
            if wp_path:
                OUTPUT_FILE3 = wp_path

        # neue Mehrfach-URLs
        urls_val = fetchSetupFile("ICS_URLS")
        urls = parse_ics_urls(urls_val) if urls_val else []

        if urls:
            main_multi(urls)
        else:
            # Fallback auf alten Kurs
            kurs = fetchSetupFile("Kurs")
            if not kurs:
                write_to_file("Keine Vorlesung aktiv", 0, "")
                sys.exit(0)
            url = "https://dhbw.app/ical/" + kurs + ".ics"
            ensure_dirs()
            ics_file = os.path.join(DEST_FOLDER, url.split("/")[-1])
            # einmal täglich laden
            main_multi([url])  # nutzt denselben Weg, aber nur mit einem Link
    else:
        print("Setup nicht ausgeführt (-> config leer)")
