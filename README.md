#ENGLISH VERSION BELOW!

# The Tool is completly free to use if you want to buy us a coffee we´d really appreciate it because ☕ = Happiness :)
https://buymeacoffee.com/vorlesungsfortschritt
# TOP DONATERS
1.
2.
3.

# Description
`Created by Simon Liebl (Siro098) & Adrian Döring (adiiii789)`

Ein Skript zum Anzeigen des aktuellen Fortschrittes in einer DHBW Vorlesung in Prozent.

Hierfür wurde Python als Backend und Rainmeter als Frontend gewählt.

Die .ics Daten werden von DHBW.app bezogen, daher den Kursnamen von dort nehmen.

## Konfiguration
**Die `Vorlesungsfortschritt.py` soll nicht ausgeführt werden, das macht Rainmeter automatisch!**

Um das Programm richtig einzurichten, wird zunächst `Python 3.XX` und `Rainmeter` vorrausgesetzt. 

(Python kann aus dem MS Store runtergeladen werden, Rainmeter von der eigenen Seite)

1. Den neusten Release von `Vorlesungsfortschritt` herunterladen und entpacken.
2. Die Fonts in `FondsInstalls` ausführen und installieren.
3. Im Ordner \RainmeterInstaller den .rmskin Installer nutzen um denn Skin zu installieren.
4. Als nächstes die `Setup.py` ausführen.
5. In dem Textfeld den aktuellen Kurs eintragen und `Speichern` (wenn man Wallpaper aktiviert, soll man eine `.txt` Datei auswählen, in welche Kursname, Prozent und Balken separat eingetragen und synchronisiert werden)
6. Falls Rainmeter im Hintergrund offen ist, `neustarten`.
7. Rainmeter öffnen, den Ordner `Vorlesungsfortschritt` aufklappen, die `Vorlesungsfortschritt.ini` doppelklicken, oder anwählen und `Laden` oben rechts anwählen.
8. Falls man es personalisieren möchte, kann man `Bearbeiten` anwählen und bei [DeinMeter1]/[DeinMeter2]/[DeinMeter3] Die `FontSize` und `FontColor` anpassen.

## Troubleshoot

Wenn das `Setup` das Rainmeter Verzeichnis nicht in `Dokumente` vorfindet, kommt in Setup ein Button, bei welchem man den `Rainmeter` Ordner auswählen soll. 

Wenn in der `config` bereits etwas steht, fragt das Setup ob man dies überschreiben will. Bei betätigen von Ja wird die `config` zurückgesetzt. 

Getestet unter Python 3.8, 3.12, 3.13 (VM Win11)

## Its not a Bug its a feature(Known Problems)
-Sollten zwei Termine zum selben Zeitpunkt stattfinden wechselt das Skript regelmäßig zwischen denn beiden Terminen(interresanterweiße ziemlich rhytmisch)
-Der Fortschrittsbalken kann Artefakte bilden bei manchen Schriftgrößen, ebenfalls wird er immer länger(in Untersuchung)


Description

Created by Simon Liebl (Siro098) & Adrian Döring (adiiii789)

A script to display the current progress of a DHBW lecture in percent.

For this, Python is used as the backend and Rainmeter as the frontend.

The .ics data is retrieved from DHBW.app, so make sure to use the course name provided there.

#Configuration
Do not run Vorlesungsfortschritt.py manually – Rainmeter will execute it automatically!
To set up the program properly, you need Python 3.XX and Rainmeter. (Python can be downloaded from the Microsoft Store, Rainmeter from the official website.)

1. Download and extract the latest release of Vorlesungsfortschritt.
2. Install the fonts by running the installers in the FontsInstalls folder.
3. Use the .rmskin installer located in the \RainmeterInstaller folder to install the skin.
4. Next, run Setup.py.
5. Enter your current course name into the text field and click Save. (If you enable the wallpaper feature, select a .txt file where course name, percentage, and progress bar will be written and synchronized separately.)
6. If Rainmeter is already running in the background, restart it.
7. Open Rainmeter, expand the Vorlesungsfortschritt folder, double-click Vorlesungsfortschritt.ini, or select it and press Load in the top right.
8. To personalize it, choose Edit and adjust FontSize and FontColor under [DeinMeter1]/[DeinMeter2]/[DeinMeter3].

# Troubleshooting

If the Setup cannot find the Rainmeter directory in Documents, a button will appear allowing you to select the Rainmeter folder manually.
If the config file already contains entries, the setup will ask whether you want to overwrite it. Clicking Yes will reset the configuration.
Tested with Python 3.8, 3.12, 3.13 (Windows 11 VM).

It’s not a bug, it’s a feature (Known Issues)
If two events occur at the same time, the script will switch between them regularly (interestingly, in a rather rhythmic way).
The progress bar may show artifacts at certain font sizes, and it tends to get longer over time (currently under investigation).
