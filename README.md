### emustarter.py 3.0

Damit Emulatoren von Retro-Computern laufen, müssen eine Menge Optionen gesetzt sein. Wenn man spielen will, will man sich aber nicht mit diesen Optionen herumschlagen, sondern man will einfach sagen: "Computer, ich möchte auf diesem System dieses Spiel spielen!", und dann soll das Spiel einfach starten, egal auf welchem Emulator.
Um das auf der Linux-Konsole zu ermöglichen, hab' ich `emustarter.py` geschrieben, und zwar für diejenigen Systeme, bzw. Emulatoren, die ich benutze. Unterstützt werden also: 

- Sinclair ZX Spectrum  (fuse)
- Atari 800 XL          (atari800)
- Amiga (500 and 1200)  (fs-uae)
- Mame                  (mame)

#### Konfiguration

Natürlich müssen diese Emulatoren auf dem Linux-System installiert und schon eingerichtet sein, damit das funktioniert.
Und dann muß man leider auch noch etwas für `emustarter.py` konfigurieren.
Dazu muß man die Konfigurationsdatei `emustarter.dat` editieren, die sich in demselben Verzeichnis wie `emustarter.py` befinden sollte.
In `emustarter.dat` sind einige Verzeichnisse anzugeben, wo die Emulatoren die Spieldateien finden. Und dann ist dort eine Liste mit den Spielen und Spieldateien zu schreiben, die man mit `emustarter.py` benutzen möchte.
An den Zeilen mit den Überschriften in eckigen Klammern (wie "[Directories]") sollte man nichts ändern.
In der Datei `emustarter.dat` sind auch Beispiele angegeben, wie das Format der Dateinzeilen aussehen soll. Diese Zeilen müssen dann also an die Gegebenheiten auf dem jeweiligen Linux-System angepaßt werden.
Die Einträge in den Zeilen für die Spiele sind einfach jeweils durch ein Komma getrennt.
Wenn `emustarter.dat` im richtigen Format ist, kann es von `emustarter.py` gelesen werden, so daß dann alle benötigten Informationen vorhanden sind, und Spiele wie beschrieben gestartet werden können.

Die folgenden Hintergrundinformationen sollte man noch kennen, um die Einträge in `emustarter.dat` richtig bearbeiten zu können: 

- ZX Spectrum-Emulation mit `fuse`: Der Emulator liest zusätzlich seine eigene Konfigurationsdatei `~/.fuserc`.

- Atari 800 XL-Emulation mit `atari800`: Der Emulator liest zusätzlich seine eigene Konfigurationsdatei `~/.atari800.cfg`. Diese Datei kann mit der grafischen Benutzeroberfläche von `atari800` erstellt werden. Der Einfachheit halber hab' ich hier auch nochmal meine eigene Datei `atari800.cfg` hochgeladen, um zu zeigen, wie die ungefähr aussehen sollte.  
- Die meisten Atari 8-bit-Spiele verwenden das ROM des [Atari 800 XL](https://upload.wikimedia.org/wikipedia/commons/b/bf/Atari-800XL.jpg) (`atarixl.rom`). Einige ältere Spiele benötigen aber das ROM des älteren [Atari 800](https://upload.wikimedia.org/wikipedia/commons/3/35/Atari_800.jpg) (`atariosb.rom`). Damit `emustarter.py` damit umgehen kann, wird in den Datenzeilen zu den Spielen ein dritter Eintrag benötigt: `0` steht für das (normale) XL-ROM, `1` für das Atari 800-ROM. `emustarter.py` bricht (zur Zeit) wahrscheinlich mit einem Fehler ab, wenn dieser dritte Eintrag fehlt.

- Amiga-Emulation mit FS-UAE: Nach dem Namen des Spiels muß in `emustarter.dat` nicht der Name der ".adf"-Datei angegeben werden, sondern der Name der FS-UAE-Konfigurationsdatei für dieses Spiel.
Diese Konfigurationsdateien werden mit dem Programm `fs-uae-launcher` erstellt, das Teil von FS-UAE ist.
`fs-uae-launcher` schreibt diese Konfigurationsdateien in ein Verzeichnis `../FS-UAE/Configurations`. Sie haben die Dateiendung `.fs-uae`. Standardmäßig sollte `fs-uae-launcher` diese Dateien nach `/home/user/Dokumente/FS-UAE/Configurations` schreiben. Der Name dieses Verzeichnisses `Configurations` ist derjenige, der im oberen Teil von `emustarter.dat` unter `AMIGA_CONFIGURATIONS_PATH=...` angegeben werden muß. (Der Ort dieses `FS-UAE`-Verzeichnisses kann übrigens dadurch geändert werden, daß man einen anderen Ort in die Datei `/home/user/.config/fs-uae/base-dir` schreibt, aber das nur am Rande.)
- Verwendung von Snapshot-Dateien: Während ein Amiga-Programm in `fs-uae` läuft, kann man den Zustand des Speichers des Amigas in eine sog. Snapshot-Datei ("Save State") speichern, indem man dazu in `fs-uae` das Menü verwendet, das erscheint, wenn man `F12` drückt. Bei Amiga-Programmen versucht `emustarter.py` standardmäßig den Speicher-Snapshot im ersten Slot mitzuladen. (Vielen Dank an Frode Solheim, daß er das in `fs-uae` möglich gemacht hat!). Dadurch können Amiga-Programme unmittelbar ohne irgendwelche Disktettenladezeiten geladen werden (vorausgesetzt, der Speicherzustand des Amiga war in dem Moment als Snapshot gespeichert worden, als der Amiga gerade das Programm zuende geladen hatte). Das direkte Starten von Amiga-Programmen ohne Diskettenladezeiten ist eine tolle Sache, die nichtmal auf einem echten Amiga möglich ist.
Wenn man aber nicht möchte, daß `emustarter.py` versucht, den ersten Snapshot zu laden, kann man eine "0" als dritten Eintrag in den Zeilen für die Spiele in `emustarter.dat` angeben. Möchte man, daß stattdessen z.B. der zweite Snapshot geladen wird, kann man dort eine "2" angeben.

- Mame-Emulation: Falls man nicht weiß, was man bei `MAME_SAMPLES_PATH` angeben soll, kann man in dem Verzeichnis mit den Spieldateien ein leeres Verzeichnis `samples` erstellen, und dieses dann in `emustarter.dat` angeben.
  
- Noch zum Auffinden der Emulator-ROM-Dateien: Dazu müssen in `emustarter.dat` keine besonderen Angaben gemacht werden. Denn:
  - fuse: Amstrad als Copyright-Inhaber der ZX Spectrum-ROMs war so freundlich, diese für Emulationszwecke freizugeben. Daher sind sie bei fuse gleich mit dabei (bei mir im Verzeichnis `/usr/share/fuse`). Daher werden sie von fuse automatisch gefunden.
  - atari800: Der Name des Verzeichnisses mit den Atari ROM-Dateien (wie z.B. `atarixl.rom`) ist schon in der Konfigurationsdatei `~/.atari800.cfg` anzugeben und wird von dort vom Emulator `atari800` eingelesen.
  - FS-UAE: Der Name des Verzeichnisses mit den Amiga Kickstart ROM-Dateien wird in `fs-uae-launcher` mit Hilfe der grafischen Benutzeroberfläche angegeben, und von diesem Programm in die oben genannten Konfigurationsdateien geschrieben. Beim Starten der Amiga-Emulation wird eine dieser Dateien dann von `fs-uae` gelesen.
  - Mame: Die Spiele selbst werden auch ROMs genannt.

#### Kommandozeilenoptionen

- Startet man `emustarter.py` ohne Optionen, zeigt es einem jeweils eine Liste an, aus der man das gewünschte System und das gewünschte Spiel auswählen kann. Kennt man aber schon die Zahlen, die man wählen würde, kann man `emustarter.py` auch direkt mit diesen Zahlen starten: `emustarter.py 3 2` startet z.B. das zweite Spiel in der Liste von Amiga-Spielen, `emustarter.py 2 5` das fünfte Spiel aus der Liste von Atari-Spielen, und so weiter. So ist die Benutzung von `emustarter.py` nochmal wesentlich schneller.

- Weitere Optionen von `emustarter.py`:
  - `-vol 10`: Setzt die Lautstärke auf einen Wert von `10`. Was `10` in diesem Zusammenhang genau bedeutet, hängt vom jeweiligen Emulator ab.
  - `-nofs`: Nicht im Vollbildmodus starten (sondern in einem Fenster).
  - `-nostart`: Nicht den Emulator starten. Nur die Startzeile für den Emulator ausgeben, und dann beenden.

License: GNU GPL 3.
