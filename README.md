The Tool is completly free to use if you want to buy us a coffee we´d really appreciate it because ☕ = Happiness :)
https://buymeacoffee.com/vorlesungsfortschritt

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
3. Als nächstes die `Setup.py` ausführen.
4. In dem Textfeld den aktuellen Kurs eintragen und `Speichern` (wenn man Wallpaper aktiviert, soll man eine `.txt` Datei auswählen, in welche Kursname, Prozent und Balken separat eingetragen und synchronisiert werden)
5. Falls Rainmeter im Hintergrund offen ist, `neustarten`.
6. Rainmeter öffnen, den Ordner `Vorlesungsfortschritt` aufklappen, die `Vorlesungsfortschritt.ini` doppelklicken, oder anwählen und `Laden` oben rechts anwählen.
7. Falls man es personalisieren möchte, kann man `Bearbeiten` anwählen und bei [DeinMeter1]/[DeinMeter2]/[DeinMeter3] Die `FontSize` und `FontColor` anpassen.

## Troubleshoot

Wenn das `Setup` das Rainmeter Verzeichnis nicht in `Dokumente` vorfindet, kommt in Setup ein Button, bei welchem man den `Rainmeter` Ordner auswählen soll. 

Wenn in der `config` bereits etwas steht, fragt das Setup ob man dies überschreiben will. Bei betätigen von Ja wird die `config` zurückgesetzt. 

Getestet unter Python 3.8, 3.12, 3.13 (VM Win11)

## Its not a Bug its a feature(Known Problems)
-Sollten zwei Termine zum selben Zeitpunkt stattfinden wechselt das Skript regelmäßig zwischen denn beiden Terminen(interresanterweiße ziemlich rhytmisch)
-Der Fortschrittsbalken kann Artefakte bilden bei manchen Schriftgrößen, ebenfalls wird er immer länger(in Untersuchung)
