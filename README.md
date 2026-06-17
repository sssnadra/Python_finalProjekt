# Python_finalProjekt

# Drinking Game (lecker lecker Bierchen)

## Projektbeschreibung

**Lecker, lecker Bierchen!** ist ein Multiplayer-Zufallszahlenspiel mit grafischer Benutzeroberfläche. Das Spiel wurde in **Python 3** mit **Tkinter** umgesetzt und ist als Partyspiel konzipiert.

Die Spieler würfeln abwechselnd eine Zufallszahl zwischen 1 und 5. Je nach Ergebnis werden Punkte gesammelt oder Trink-Runden ausgelöst. Das Spiel läuft so lange, bis nur noch ein aktiver Spieler übrig ist.

Das Projekt wurde objektorientiert aufgebaut und eignet sich als Python-Abschlussprojekt auf FH-Schülerniveau.

---

## Verwendete Technologien

* Python 3
* Tkinter für die grafische Benutzeroberfläche
* random für die Zufallszahlen
* Standardbibliotheken von Python

Es werden keine zusätzlichen Pakete oder externen Dateien benötigt.

---

## Projektstruktur

Das gesamte Projekt befindet sich in einer einzigen Datei:

```text
main.py
```

Die Datei enthält alle Klassen, die Spiellogik und die grafische Oberfläche.

---

## Spielidee

Zu Beginn werden die Spielernamen eingegeben. Danach würfeln die Spieler abwechselnd.

Wird eine Zahl von **2 bis 5** gewürfelt, wird diese Zahl zum aktuellen Score des Spielers addiert.

Wird eine **1** gewürfelt, passiert Folgendes:

* Der Spieler muss trinken.
* Die Anzahl der Schlucke entspricht dem aktuellen Score.
* Danach wird der Score des Spielers auf 0 gesetzt.
* Die Anzahl der Trink-Runden wird erhöht.
* Ein Bier-Symbol wird angezeigt.

Nach jeder fünften Trink-Runde eines Spielers wird ein Zungenbrecher-Test ausgelöst.

---

## Zungenbrecher-Test

Bei jeder fünften Trink-Runde muss der betroffene Spieler folgenden Satz laut aufsagen:

```text
Auf den sieben Robbenklippen sitzen sieben Robbensippen, die sich in die Rippen stippen, bis sie von den Klippen kippen.
```

Der Test kann bestanden oder nicht bestanden werden.

Wenn der Spieler den Test nicht besteht, bekommt er einen zweiten Versuch. Besteht er auch den zweiten Versuch nicht, kann er aus dem Spiel entfernt werden.

Ausgeschiedene Spieler werden im Scoreboard markiert und bei zukünftigen Spielzügen übersprungen.

---

## Spielende

Das Spiel hat keine feste Rundenzahl.

Es endet automatisch, sobald nur noch ein Spieler aktiv ist. Dieser Spieler gewinnt das Spiel.

Nach dem Spielende kann das Spiel neu gestartet oder beendet werden.

---

## Funktionen

Das Spiel enthält folgende Funktionen:

* Startbildschirm mit Spielernamen
* Auswahl der Spieleranzahl
* Mindestens 2 Spieler
* Bis zu 6 Spieler möglich
* Eingabeprüfung für leere oder doppelte Spielernamen
* Zufallszahl zwischen 1 und 5
* Live-Scoreboard
* Anzeige des aktiven Spielers
* Anzeige von Würfelergebnissen
* Trink-Runden-System
* Zungenbrecher-Test
* Ausscheiden von Spielern
* Automatische Gewinnerermittlung
* Neustart-Funktion
* Beenden-Funktion

---

## Live-Scoreboard

Während des Spiels werden folgende Werte angezeigt:

* Spielername
* Aktueller Score
* Anzahl der Würfe
* Anzahl der gewürfelten 1er
* Anzahl der Trink-Runden
* Anzahl der nicht bestandenen Tests
* Status: aktiv oder ausgeschieden

---

## Klassenübersicht

### Player

Die Klasse `Player` speichert alle Daten eines Spielers.

Dazu gehören:

* Name
* Score
* Anzahl der Würfe
* Anzahl der gewürfelten 1er
* Anzahl der Trink-Runden
* Anzahl der nicht bestandenen Tests
* Status aktiv oder ausgeschieden

---

### GameLogic

Die Klasse `GameLogic` enthält die eigentliche Spiellogik.

Sie verwaltet:

* Die Spielerliste
* Den aktuellen Spieler
* Die Würfelergebnisse
* Die Punktevergabe
* Die Trink-Runden
* Das Ausscheiden von Spielern
* Die Gewinnerermittlung

Diese Klasse enthält keine Tkinter-Befehle. Dadurch ist die Spiellogik sauber von der Benutzeroberfläche getrennt.

---

### GameApp

Die Klasse `GameApp` verwaltet die grafische Oberfläche mit Tkinter.

Sie ist zuständig für:

* Startbildschirm
* Spielbildschirm
* Buttons
* Meldungen
* Scoreboard
* Zungenbrecher-Test
* Gewinneranzeige

---

## Installation

Eine Installation ist nicht notwendig.

Voraussetzung ist lediglich eine funktionierende Python-3-Installation.

---

## Programm starten

Das Spiel wird über die Datei `main.py` gestartet.

Im Terminal oder in der PowerShell:

```bash
python main.py
```

Je nach System kann auch folgender Befehl nötig sein:

```bash
python3 main.py
```

---

## Bedienung

1. Programm starten.
2. Spieleranzahl auswählen.
3. Spielernamen eingeben.
4. Auf **Spiel starten** klicken.
5. Der aktive Spieler würfelt mit dem Button **Riskier den Schluck**.
6. Das Spiel folgt automatisch den Regeln.
7. Nach einer Trinkmeldung wird mit **Weiter zum nächsten Spieler** fortgesetzt.
8. Wenn nur noch ein Spieler aktiv ist, endet das Spiel automatisch.

---

## Wichtiger Hinweis

Dieses Spiel ist als Programmierprojekt und Partyspiel gedacht.

Alkoholische Getränke dürfen ausschließlich von volljährigen Personen konsumiert werden. Alkohol sollte verantwortungsvoll konsumiert werden. Übermäßiger Alkoholkonsum kann gesundheitsschädlich sein.

Das Spiel kann auch ohne Alkohol gespielt werden, zum Beispiel mit Wasser, Saft oder symbolischen Aufgaben.

---

## Mögliche Erweiterungen

Das Projekt kann später erweitert werden, zum Beispiel durch:

* Speicherung von Spielergebnissen
* Weitere Minispiele
* Mehr Zungenbrecher
* Schwierigkeitsstufen
* Soundeffekte
* Eigenes Design mit Farben
* Alternative Strafen ohne Alkohol
* Statistiken am Spielende

---

## Autorinnen und Autoren

Projektmitglieder:

* Sandra Sollberger
* Vanessa Berger

---

## Fazit

Das Projekt zeigt grundlegende und wichtige Python-Konzepte:

* Objektorientierte Programmierung
* Arbeiten mit Klassen und Objekten
* Trennung von Logik und Benutzeroberfläche
* Ereignisgesteuerte Programmierung mit Tkinter
* Eingabevalidierung
* Arbeiten mit Zufallszahlen
* Aktualisierung einer grafischen Oberfläche

Dadurch eignet sich das Spiel gut für eine Präsentation oder mündliche Erklärung im Rahmen eines Python-Abschlussprojekts.
