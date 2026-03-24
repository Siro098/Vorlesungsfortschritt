# @Author: Simon Liebl & Adrian Döring
# Git: Siro098 & adiiii789
# Python Skript for Vorlesungsfortschritt 1.0

from icalendar import Calendar
from datetime import datetime, timedelta
import os
import requests
import sys

# === KONFIGURATION ===
#URL = "https://dhbw.app/ical/STG-TINF24IN"  # Download-Link für die iCal-Datei
DEST_FOLDER = os.path.abspath(__file__).replace("Vorlesungsfortschritt.py","ical")  # Speicherort für die iCal-Datei
#ICS_FILE = os.path.join(DEST_FOLDER, str(URL.split("/")[-1]) + ".ics")  # Pfad zur gespeicherten iCal-Datei

# Neuer Speicherort für Rainmeter (kein OneDrive!)
OUTPUT_FILE = os.path.abspath(__file__).replace("Vorlesungsfortschritt.py",r"txtfiles\Vorlesung.txt")
OUTPUT_FILE1 = os.path.abspath(__file__).replace("Vorlesungsfortschritt.py",r"txtfiles\Zahl.txt")
OUTPUT_FILE2 = os.path.abspath(__file__).replace("Vorlesungsfortschritt.py",r"txtfiles\Bar.txt")

# Speicherort für Wallpaper Engine (relativer Pfad gönnt nicht)
#WALLPAPER = True
# OUTPUT_FILE3 = "C:/Program Files (x86)/Steam/steamapps/workshop/content/431960/1322008613/test/percentage.txt"


def update_ics_file():
    today = datetime.today().date()
    updated_lines = []
    found_datum = False

    with open(config, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    for line in lines:
        if line.strip().startswith("datum="):
            found_datum = True
            try:
                saved_date = datetime.strptime(line.strip().split("=", 1)[1], "%Y-%m-%d").date()
                if saved_date < today:
                    updated_lines.append(f"datum={today}\n")
                else:
                    print("ICS-Datei wurde heute bereits aktualisiert.")
                    return
            except Exception as e:
                updated_lines.append(f"datum={today}\n")
        else:
            updated_lines.append(line)

    if not found_datum:
        updated_lines.append(f"datum={today}\n")

    print("Lade ICS-Datei herunter...")
    try:
        response = requests.get(URL, stream=True)
        if response.ok:
            with open(ICS_FILE, 'wb') as f:
                for chunk in response.iter_content(chunk_size=1024 * 8):
                    if chunk:
                        f.write(chunk)
                        f.flush()
                        os.fsync(f.fileno())
        else:
            print(f"Fehler beim Download: {response.status_code}")
            sys.exit(1)
    except Exception as e:
        print(f"Fehler beim Download: {e}")
        # sys.exit(1)

    with open(config, 'w', encoding='utf-8') as f:
        f.writelines(updated_lines)


def write_to_file(vorlesung, percentage, timer_if_upcoming_subject, remaining_time="", earned=None):
    """Schreibt die Vorlesungsdaten in eine Datei, die Rainmeter nutzen kann."""
    progress_bar_length = 25
    filled_blocks = int(round(progress_bar_length * percentage / 100))
    progress_bar = "[" + "#" * filled_blocks + "-" * (progress_bar_length - filled_blocks) + "]"
    if timer_if_upcoming_subject != "":
        progress_bar = timer_if_upcoming_subject

    try:
        with open(OUTPUT_FILE, "w") as f:
            f.write(f"{vorlesung}\n")
        with open(OUTPUT_FILE1, "w") as f:
            if remaining_time != "":
                lohn_str = f" | {earned:.2f}" if earned is not None else ""
                f.write(f"{percentage:.3f}% - {remaining_time}{lohn_str}€\n")
            else:
                f.write(f"{percentage:.3f} %\n")
        with open(OUTPUT_FILE2, "w") as f:
            f.write(f"{progress_bar}\n")

        if WALLPAPER:
            with open(OUTPUT_FILE3, "w") as f:
                if vorlesung == "Keine Vorlesung aktiv":
                    f.write(r"")
                    return
                if timer_if_upcoming_subject != "":
                    f.write(f"{vorlesung}\n{timer_if_upcoming_subject}\n")
                    return
                f.write(f"{vorlesung}\n{progress_bar}\n{percentage:.3f}% | {remaining_time}{lohn_str}$\n")

    except Exception as e:
        print(f"Fehler beim Schreiben der Datei: {e}")


def get_monthly_vorlesungsstunden():
    """Berechnet die gesamten Vorlesungsstunden im aktuellen Monat aus der ICS-Datei."""
    now = datetime.now().astimezone()
    month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    # Nächsten Monat berechnen
    if now.month == 12:
        month_end = now.replace(year=now.year + 1, month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
    else:
        month_end = now.replace(month=now.month + 1, day=1, hour=0, minute=0, second=0, microsecond=0)

    total_seconds = 0
    try:
        with open(ICS_FILE, 'rb') as f:
            ecal = Calendar.from_ical(f.read())
        for component in ecal.walk():
            if component.name == "VEVENT":
                start = component.decoded("dtstart")
                end = component.decoded("dtend")
                if isinstance(start, datetime) and isinstance(end, datetime):
                    if month_start <= start < month_end:
                        total_seconds += (end - start).total_seconds()
    except Exception as e:
        print(f"Fehler beim Berechnen der Monatsstunden: {e}")

    return total_seconds / 3600  # Stunden


def main():
    print("Starte Berechnung...")  # Debug-Ausgabe

    """Berechnet den aktuellen Fortschritt der laufenden Vorlesung."""
    now = datetime.now().astimezone()  # Konvertiert 'now' in ein offset-aware datetime
    try:
        with open(ICS_FILE, 'rb') as f:
            ecal = Calendar.from_ical(f.read())

        for component in ecal.walk():
            if component.name == "VEVENT":
                start = component.decoded("dtstart")
                end = component.decoded("dtend")
                subject = component.decoded("SUMMARY").decode("utf-8") if isinstance(component.decoded("SUMMARY"),
                                                                                     bytes) else str(
                    component.decoded("SUMMARY"))
                if isinstance(start, datetime) and isinstance(end, datetime):
                    if start <= now <= end:
                        total_duration = (end - start).total_seconds()
                        elapsed_time = (now - start).total_seconds()
                        percentage = (elapsed_time / total_duration) * 100

                        remaining_seconds = (end - now).total_seconds()
                        hours = str(int(remaining_seconds // 3600)).zfill(2)
                        minutes = str(int((remaining_seconds % 3600) // 60)).zfill(2)
                        seconds = str(int(remaining_seconds % 60)).zfill(2)
                        remaining_time = f"{hours}:{minutes}:{seconds}"

                        # Lohn berechnen: Monatslohn / Vorlesungsstunden im Monat * bereits absolvierte Stunden
                        monatsstunden = get_monthly_vorlesungsstunden()
                        if monatsstunden > 0:
                            lohn_pro_sekunde = MONATSLOHN / (monatsstunden * 3600)
                            earned = elapsed_time * lohn_pro_sekunde
                        else:
                            earned = 0.0

                        write_to_file(subject, percentage, "", remaining_time, earned)
                        return  # Vorlesung gefunden, kein weiteres Durchsuchen nötig

                    elif now <= start and now.date() == start.date():  # Nächste Vorlesung an selben Tag
                        time_to_subject = (start - now).total_seconds()
                        hours = str(int(time_to_subject // 3600)).zfill(2)
                        minutes = str(int((time_to_subject % 3600) // 60)).zfill(2)
                        seconds = str(int(time_to_subject % 60)).zfill(2)

                        timer_if_upcoming_subject = f"{hours}:{minutes}:{seconds}"
                        write_to_file(subject, 0, timer_if_upcoming_subject)
                        return  # Erste Vorlesung, welche nach der aktuellen Zeit stattfindet

        # Falls keine Vorlesung läuft, leere Datei schreiben
        write_to_file("Keine Vorlesung aktiv", 0, "")

    except Exception as e:
        print(f"Fehler beim Verarbeiten der iCal-Datei: {e}")
        write_to_file("Fehler", 0, "")


zeile = ""
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
            if "kurs" in typ:
                return array[i].split("=")[-1].strip()
            elif "monatslohn" in typ:
                return float(array[i].split("=")[-1].strip())
            elif "wallpaper_aktiv" in typ:
                pass
            elif "pfad_falls_nicht_in_dokumente" in typ:
                pass
            elif "wallpaper_datei_pfad" in typ:
                pass

    return None


if __name__ == "__main__":
    config = os.path.abspath(__file__).replace("Vorlesungsfortschritt.py", "config.txt")
    if open(config, 'r', encoding='utf-8').read() != "":
        URL = "https://dhbw.app/ical/" + fetchSetupFile("kurs") + ".ics"
        ICS_FILE = os.path.join(DEST_FOLDER, str(URL.split("/")[-1]))  # Pfad zur gespeicherten iCal-Datei

        MONATSLOHN = fetchSetupFile("monatslohn") or 0.0

        if "Wallpaper An" in open(config, 'r', encoding='utf-8').read():
            WALLPAPER = True
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
                if "wallpaper_datei_pfad" in array[i]:
                    OUTPUT_FILE3 = array[i].split("=")[-1].strip()
        else:
            WALLPAPER = False

        update_ics_file()
        main()
    else:
        print("Setup nicht ausgeführt (-> config leer)")