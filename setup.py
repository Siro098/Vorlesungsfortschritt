import tkinter as tk
import configparser
import os
import sys
import subprocess

dateiname = os.path.abspath(__file__).replace("setup.py", "config.txt")


def installiere_module():
    try:
        python_path = sys.executable
        for modul in ["requests", "icalendar"]:
            print(f"Installiere {modul}...")
            subprocess.run([python_path, "-m", "pip", "install", modul], check=True)
        print("Alle Module wurden erfolgreich installiert.")
    except Exception as e:
        print(f"Ein Fehler ist aufgetreten: {e}")


def speichern(root, eintrag_kurs, kurs_checkbox_var, txt_urls):
    config = configparser.ConfigParser()
    # Collect URLs from text field
    urls_roh = txt_urls.get("1.0", tk.END).strip()
    urls = [u.strip() for u in urls_roh.splitlines() if u.strip()]

    # Check if checkbox is checked and Kursname is provided
    kursname = eintrag_kurs.get().strip()
    if kurs_checkbox_var.get() and kursname:
        dhbw_url = f"https://dhbw.app/ical/{kursname}.ics"
        urls.append(dhbw_url)

    config["ICS"] = {"URLs": "|".join(urls)}
    # Save Kursname for reference (optional)
    config["ICS"]["Kursname"] = kursname if kursname else ""
    config["ICS"]["KursCheckbox"] = str(bool(kurs_checkbox_var.get()))
    with open(dateiname, "w", encoding="utf-8") as configfile:
        config.write(configfile)
    root.destroy()


def erstellen_fenster():
    root = tk.Tk()
    root.title("iCal-Links/Kursname speichern")
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    fenster_width = int(screen_width * 0.36)
    fenster_height = int(screen_height * 0.35)
    root.geometry(f"{fenster_width}x{fenster_height}")

    tk.Label(root, text="Kursname (optional, z.B. STG-TINF24IN):").pack(pady=(10, 0))
    eintrag_kurs = tk.Entry(root)
    eintrag_kurs.pack(pady=2, fill=tk.X, padx=8)

    kurs_checkbox_var = tk.IntVar()
    kurs_checkbox = tk.Checkbutton(root, text="DHBW.app Link für Kursname hinzufügen", variable=kurs_checkbox_var)
    kurs_checkbox.pack(pady=(2, 8))

    tk.Label(root, text="iCal-Links (ein Link pro Zeile):").pack(pady=(8, 0))
    txt_urls = tk.Text(root, height=8, wrap="word")
    txt_urls.pack(padx=8, pady=4, fill=tk.BOTH, expand=True)

    btn_speichern = tk.Button(
        root,
        text="Speichern",
        command=lambda: speichern(root, eintrag_kurs, kurs_checkbox_var, txt_urls)
    )
    btn_speichern.pack(side=tk.BOTTOM, fill=tk.X, pady=10)

    root.mainloop()


installiere_module()
erstellen_fenster()