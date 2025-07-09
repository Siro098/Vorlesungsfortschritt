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
    outdated = False

    with open(config, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    for line in lines:
        if line.strip().startswith("datum="):
            found_datum = True
            try:
                saved_date = datetime.strptime(line.strip().split("=", 1)[1], "%Y-%m-%d").date()
                if saved_date < today:
                    updated_lines.append(f"datum={today}\n")
                    outdated = True
                else:
                    print("ICS-Datei wurde heute bereits aktualisiert.")
                    return
            except Exception as e:
                updated_lines.append(f"datum={today}\n")
                outdated = True
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
        sys.exit(1)

    with open(config, 'w', encoding='utf-8') as f:
        f.writelines(updated_lines)


def write_to_file(vorlesung, percentage, timer_if_upcoming_subject):
    """Schreibt die Vorlesungsdaten in eine Datei, die Rainmeter nutzen kann."""
    progress_bar_length = 25  # Länge des Fortschrittsbalkens
    filled_blocks = int(round(progress_bar_length * percentage / 100))
    progress_bar = "[" + "#" * filled_blocks + "-" * (progress_bar_length - filled_blocks) + "]"
    if timer_if_upcoming_subject != "":
        # Zeit bis nächste Vorlesung
        progress_bar = timer_if_upcoming_subject

    try:
        with open(OUTPUT_FILE, "w") as f:
            f.write(f"{vorlesung}\n")  # Vorlesungsname
        with open(OUTPUT_FILE1, "w") as f:
            f.write(f"{percentage:.3f} %\n")  # Prozentwert
        with open(OUTPUT_FILE2, "w") as f:
            f.write(f"{progress_bar}\n")  # Fortschrittsbalke

        if WALLPAPER:
            with open(OUTPUT_FILE3, "w") as f:
                if vorlesung == "Keine Vorlesung aktiv":
                    f.write(r"")
                    return
                if timer_if_upcoming_subject != "":
                    f.write(f"{vorlesung}\n{timer_if_upcoming_subject}\n")
                    return

                f.write(f"{vorlesung}\n{progress_bar}\n{percentage:.3f}%\n")

    except Exception as e:
        print(f"Fehler beim Schreiben der Datei: {e}")


def main():
    print("Starte Berechnung...")  # Debug-Ausgabe

    """Berechnet den aktuellen Fortschritt der laufenden Vorlesung."""
    now = datetime.now().astimezone()  # - timedelta(hours=12, minutes=15) # Konvertiert 'now' in ein offset-aware datetime
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
                        write_to_file(subject, percentage, "")
                        return  # Vorlesung gefunden, kein weiteres Durchsuchen nötig

                    elif now <= start and now.date() == start.date():  # Nächste Vorlesung an selben Tag
                        # print(now.date())
                        # print(start.date())
                        time_to_subject = (start - now).total_seconds()
                        hours = str(int(time_to_subject // 3600)).zfill(2)
                        minutes = str(int((time_to_subject % 3600) // 60)).zfill(2)
                        seconds = str(int(time_to_subject % 60)).zfill(2)

                        timer_if_upcoming_subject = f"{hours}:{minutes}:{seconds}"
                        # print(timer_if_upcoming_subject)
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
                    OUTPUT_FILE3 =  array[i].split("=")[-1].strip()
                    #print(OUTPUT_FILE3)
        else:
            WALLPAPER = False

        update_ics_file()
        main()
    else:
        print("Setup nicht ausgeführt (-> config leer)")

