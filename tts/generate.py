#!/usr/bin/env python3
"""Génère les paquets Anki (.apkg) d'une leçon, avec son arménien ORIENTAL intégré.

Moteur par défaut : Piper (modèle local hy_AM-gor-medium, arménien d'Arménie = oriental).
  → 100 % hors-ligne, aucun compte, aucune clé. Voix neuronale (pas robotique).
Moteur optionnel : Azure Neural (--engine azure) si un jour une clé est dispo.

Source : tts/lesson_data/NNNN.json
Sortie : anki/NNNN-slug.apkg   (3 sens : reconnaissance, production, saisie)
Audio  : audio/hy_NNNN_*.mp3    (cache : non régénéré s'il existe déjà)

Usage :
    python tts/generate.py --lesson 0001
    python tts/generate.py --all
    python tts/generate.py --lesson 0001 --engine azure     # nécessite AZURE_SPEECH_KEY/REGION
"""

import argparse
import hashlib
import json
import os
import subprocess
import sys
import tempfile
import wave
from pathlib import Path

import genanki

sys.path.insert(0, str(Path(__file__).resolve().parent))
from anki_models import (  # noqa: E402
    recognition_model, production_model, typing_model, listening_model,
)

ROOT = Path(__file__).resolve().parent.parent          # .../Armenian
TTS_DIR = Path(__file__).resolve().parent
DATA_DIR = TTS_DIR / "lesson_data"
MODEL_DIR = TTS_DIR / "models"
AUDIO_DIR = ROOT / "audio"
ANKI_DIR = ROOT / "anki"

PIPER_MODEL = MODEL_DIR / "hy_AM-gor-medium.onnx"
DECK_BASE_ID = 1987650000
DECK_PARENT = "Armenian-lessons"   # paquet racine dans Anki (séparé d'un éventuel deck "Armenian")

# Voix Azure (oriental hy-AM) — utilisée seulement si --engine azure
AZURE_VOICE = "hy-AM-AnahitNeural"
AZURE_FORMAT = "audio-24khz-48kbitrate-mono-mp3"


def slugify(text: str) -> str:
    return hashlib.md5(text.encode("utf-8")).hexdigest()[:10]


# ---------- Moteur Piper (local, défaut) ----------
_piper_voice = None


def _load_piper():
    global _piper_voice
    if _piper_voice is None:
        from piper import PiperVoice
        if not PIPER_MODEL.exists():
            sys.exit(f"✗ Modèle Piper introuvable : {PIPER_MODEL}\n"
                     "  Télécharge-le (voir tts/README.md).")
        print(f"  (chargement voix Piper {PIPER_MODEL.name})")
        _piper_voice = PiperVoice.load(str(PIPER_MODEL))
    return _piper_voice


def synth_piper(text: str, mp3_path: Path):
    voice = _load_piper()
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
        wav_path = tmp.name
    try:
        with wave.open(wav_path, "wb") as wf:
            voice.synthesize_wav(text, wf)
        subprocess.run(
            ["ffmpeg", "-y", "-loglevel", "error", "-i", wav_path,
             "-b:a", "96k", str(mp3_path)],
            check=True,
        )
    finally:
        os.unlink(wav_path)


# ---------- Moteur Azure (optionnel) ----------
def synth_azure(text: str, mp3_path: Path):
    import requests
    key = os.environ.get("AZURE_SPEECH_KEY")
    region = os.environ.get("AZURE_SPEECH_REGION")
    if not key or not region:
        sys.exit("✗ --engine azure exige AZURE_SPEECH_KEY et AZURE_SPEECH_REGION.")
    esc = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    ssml = (f'<speak version="1.0" xml:lang="hy-AM">'
            f'<voice xml:lang="hy-AM" name="{AZURE_VOICE}">{esc}</voice></speak>')
    r = requests.post(
        f"https://{region}.tts.speech.microsoft.com/cognitiveservices/v1",
        headers={"Ocp-Apim-Subscription-Key": key,
                 "Content-Type": "application/ssml+xml",
                 "X-Microsoft-OutputFormat": AZURE_FORMAT,
                 "User-Agent": "armenian-teach"},
        data=ssml.encode("utf-8"), timeout=30)
    if r.status_code != 200:
        raise RuntimeError(f"Azure {r.status_code} : {r.text[:200]}")
    mp3_path.write_bytes(r.content)


SYNTH = {"piper": synth_piper, "azure": synth_azure}


def get_audio(text: str, lesson: str, engine: str) -> str:
    """Nom de fichier mp3 (en cache), généré si besoin."""
    AUDIO_DIR.mkdir(exist_ok=True)
    fname = f"hy_{lesson}_{slugify(text)}.mp3"
    fpath = AUDIO_DIR / fname
    if not fpath.exists() or fpath.stat().st_size < 500:
        print(f"  ♪ {text}")
        SYNTH[engine](text, fpath)
    return fname


def build_lesson(lesson: str, engine: str, with_production: bool = False) -> Path:
    data = json.loads((DATA_DIR / f"{lesson}.json").read_text(encoding="utf-8"))
    slug, title, entries = data["slug"], data["title"], data["entries"]

    media = set()
    notes_reco, notes_prod, notes_type, notes_listen = [], [], [], []

    for e in entries:
        word_mp3 = get_audio(e["hy_clean"], lesson, engine)
        ex_mp3 = get_audio(e["ex_hy"], lesson, engine)
        media.add(AUDIO_DIR / word_mp3)
        media.add(AUDIO_DIR / ex_mp3)
        word_tag, ex_tag = f"[sound:{word_mp3}]", f"[sound:{ex_mp3}]"

        # Reconnaissance (HY→FR) — lecture
        #   Audio = mot seul (pas la phrase) : ne pas griller à l'avance ce que
        #   la carte Écoute-phrase teste dédiément. guid stable → pas de doublon au réimport.
        notes_reco.append(genanki.Note(
            model=recognition_model,
            guid=genanki.guid_for(lesson, "reconnaissance", e["hy"]),
            fields=[e["hy"], e["pron"], e["fr"], e["ex_hy"], e["ex_fr"], word_tag]))
        # Saisie (FR→HY tapé) — écriture
        notes_type.append(genanki.Note(
            model=typing_model,
            guid=genanki.guid_for(lesson, "saisie", e["hy"]),
            fields=[e["fr"], e["hy_clean"].lower(), e["pron"], word_tag]))
        # Écoute pure (son→sens) — oral. 2 cartes : le mot, puis la phrase.
        #   guid explicite stable → ré-import propre même si on retouche pron/fr.
        #   Le mot n'affiche PAS la phrase d'exemple au verso (déjà le job d'Écoute-phrase,
        #   sinon verso quasi identique à celui de Reconnaissance).
        notes_listen.append(genanki.Note(
            model=listening_model,
            guid=genanki.guid_for(lesson, "ecoute-mot", e["hy"]),
            fields=[f"{e['fr']} 〔mot〕", e["hy"], e["pron"], e["fr"],
                    "", "", word_tag]))
        notes_listen.append(genanki.Note(
            model=listening_model,
            guid=genanki.guid_for(lesson, "ecoute-phrase", e["ex_hy"]),
            fields=[f"{e['fr']} 〔phrase〕", e["ex_hy"], "", e["ex_fr"],
                    "", "", ex_tag]))
        # Production (FR→HY de tête) — optionnelle, redondante avec Saisie
        if with_production:
            notes_prod.append(genanki.Note(
                model=production_model,
                fields=[e["fr"], e["hy"], e["pron"], word_tag]))

    base = int(lesson) * 10 + DECK_BASE_ID
    decks = []
    deck_reco = genanki.Deck(base + 1, f"{DECK_PARENT}::{lesson} {title}::Reconnaissance")
    deck_type = genanki.Deck(base + 3, f"{DECK_PARENT}::{lesson} {title}::Saisie")
    deck_listen = genanki.Deck(base + 4, f"{DECK_PARENT}::{lesson} {title}::Écoute")
    for n in notes_reco:
        deck_reco.add_note(n)
    for n in notes_type:
        deck_type.add_note(n)
    for n in notes_listen:
        deck_listen.add_note(n)
    decks += [deck_reco, deck_type, deck_listen]
    if with_production:
        deck_prod = genanki.Deck(base + 2, f"{DECK_PARENT}::{lesson} {title}::Production")
        for n in notes_prod:
            deck_prod.add_note(n)
        decks.append(deck_prod)

    ANKI_DIR.mkdir(exist_ok=True)
    out = ANKI_DIR / f"{lesson}-{slug}.apkg"
    pkg = genanki.Package(decks)
    pkg.media_files = [str(p) for p in sorted(media)]
    pkg.write_to_file(str(out))
    n_cards = sum(len(x) for x in (notes_reco, notes_type, notes_listen, notes_prod))
    print(f"✓ {out}  ({len(entries)} mots → {n_cards} cartes, {len(media)} sons)")
    return out


def inject_audio_src(lesson: str):
    """Injecte data-src dans le HTML de la leçon après génération des MP3."""
    import re
    html_path = ROOT / "lessons" / f"{lesson}-*.html"
    candidates = list(ROOT.glob(f"lessons/{lesson}-*.html"))
    if not candidates:
        print(f"  ⚠ Aucun fichier HTML trouvé pour la leçon {lesson} (lessons/{lesson}-*.html)")
        return
    html_file = candidates[0]
    html = html_file.read_text(encoding="utf-8")

    data = json.loads((DATA_DIR / f"{lesson}.json").read_text(encoding="utf-8"))
    mapping = {e["hy_clean"]: f"hy_{lesson}_{slugify(e['hy_clean'])}.mp3"
               for e in data["entries"]}

    injected = 0

    def add_src(m):
        nonlocal injected
        hy_val = re.search(r'data-hy="([^"]+)"', m.group(0))
        if not hy_val:
            return m.group(0)
        fname = mapping.get(hy_val.group(1))
        if not fname or f'data-src="../audio/{fname}"' in m.group(0):
            return m.group(0)
        injected += 1
        return m.group(0).replace('data-hy=', f'data-src="../audio/{fname}" data-hy=')

    html_new = re.sub(r'<button class="sound"[^>]*>', add_src, html)
    html_file.write_text(html_new, encoding="utf-8")
    print(f"  ✓ {html_file.name} — {injected} bouton(s) mis à jour avec data-src")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lesson", help="numéro, ex. 0001")
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--engine", choices=["piper", "azure"], default="piper")
    ap.add_argument("--with-production", action="store_true",
                    help="ajoute le 3e sens 'Production' (FR→HY de tête), redondant avec Saisie")
    ap.add_argument("--update-html", action="store_true",
                    help="injecte data-src dans le HTML de la leçon après génération audio")
    args = ap.parse_args()

    if args.all:
        lessons = sorted(p.stem for p in DATA_DIR.glob("*.json"))
    elif args.lesson:
        lessons = [args.lesson]
    else:
        sys.exit("✗ Précise --lesson NNNN ou --all.")

    for lesson in lessons:
        print(f"== Leçon {lesson} (moteur: {args.engine}) ==")
        build_lesson(lesson, args.engine, args.with_production)
        if args.update_html:
            inject_audio_src(lesson)


if __name__ == "__main__":
    main()
