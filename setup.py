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
        python_path = os.path.abspath(os.sys.executable)

        with open(dateipfad, "r", encoding="utf-8") as datei:
            inhalt = datei.read()

        inhalt = inhalt.replace("%SETUP%", python_path)

        with open(dateipfad, "w", encoding="utf-8") as datei:
            datei.write(inhalt)

        print(f"'%SETUP%' wurde in '{dateipfad}' erfolgreich durch '{python_path}' ersetzt.")

    except Exception as e:
        print(f"Ein Fehler ist aufgetreten: {e}")

def speichern(root, eintrag, button, ordner_pfad, datei_pfad):
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
    copyFolder(ordner_pfad)
    root.destroy()

def toggle_button(button, btn_datei_waehlen, label_datei_pfad):
    button["text"] = "Wallpaper An" if button["text"] == "Wallpaper Aus" else "Wallpaper Aus"

    if button["text"] == "Wallpaper An":
        btn_datei_waehlen.pack(pady=5)
        label_datei_pfad.pack()
    else:
        btn_datei_waehlen.pack_forget()
        label_datei_pfad.pack_forget()

def datei_waehlen(label_datei_pfad):
    datei_pfad = filedialog.askopenfilename(title="Wähle eine Textdatei", filetypes=[("Textdateien", "*.txt")])
    if datei_pfad:
        label_datei_pfad.config(text=f"Ausgewählt: {datei_pfad}")
    return datei_pfad

def ordner_waehlen(label_ausgewaehlter_ordner):
    ordner_pfad = filedialog.askdirectory(title="Wähle einen Ordner")
    if ordner_pfad:
        label_ausgewaehlter_ordner.config(text=f"Ausgewählt: {ordner_pfad}")
    return ordner_pfad

def erstellen_fenster():
    root = tk.Tk()
    root.title("Konfiguration speichern")

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    fenster_width = int(screen_width * 0.32)
    fenster_height = int(screen_height * 0.4)
    root.geometry(f"{fenster_width}x{fenster_height}")

    ordner_pfad = ""
    datei_pfad = ""

    dokumente_path = os.path.join(os.path.expanduser("~"), "Documents")
    rainmeter_ordner = os.path.join(dokumente_path, "Rainmeter")

    if not os.path.exists(rainmeter_ordner):
        label_info = tk.Label(root, text="Rainmeter-Ordner nicht gefunden. Bitte einen Ordner auswählen:")
        label_info.pack()

        btn_ordner_waehlen = tk.Button(root, text="Ordner auswählen", command=lambda: ordner_waehlen(label_ausgewaehlter_ordner))
        btn_ordner_waehlen.pack(pady=5)

        label_ausgewaehlter_ordner = tk.Label(root, text="Kein Ordner ausgewählt")
        label_ausgewaehlter_ordner.pack()

    label = tk.Label(root, text="Kurs:\neg. STG-TINFXXIN")
    label.pack()
    eintrag = tk.Entry(root)
    eintrag.pack(pady=5)

    button = tk.Button(root, text="Wallpaper Aus", command=lambda: toggle_button(button, btn_datei_waehlen, label_datei_pfad))
    button.pack(pady=5)

    btn_datei_waehlen = tk.Button(root, text="Textdatei auswählen", command=lambda: datei_waehlen(label_datei_pfad))
    label_datei_pfad = tk.Label(root, text="Keine Datei ausgewählt")

    btn_speichern = tk.Button(root, text="Speichern", command=lambda: speichern(root, eintrag, button, ordner_pfad, datei_pfad))
    btn_speichern.pack(side=tk.BOTTOM, fill=tk.X, pady=10)

    root.mainloop()

def kopiere_ordner(quellordner, zielordner):
    try:
        if not os.path.exists(quellordner):
            print(f"Der Quellordner '{quellordner}' existiert nicht.")
            return

        if os.path.exists(zielordner):
            shutil.rmtree(zielordner)
            print(f"Zielordner '{zielordner}' wurde gelöscht.")

        shutil.copytree(quellordner, zielordner, ignore=shutil.ignore_patterns(".github",".git"))
        print(f"Ordner '{quellordner}' wurde erfolgreich nach '{zielordner}' kopiert.")

    except Exception as e:
        print(f"Ein Fehler ist aufgetreten: {e}")

def copyFolder(ordner_pfad):
    array = []
    with open(dateiname, 'r', encoding='utf-8') as datei:
        for zeile in datei:
            array.append(zeile.strip())

    for i in range(len(array)):
        if "pfad_falls_nicht_in_dokumente" in array[i]:
            kopiere_ordner(os.path.join(os.getcwd()), array[i].split("=")[-1].strip() + "\\Skins\\Vorlesungsfortschritt")
            return
    kopiere_ordner(os.path.join(os.getcwd()), os.path.join(os.path.expanduser("~"), "Documents", "Rainmeter", "Skins", "Vorlesungsfortschritt"))

installiere_module()
if os.path.exists(dateiname):
    erstellen_fenster()
else:
    erstellen_fenster()