# ENGLISH VERSION BELOW!

# The Tool is completly free to use if you want to buy us a coffee we´d really appreciate it because ☕ = Happiness :)
https://buymeacoffee.com/vorlesungsfortschritt
# TOP DONATERS
1.
2.
3.

# Description
`Created by Simon Liebl (Siro098) & Adrian Döring (adiiii789)`

Ein Skript zum Anzeigen des aktuellen Fortschrittes in einer DHBW Vorlesung oder eines Kalendertermins in Prozent.

Hierfür wurde Python als Backend und Rainmeter als Frontend gewählt.

Die .ics Daten werden von DHBW.app bezogen, daher den Kursnamen von dort nehmen.

## Konfiguration
**Die `Vorlesungsfortschritt.py` soll nicht ausgeführt werden, das macht Rainmeter automatisch!**

Um das Programm richtig einzurichten, wird zunächst `Python 3.XX` und `Rainmeter` vorrausgesetzt. 

(Python kann aus dem MS Store runtergeladen werden, Rainmeter von der eigenen Seite)

1. Neusten Release von Vorlesungsfortschritt installieren und entpacken.
2. In denn Ordner FondsInstallswechseln und beide Schriftarten installieren
3. In denn Ordner RainmeterInstaller wechseln und denn Vorlesungsfortschritt_v1.3.rmskin installer nutzen.
4. Als nächstes in denn Skins Ordner von Rainmeter wechseln und die setup.py ausführen (Python sollte vorher installiert werden)
5. Sollte der Skin sich nicht automatisch geöffnet haben in Rainmeter, denn Vorlesungsfortschrittordner ausklappen und die Vorlesungsfortschritt.ini doppelklicken / laden
6. In der .ini Datei können Die Schriftgröße und Farbe ect. verändert werden (DeinMeter1-3)
7. Viel Spaß

## Troubleshoot

Wenn das `Setup` das Rainmeter Verzeichnis nicht in `Dokumente` vorfindet, kommt in Setup ein Button, bei welchem man den `Rainmeter` Ordner auswählen soll. 

Wenn in der `config` bereits etwas steht, fragt das Setup ob man dies überschreiben will. Bei betätigen von Ja wird die `config` zurückgesetzt. 

Getestet unter Python 3.8, 3.12, 3.13 (VM Win11)

## Its not a Bug its a feature(Known Problems)
-Sollten zwei Termine zum selben Zeitpunkt stattfinden wechselt das Skript regelmäßig zwischen denn beiden Terminen(interresanterweiße ziemlich rhytmisch)
-Der Fortschrittsbalken kann Artefakte bilden bei manchen Schriftgrößen, ebenfalls wird er immer länger(in Untersuchung)


Description

Created by Simon Liebl (Siro098) & Adrian Döring (adiiii789)

A script to display the current progress of a DHBW lecture or calender event in percent.

For this, Python is used as the backend and Rainmeter as the frontend.

The .ics data is retrieved from DHBW.app, so make sure to use the course name provided there.

#Configuration
Do not run Vorlesungsfortschritt.py manually – Rainmeter will execute it automatically!
To set up the program properly, you need Python 3.XX and Rainmeter. (Python can be downloaded from the Microsoft Store, Rainmeter from the official website.)

1. Download the latest release of Vorlesungsfortschritt and extract it.
2. Go to the FontsInstalls folder and install both fonts.
3. Navigate to the RainmeterInstaller folder and run the Vorlesungsfortschritt_v1.3.rmskin installer.
4. Next, open the Skins folder of Rainmeter and execute the setup.py file (make sure Python is installed beforehand).
5. If the skin does not automatically appear in Rainmeter, expand the Vorlesungsfortschritt folder and double-click/load the Vorlesungsfortschritt.ini file.
6. Inside the .ini file you can adjust font size, colors, etc. (DeinMeter1-3).
7. Have fun!

# Troubleshooting

If the Setup cannot find the Rainmeter directory in Documents, a button will appear allowing you to select the Rainmeter folder manually.

If the config file already contains entries, the setup will ask whether you want to overwrite it. Clicking Yes will reset the configuration.

Tested with Python 3.8, 3.12, 3.13 (Windows 11 VM).

## It’s not a bug, it’s a feature (Known Issues)
If two events occur at the same time, the script will switch between them regularly (interestingly, in a rather rhythmic way).
The progress bar may show artifacts at certain font sizes, and it tends to get longer over time (currently under investigation).
