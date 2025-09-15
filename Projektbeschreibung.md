# Projekt: Sprachgesteuertes Terminal für Produktionsdaten

## Übersicht  
In diesem Projekt entwickeln Sie ein **sprachgesteuertes Terminal**, mit dem Produktionsdaten (Teilenummer, produzierte Menge, Ausschuss) erfasst und in **SAP** verbucht werden können.  

Das Projekt ist für **3 Studenten** ausgelegt und läuft über ein Semester. Die Arbeit ist in 3 große Arbeitspakete gegliedert, die eng aufeinander aufbauen. 

---

## Use Case  
An einer Produktionsanlage sollen künftig die produzierten Teile nicht mehr manuell in ein Terminal eingegeben, sondern per **Sprache** erfasst werden:

1. Ein Webinterface im Browser zeigt einen **Record-Button** (rotes Kreissymbol) an.  
   - Klick: Aufnahme startet.  
   - Beispiel-Eingabe: „Teil 4711, produziert: 5, Ausschuss: 2“.  
   - Klick auf Stop (Quadratsymbol): Aufnahme wird beendet.  

2. Mit Klick auf „Absenden“ wird die Audioaufnahme an einen Server übertragen.  

3. Der Server verarbeitet die Aufnahme in zwei Schritten:  
   - **Automatic Speech Recognition (ASR)**: Umwandeln von Sprache in Text, z. B. mit **Whisper** oder anderen Speech-to-Text-Modellen.  
   - **Natural Language Understanding (NLU)**: Analysieren des Texts, um zu erkennen, ob eine **Teilenummer**, eine **Produktionsmenge** und eine **Ausschussmenge** angegeben sind. Hierbei kommen oft Verfahren wie **Regex**, **Rule-based NLU**, oder **word2vec / Embeddings** zum Einsatz.  

4. Ergebnis:  
   - Falls gültig → Der Server erzeugt ein **JSON**-Objekt mit den extrahierten Daten und übergibt es an den Browser.  
   - Falls fehlerhaft → Fehlercode an den Browser.  

5. Das JSON wird im Browser ausgewertet und in **SAP** gebucht.  

---

## Arbeitspakete  

### 1. Webfrontend für Audioaufnahme  
- Browser-Interface mit **HTML, CSS, JavaScript**  
- Buttons: Start/Stop/Absenden  
- Audioaufnahme über die **Web Audio API**  
- Versand der Aufnahme an einen Server (z. B. über **HTTP POST** mit **Fetch API**)  

**Technologien zum Recherchieren:**  
- HTML / CSS / JavaScript  
- Web Audio API  
- JSON für Datenaustausch  
- Docker (Containerisierung: reproduzierbare, portable Laufumgebung auf jedem System sicherstellen)

---

### 2. Server: Verarbeitung der Aufnahme (ASR + NLU)  
- Server-Backend mit **Python** und **FastAPI** (alternativ Flask, Django)  
- Deployment mit **uvicorn**  
- Nutzung eines neuronalen Netzes für **ASR**, z. B. **Whisper**  
- Entwicklung eines einfachen **NLU-Moduls**, das den Text analysiert (Teilenummer, Mengen, Ausschuss).  
- Rückgabe der Ergebnisse als JSON  

**Hinweis zum Hosting:**  
Das Backend muss auf einem Server laufen, damit das Frontend (Browser) darauf zugreifen kann.  
Mögliche Optionen, die zu evaluieren und zu dokumentieren sind:  
- **Hugging Face Spaces** (kostenlos, einfaches Hosting für ML-Modelle)  
- **Cloud-Provider** (z. B. AWS, Azure, GCP)  
- **Hochschulrechner** (lokales Deployment mit Zugriff aus dem Uni-Netzwerk)  


Jede Gruppe soll eine **Hosting-Strategie** auswählen und begründen (Kosten, Einfachheit, Performance).
**TODO**: @Mario: Diese Aufgabe den Studenten überlassen oder Komplexität rausnehmen und Hosting-Lösung vorgeben?

**Technologien zum Recherchieren:**  
- Python  
- FastAPI, uvicorn  
- Speech-to-Text (z. B. Whisper, Vosk, Google Speech API)  
- NLU (Regex, Embeddings, word2vec, Spacy, Transformers)  
- JSON  
- Docker

---

### 3. Auswertung und Eintrag in SAP  
- Empfang des JSON am Browser-Terminal  
- Interpretation der Daten (z. B. Visualisierung: „Teil 4711, produziert 5, Ausschuss 2“)  
- Weiterleitung der Daten an SAP (**TODO:** womit? TBD)  

**Technologien zum Recherchieren:**  
- **TODO**: Abklären wie JSON-Daten an SAP weitergereicht werden
- Docker

---

## Lernziele  
Am Ende des Projekts haben Sie:  
- Ein grundlegendes Verständnis von **Webentwicklung** (Frontend + Backend)  
- Erfahrungen im Umgang mit **Spracherkennung (ASR)** und **Sprachverstehen (NLU)** gesammelt  
- Gelernt, wie man Daten in **JSON** strukturiert und verarbeitet  
- Einen Überblick über Integrationsmöglichkeiten in **SAP**  
- Ihre Lösung dokumentiert und Alternativen diskutiert (z. B. verschiedene Speech-to-Text-Engines, Server-Frameworks, Datenbanken, Schnittstellen)  

---

## Hinweise zur Umsetzung  
- Jeder Student übernimmt die Verantwortung für **ein Arbeitspaket** – gleichzeitig ist eine enge Abstimmung erforderlich, da die Pakete aufeinander aufbauen.  
- Dokumentieren Sie:  
  - welche Technologien Sie ausprobiert haben,
  - welche Schwierigkeiten es gab,    
  - warum Sie sich für eine konkrete Lösung entschieden haben.  

---

## Erwartetes Ergebnis  
- Funktionierendes Web-Frontend zur Audioaufnahme  
- Backend-Server, der Audio → Text → JSON umsetzt  
- JSON-Auswertung im Terminal und Übergabe an SAP  
- Projektdokumentation (siehe Dokument "Hinweise zur Durchführung des mechatronischen Projekts" von Prof. Roßdeutscher)  

---

## Benötigtes Vorwissen

Um die Aufgabe in der vorgegebenen Zeit gut lösen zu können werden Grundkenntnisse in Python und FastAPI dringend empfohlen. Die Vorlesung [DEB3_Technische_Informatik](https://moodle.hs-esslingen.de/moodle/course/view.php?id=33208) von Prof. Baumgartl behandelt genau diese Themen.

---

## Literatur

- **TODO**: Relevante Literatur zum Einstieg hinzufügen

---

## Ansprechpartner

Marco Dittmann  
marco.dittmann@hs-esslingen.de
