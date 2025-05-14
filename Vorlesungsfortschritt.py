# @Author: Simon Liebl & Adrian Döring
#Git: Siro098 & adiiii789
#Python Skript for Vorlesungsfortschritt 1.0

from icalendar import Calendar 
from datetime import datetime, timedelta
import os
import requests
import sys

# === KONFIGURATION ===
URL = "https://dhbw.app/ical/STG-TINF24IN"  # Download-Link für die iCal-Datei
DEST_FOLDER = r".\ical" # Speicherort für die iCal-Datei
ICS_FILE = os.path.join(DEST_FOLDER, str(URL.split("/")[-1])+".ics")  # Pfad zur gespeicherten iCal-Datei

# Neuer Speicherort für Rainmeter (kein OneDrive!)
OUTPUT_FILE = r".\txtfiles\Vorlesung.txt"  
OUTPUT_FILE1 = r".\txtfiles\Zahl.txt"  
OUTPUT_FILE2 = r".\txtfiles\Bar.txt"  

# Speicherort für Wallpaper Engine (relativer Pfad gönnt nicht)
WALLPAPER = True
OUTPUT_FILE3 = "C:/Program Files (x86)/Steam/steamapps/workshop/content/431960/1322008613/test/percentage.txt"

def update_ics_file():
    """Lädt die aktuelle iCal-Datei herunter."""
    print("Lade ICS-Datei herunter...")  # Debug-Output
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
        print(f"Fehler beim Aktualisieren der iCal-Datei: {e}")
        sys.exit(1)

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
    now = datetime.now().astimezone()# - timedelta(hours=12, minutes=15) # Konvertiert 'now' in ein offset-aware datetime
    try:
        with open(ICS_FILE, 'rb') as f:
            ecal = Calendar.from_ical(f.read())

        for component in ecal.walk():
            if component.name == "VEVENT":
                start = component.decoded("dtstart")
                end = component.decoded("dtend")
                subject = component.decoded("SUMMARY").decode("utf-8") if isinstance(component.decoded("SUMMARY"), bytes) else str(component.decoded("SUMMARY"))
                if isinstance(start, datetime) and isinstance(end, datetime):
                    if start <= now <= end:
                        total_duration = (end - start).total_seconds()
                        elapsed_time = (now - start).total_seconds()
                        percentage = (elapsed_time / total_duration) * 100
                        write_to_file(subject, percentage, "")
                        return  # Vorlesung gefunden, kein weiteres Durchsuchen nötig

                    elif now <= start and now.date() == start.date(): # Nächste Vorlesung an selben Tag
                        #print(now.date())
                        #print(start.date())
                        time_to_subject = (start - now).total_seconds()
                        hours =   str(int(time_to_subject // 3600)).zfill(2)
                        minutes = str(int((time_to_subject % 3600) // 60)).zfill(2)
                        seconds = str(int(time_to_subject % 60)).zfill(2)

                        timer_if_upcoming_subject = f"{hours}:{minutes}:{seconds}"
                        #print(timer_if_upcoming_subject)
                        write_to_file(subject, 0, timer_if_upcoming_subject)
                        return # Erste Vorlesung, welche nach der aktuellen Zeit stattfindet


        # Falls keine Vorlesung läuft, leere Datei schreiben
        write_to_file("Keine Vorlesung aktiv", 0, "")

    except Exception as e:
        print(f"Fehler beim Verarbeiten der iCal-Datei: {e}")
        write_to_file("Fehler", 0, "")

if __name__ == "__main__":
    update_ics_file()
    main()
