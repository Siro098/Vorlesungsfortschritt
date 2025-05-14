import tkinter as tk
import configparser
import os
from tkinter import filedialog
import shutil
import sys
import subprocess

dateiname = "config.txt"
def installiere_module():
    try:
        python_path = sys.executable

        for modul in ["requests", "icalendar"]:
            print(f"Installiere {modul}...")
            subprocess.run([python_path, "-m", "pip", "install", modul], check=True)

        print("Alle Module wurden erfolgreich installiert.")

    except Exception as e:
        print(f"Ein Fehler ist aufgetreten: {e}")


def editIni():
    dateipfad = r".\Vorlesungsfortschritt.ini"
    try:
        python_path = os.path.abspath(os.sys.executable)  # Ermittelt den aktuellen Python-Pfad

        with open(dateipfad, "r", encoding="utf-8") as datei:
            inhalt = datei.read()

        # Ersetzt "%SETUP%" durch den Python-Pfad
        inhalt = inhalt.replace("%SETUP%", python_path)

        with open(dateipfad, "w", encoding="utf-8") as datei:
            datei.write(inhalt)

        print(f"'%SETUP%' wurde in '{dateipfad}' erfolgreich durch '{python_path}' ersetzt.")

    except Exception as e:
        print(f"Ein Fehler ist aufgetreten: {e}")





def speichern(event=None):
    global root
    config = configparser.ConfigParser()

    if os.path.exists(dateiname):
        config.read(dateiname)

    if "Eingaben" not in config:
        config["Eingaben"] = {}

    config["Eingaben"]["Kurs"] = eintrag.get()
    config["Eingaben"]["Wallpaper_Aktiv"] = button["text"]

    if ordner_pfad:
        config["Eingaben"]["pfad_falls_nicht_in_Dokumente"] = ordner_pfad

    if datei_pfad:
        config["Eingaben"]["Wallpaper_Datei_Pfad"] = datei_pfad

    with open(dateiname, "w") as configfile:
        config.write(configfile)

    editIni()
    copyFolder()  # Funktion zum Kopieren des Ordners nach dem Speichern aufrufen
    root.destroy()

def check_ueberschreiben():
    config = configparser.ConfigParser()
    config.read(dateiname)

    if config.sections():
        def ueberschreiben():
            with open(dateiname, "w") as configfile:
                pass
            dialog.destroy()
            erstellen_fenster()

        def abbrechen():
            dialog.destroy()
            root.quit()

        dialog = tk.Tk()
        dialog.title("Konfiguration überschreiben?")
        label = tk.Label(dialog, text="Die Datei enthält bereits Daten. Überschreiben?")
        label.pack(pady=10)

        btn_yes = tk.Button(dialog, text="Ja", command=ueberschreiben)
        btn_yes.pack(side=tk.LEFT, padx=10, pady=10)

        btn_no = tk.Button(dialog, text="Nein", command=abbrechen)
        btn_no.pack(side=tk.RIGHT, padx=10, pady=10)

        dialog.mainloop()
    else:
        erstellen_fenster()


def toggle_button():
    button["text"] = "Wallpaper An" if button["text"] == "Wallpaper Aus" else "Wallpaper Aus"

    if button["text"] == "Wallpaper An":
        btn_datei_waehlen.pack(pady=5)
        label_datei_pfad.pack()
    else:
        btn_datei_waehlen.pack_forget()
        label_datei_pfad.pack_forget()


def datei_waehlen():
    global datei_pfad, label_datei_pfad
    datei_pfad = filedialog.askopenfilename(title="Wähle eine Textdatei", filetypes=[("Textdateien", "*.txt")])
    if datei_pfad:
        label_datei_pfad.config(text=f"Ausgewählt: {datei_pfad}")


def ordner_waehlen():
    global ordner_pfad, label_ausgewaehlter_ordner
    ordner_pfad = filedialog.askdirectory(title="Wähle einen Ordner")
    if ordner_pfad:
        label_ausgewaehlter_ordner.config(text=f"Ausgewählt: {ordner_pfad}")


def erstellen_fenster():
    global root, label_ausgewaehlter_ordner, btn_datei_waehlen, label_datei_pfad, eintrag
    root = tk.Tk()
    root.title("Konfiguration speichern")

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    fenster_width = int(screen_width * 0.32)
    fenster_height = int(screen_height * 0.4)
    root.geometry(f"{fenster_width}x{fenster_height}")

    global button, ordner_pfad, datei_pfad
    ordner_pfad = ""
    datei_pfad = ""

    dokumente_path = os.path.join(os.path.expanduser("~"), "Documents")
    rainmeter_ordner = os.path.join(dokumente_path, "Rainmeter")

    if not os.path.exists(rainmeter_ordner):
        label_info = tk.Label(root, text="Rainmeter-Ordner nicht gefunden. Bitte einen Ordner auswählen:")
        label_info.pack()

        btn_ordner_waehlen = tk.Button(root, text="Ordner auswählen", command=ordner_waehlen)
        btn_ordner_waehlen.pack(pady=5)

        label_ausgewaehlter_ordner = tk.Label(root, text="Kein Ordner ausgewählt")
        label_ausgewaehlter_ordner.pack()

    # Nur ein Textfeld bleibt erhalten
    label = tk.Label(root, text="Kurs:\neg. STG-TINFXXIN")
    label.pack()
    eintrag = tk.Entry(root)
    eintrag.pack(pady=5)
    eintrag.bind("<Return>", speichern)

    label_button = tk.Label(root, text="\n\n\nWenn aktiviert, schreibt generierte Daten in .txt Datei,\n welche weitere Programme nutzen können (e.g. Wallpaper Engine)")
    label_button.pack()
    button = tk.Button(root, text="Wallpaper Aus", command=toggle_button)
    button.pack(pady=5)

    # Button für Datei-Auswahl (wird erst sichtbar, wenn Wallpaper aktiviert wird)
    btn_datei_waehlen = tk.Button(root, text="Textdatei auswählen", command=datei_waehlen)
    label_datei_pfad = tk.Label(root, text="Keine Datei ausgewählt")

    # Speichern-Button **ganz unten** im Fenster platzieren
    btn_speichern = tk.Button(root, text="Speichern", command=speichern)
    btn_speichern.pack(side=tk.BOTTOM, fill=tk.X, pady=10)


    root.mainloop()

def kopiere_ordner(quellordner, zielordner):
    try:
        if not os.path.exists(quellordner):
            print(f"Der Quellordner '{quellordner}' existiert nicht.")
            return

        # Falls der Zielordner existiert, wird er gelöscht
        if os.path.exists(zielordner):
            shutil.rmtree(zielordner)
            print(f"Zielordner '{zielordner}' wurde gelöscht.")

        # Kopiere den Quellordner, ignoriere ".GitHub"
        shutil.copytree(quellordner, zielordner, ignore=shutil.ignore_patterns(".github",".git"))
        print(f"Ordner '{quellordner}' wurde erfolgreich nach '{zielordner}' kopiert ('.GitHub' ignoriert).")

    except Exception as e:
        print(f"Ein Fehler ist aufgetreten: {e}")


def copyFolder():
    array = []
    with open(r".\config.txt", 'r', encoding='utf-8') as datei:
        for zeile in datei:
            array.append(zeile.strip())

    for i in range(len(array)):
        if "pfad_falls_nicht_in_dokumente" in array[i]:
            #print(array[i].split("=")[-1].strip() + "/Skins")
            #print(os.path.join(os.path.expanduser("~"), "Documents", "Rainmeter", "Skins"))
            kopiere_ordner(os.path.join(os.getcwd()), array[i].split("=")[-1].strip() + "\\Skins\\Vorlesungsfortschritt")
            return
    kopiere_ordner(os.path.join(os.getcwd()), os.path.join(os.path.expanduser("~"), "Documents", "Rainmeter", "Skins", "Vorlesungsfortschritt"))

installiere_module()
if os.path.exists(dateiname):
    check_ueberschreiben()
else:
    erstellen_fenster()




