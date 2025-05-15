import tkinter as tk
import configparser
import os
from tkinter import filedialog
import shutil
import sys
import subprocess

assert 1 + 1 == 2  # Damit Github nicht heult

dateiname = os.path.abspath(__file__).replace("setup.py", "config.txt")
print(dateiname)


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
    dateipfad = os.path.abspath(__file__).replace("setup.py", "Vorlesungsfortschritt.ini")
    try:
        python_path = os.path.abspath(sys.executable)
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
            #root.quit()

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


def toggle_button(button, btn_datei_waehlen, label_datei_pfad):
    button["text"] = "Wallpaper An" if button["text"] == "Wallpaper Aus" else "Wallpaper Aus"
    if button["text"] == "Wallpaper An":
        btn_datei_waehlen.pack(pady=5)
        label_datei_pfad.pack()
    else:
        btn_datei_waehlen.pack_forget()
        label_datei_pfad.pack_forget()


def datei_waehlen(label_datei_pfad, datei_var):
    pfad = filedialog.askopenfilename(title="Wähle eine Textdatei", filetypes=[("Textdateien", "*.txt")])
    if pfad:
        label_datei_pfad.config(text=f"Ausgewählt: {pfad}")
        datei_var.set(pfad)


def ordner_waehlen(label_ausgewaehlter_ordner, ordner_var):
    pfad = filedialog.askdirectory(title="Wähle einen Ordner")
    if pfad:
        label_ausgewaehlter_ordner.config(text=f"Ausgewählt: {pfad}")
        ordner_var.set(pfad)


def erstellen_fenster():
    root = tk.Tk()
    root.title("Konfiguration speichern")

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    fenster_width = int(screen_width * 0.32)
    fenster_height = int(screen_height * 0.4)
    root.geometry(f"{fenster_width}x{fenster_height}")

    ordner_pfad = tk.StringVar()
    datei_pfad = tk.StringVar()

    dokumente_path = os.path.join(os.path.expanduser("~"), "Documents")
    rainmeter_ordner = os.path.join(dokumente_path, "Rainmeter")

    if not os.path.exists(rainmeter_ordner):
        label_info = tk.Label(root, text="Rainmeter-Ordner nicht gefunden. Bitte einen Ordner auswählen:")
        label_info.pack()

        label_ausgewaehlter_ordner = tk.Label(root, text="Kein Ordner ausgewählt")
        label_ausgewaehlter_ordner.pack()

        btn_ordner_waehlen = tk.Button(root, text="Ordner auswählen",
                                       command=lambda: ordner_waehlen(label_ausgewaehlter_ordner, ordner_pfad))
        btn_ordner_waehlen.pack(pady=5)

    label = tk.Label(root, text="Kurs:\neg. STG-TINFXXIN")
    label.pack()
    eintrag = tk.Entry(root)
    eintrag.pack(pady=5)

    label_datei_pfad = tk.Label(root, text="Keine Datei ausgewählt")
    btn_datei_waehlen = tk.Button(root, text="Textdatei auswählen",
                                  command=lambda: datei_waehlen(label_datei_pfad, datei_pfad))

    button = tk.Button(root, text="Wallpaper Aus",
                       command=lambda: toggle_button(button, btn_datei_waehlen, label_datei_pfad))
    button.pack(pady=5)

    btn_speichern = tk.Button(root, text="Speichern", command=lambda: speichern(
        root, eintrag, button, ordner_pfad.get(), datei_pfad.get()))
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

        shutil.copytree(quellordner, zielordner, ignore=shutil.ignore_patterns(".github", ".git"))
        print(f"Ordner '{quellordner}' wurde erfolgreich nach '{zielordner}' kopiert.")
    except Exception as e:
        print(f"Ein Fehler ist aufgetreten: {e}")


def copyFolder(ordner_pfad):
    array = []
    with open(dateiname, 'r', encoding='utf-8') as datei:
        for zeile in datei:
            array.append(zeile.strip())

    for zeile in array:
        if "pfad_falls_nicht_in_dokumente" in zeile:
            ziel = zeile.split("=")[-1].strip() + r"\Skins\Vorlesungsfortschritt"
            quelle = os.path.join(os.path.abspath(__file__).replace("setup.py", ""))
            kopiere_ordner(quelle, ziel)
            return

    # Fallback wenn kein alternativer Pfad angegeben
    ziel = os.path.join(os.path.expanduser("~"), "Documents", "Rainmeter", "Skins", "Vorlesungsfortschritt")
    quelle = os.path.join(os.path.abspath(__file__).replace("setup.py", ""))
    kopiere_ordner(quelle, ziel)


# Startpunkt
installiere_module()
print(os.path.exists(dateiname))
if os.path.exists(dateiname):
    check_ueberschreiben()
else:
    erstellen_fenster()
