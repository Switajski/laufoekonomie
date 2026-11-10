"""Laden und Aufbereiten externer Laufdaten.

Grundsatz: Daten Dritter werden zur Laufzeit aus der Originalquelle geladen und nur
lokal zwischengespeichert (Ordner ``data/``, git-ignoriert). Sie werden nicht
mit diesem Repository verbreitet.
"""
from __future__ import annotations

import hashlib
import urllib.request
from pathlib import Path

import numpy as np
import pandas as pd

DATA_DIR = Path(__file__).resolve().parents[2] / "data"

QUELLEN = {
    "running-races-strava": {
        "url": "https://raw.githubusercontent.com/mikeyfera1/running-races-strava/"
               "516d1f3b4b3d2248ca96326b212c7f397fa5ee4d/data.csv",
        "sha256": "1c24d2252a14c71918644b6903a16f3e3008759c2330a5a6a0f01e9b385db9c9",
        "repo": "https://github.com/mikeyfera1/running-races-strava",
    },
}


def lade_rohdaten(name: str) -> Path:
    """Lädt einen Datensatz (gepinnter Commit) und prüft die Prüfsumme."""
    q = QUELLEN[name]
    ziel = DATA_DIR / name / Path(q["url"]).name
    if not ziel.exists():
        ziel.parent.mkdir(parents=True, exist_ok=True)
        req = urllib.request.Request(q["url"], headers={"User-Agent": "laufoekonomie"})
        with urllib.request.urlopen(req, timeout=120) as r:
            ziel.write_bytes(r.read())
    ist = hashlib.sha256(ziel.read_bytes()).hexdigest()
    if ist != q["sha256"]:
        raise ValueError(f"Prüfsumme stimmt nicht für {ziel} – Datei geändert?")
    return ziel


def pseudonym(athlet_id: int | str) -> str:
    """Stabiles Pseudonym statt der (vermutlich echten) Strava-ID."""
    return "L-" + hashlib.sha256(f"laufoekonomie:{athlet_id}".encode()).hexdigest()[:6]


def lade_laeufe() -> pd.DataFrame:
    """running-races-strava als aufbereiteter DataFrame, ein Lauf pro Zeile.

    Abgeleitete Spalten:
      km, dauer_min, dauer_h, pace (min/km), hm_pro_km,
      ef = Meter pro Herzschlag = Distanz / (Ø-HF × Dauer in min),
      plausibel (bool) und auffaelligkeit (Text).
    """
    roh = pd.read_csv(lade_rohdaten("running-races-strava"), sep=";")
    d = pd.DataFrame({
        "athlet": roh["athlete"].map(pseudonym),
        "geschlecht": roh["gender"],
        "start": pd.to_datetime(roh["timestamp"], format="%d/%m/%Y %H:%M"),
        "km": roh["distance (m)"] / 1000,
        "dauer_min": roh["elapsed time (s)"] / 60,
        "hm": roh["elevation gain (m)"],
        "hf": roh["average heart rate (bpm)"],
    })
    d["dauer_h"] = d.dauer_min / 60
    d["pace"] = np.where(d.km > 0, d.dauer_min / d.km.where(d.km > 0), np.nan)
    d["hm_pro_km"] = d.hm / d.km.where(d.km > 0)

    gruende = pd.DataFrame({
        "Distanz 0": d.km <= 0,
        "Dauer 0": d.dauer_min <= 0,
        "Pace < 2:30": d.pace < 2.5,
        "Pace > 20": d.pace > 20,
        "Dauer > 48 h": d.dauer_h > 48,
        "HF unplausibel": d.hf.notna() & ((d.hf < 40) | (d.hf > 220)),
        "> 250 Hm/km": d.hm_pro_km > 250,
    })
    d["plausibel"] = ~gruende.any(axis=1)
    d["auffaelligkeit"] = gruende.apply(lambda r: "; ".join(r.index[r]), axis=1)
    schlaege = d.hf * d.dauer_min
    d["ef"] = np.where(d.plausibel & d.hf.notna(), d.km * 1000 / schlaege, np.nan)
    return d
