# Laufökonomie

Ökonometrie für Läufer: Wie effizient setzt ein Läufer seine Herzschläge in Strecke
um? Wovon hängt das ab: Dauer, Höhenmeter, Trainingsfortschritt? Und wie verlässlich
sind solche Aussagen?

Das Projekt ist ein **Lern- und Forschungsprojekt**. Ich will die Denkweise der
Ökonometrie wieder einüben und an echten Laufdaten anwenden:

- Hypothesen formulieren, bevor gerechnet wird
- Streuung und Gleichläufigkeit (Korrelation) zwischen Variablen betrachten und interpretieren
- Modelle schätzen, prüfen, verwerfen, ausbauen; Parameter bereinigen
- Kennzahlen für Laufökonomie und Effizienz herausrechnen
- jede Herleitung nachvollziehbar und reproduzierbar veröffentlichen

Anlass ist die eigene Vorbereitung auf einen 100-km-Ultratrail. Die Methoden sind
aber allgemein gehalten.

## Notebooks

| Nr. | Thema | Inhalt |
|---|---|---|
| [01](notebooks/01_effizienz_modell.ipynb) | Effizienz pro Herzschlag, ein Läufer | Kennzahl EF, Hypothesen, OLS, Bootstrap, Permutationstest, robuste Standardfehler, Validierung außerhalb der Stichprobe, Höhenmeter-Äquivalent |

Die Notebooks sind ausgeführt eingecheckt. GitHub zeigt sie samt Formeln und Grafiken
direkt an.

## Die zentrale Kennzahl

**Effizienz (EF)** = Meter pro Herzschlag = Distanz / (Ø-Herzfrequenz × Dauer in Minuten).
Daraus folgt die Pace bei gegebenem Puls: Pace [min/km] = 1000 / (EF × HF).
Die Herleitung steht in Notebook 01.

## Fragestellungen und Hypothesen

- **H1:** Längere Läufe sind weniger effizient (kardialer Drift).
  *Stand Notebook 01:* Die Punktschätzung ist negativ, aber mit robusten Verfahren nicht gesichert.
- **H2:** Höhenmeter senken die Effizienz. Wie viele Höhenmeter entsprechen 1 km flach?
  *Stand:* Bei einem Straßenläufer sind es etwa 285 Hm, deutlich mehr als die ITRA-Faustregel von 100 Hm.
- **H3:** Die Effizienz steigt mit den Trainingsjahren.
- *offen:* Unterscheiden sich die Effekte zwischen Läufern systematisch, zum Beispiel nach Geschlecht oder Umfang?
- *offen:* Wie entwickeln Ultraläufer ihren Wochenumfang vor einem Ultra?

## Methodischer Werkzeugkasten

| Schritt | Werkzeug |
|---|---|
| explorativ | Streudiagramme, Pearson und Spearman, bedingte Verteilungen |
| schätzen | OLS (`statsmodels`), später Panel-Modelle mit Fixed Effects |
| Unsicherheit | Standardfehler, t, p, Konfidenzintervalle, Bootstrap, Permutationstests |
| Diagnostik | Residuenplots, Breusch-Pagan, robuste Standardfehler (HC3), VIF, Einflussmaße |
| Validierung | Vorhersage außerhalb der Stichprobe (zeitlicher Split), Kreuzvalidierung |

## Daten und Umgang mit Daten Dritter

| Datensatz | Inhalt | Lizenz |
|---|---|---|
| [mikeyfera1/running-races-strava](https://github.com/mikeyfera1/running-races-strava) | 42.116 Läufe von 116 Strava-Nutzern, je Lauf Summen und Mittelwerte | keine angegeben |

**Regeln:**
1. **Daten Dritter werden nicht in diesem Repo gespeichert.** Der Code lädt sie zur
   Laufzeit aus der Originalquelle, auf einen Commit festgelegt und mit Prüfsumme
   (`src/laufoekonomie/daten.py`). Zwischengespeichert wird nur lokal in `data/`;
   dieser Ordner ist git-ignoriert.
2. **Pseudonymisierung:** Athleten-IDs sind vermutlich echte Strava-IDs und damit
   personenbezogen. In allen Ausgaben erscheinen nur Pseudonyme (`L-xxxxxx`).
3. Veröffentlicht werden Code, Herleitungen und aggregierte Ergebnisse, keine
   Trainingstagebücher einzelner Personen.
4. Eigene Daten kommen nur bereinigt hinzu: ohne GPS-Spuren und ohne Gesundheitsangaben.

Die Auswertung stützt sich auf die Schranken für Text- und Data-Mining (§§ 44b, 60d UrhG).
Wer Rechte an einem Datensatz hat und Einwände hat: bitte ein Issue eröffnen.

## Struktur

```
notebooks/            Herleitungen (ausgeführt eingecheckt)
src/laufoekonomie/    wiederverwendbarer Code (Datenladen, Kennzahlen)
data/                 lokaler Zwischenspeicher, nicht im Repo
```

## Loslegen

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/jupyter lab notebooks/
```

Alternativ öffnest du den Ordner in VS Code mit der Jupyter-Erweiterung und wählst `.venv` als Kernel.

## Roadmap

- [x] 01: Effizienzmodell für einen Läufer mit Diagnostik
- [ ] 01b: einflussreiche Beobachtungen (Cook's Distance, Leverage), H1 ohne Ausreißer
- [ ] 02: dasselbe Modell für alle Läufer, Verteilung der Koeffizienten, Heterogenität
- [ ] 03: Panel-Modell (gepoolt vs. Fixed Effects vs. Random Effects, Hausman-Test)
- [ ] 04: Nichtlinearitäten und Interaktionen (Dauer², Dauer × Hm)
- [ ] 05: Wochenumfang und Belastungsverlauf von Ultraläufern
- [ ] Veröffentlichung als Website mit Quarto und GitHub Pages
- [ ] Lizenzanfrage an die Datensatz-Autoren

## Lizenz

Noch offen. Für den Code ist MIT vorgesehen, für Texte und Grafiken CC BY 4.0.
