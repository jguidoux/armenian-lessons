# Génération du son arménien (oriental) → cartes Anki

Transforme une leçon (`lesson_data/NNNN.json`) en un paquet Anki `.apkg` prêt à importer,
avec la prononciation arménienne **intégrée** (lecture auto), dans 3 sens :
reconnaissance (HY→FR), production (FR→HY), saisie (FR→HY tapé).

## Moteur par défaut : Piper local — voix neuronale, hors-ligne, sans compte
Modèle : `davit312/piper-TTS-Armenian` → fichier **`hy_AM-gor-medium.onnx`**
(`hy_AM` = arménien d'Arménie = **oriental**, le bon dialecte). Tourne en local via `onnxruntime`,
aucune clé, aucune carte, aucun quota.

### Installation (une fois)
Le venv Python 3.12 dédié est `~/Learning/Armenian/.venv-tts` (isolé ; supprimable d'un `rm -rf`).
```bash
cd ~/Learning/Armenian
python3.12 -m venv .venv-tts
.venv-tts/bin/pip install -r tts/requirements.txt
```

### Modèle de voix (une fois, ~60 Mo) — déjà téléchargé dans tts/models/
S'il manque :
```bash
mkdir -p tts/models && cd tts/models
curl -sL -o hy_AM-gor-medium.onnx      https://huggingface.co/davit312/piper-TTS-Armenian/resolve/main/v3/hy_AM-gor-medium.onnx
curl -sL -o hy_AM-gor-medium.onnx.json https://huggingface.co/davit312/piper-TTS-Armenian/resolve/main/v3/hy_AM-gor-medium.onnx.json
```

### Générer
```bash
.venv-tts/bin/python tts/generate.py --lesson 0001    # une leçon
.venv-tts/bin/python tts/generate.py --all            # toutes
```
Résultat : `anki/NNNN-slug.apkg`. Les mp3 sont mis en cache dans `audio/` (non régénérés s'ils existent).

### Cartes produites (4 par mot)
- **Reconnaissance** (HY→FR, lecture) · **Saisie** (FR→HY tapé, écriture)
- **Écoute** (son seul, sans texte → deviner le sens, oral) : 2 cartes par mot (le mot + la phrase).
- Sous-paquets : `Arménien::NNNN Titre::{Reconnaissance|Saisie|Écoute}`.
- Option `--with-production` : ajoute un sens FR→HY « de tête » (redondant avec Saisie, off par défaut).

## Importer dans Anki
Double-clic sur le `.apkg` (ou Fichier → Importer). Cartes dans le paquet
**Arménien::NNNN Titre::…**, le son se joue automatiquement.
Réimport d'une leçon déjà importée : les cartes existantes sont mises à jour (guid stable), pas dupliquées.

## Ajouter une future leçon
Créer `lesson_data/NNNN.json` (champs `hy`, `hy_clean`, `pron`, `fr`, `ex_hy`, `ex_fr`)
puis `generate.py --lesson NNNN`. C'est tout.
- `hy` : forme affichée (avec ՞ ։ et accents).
- `hy_clean` : forme à taper en mode saisie (sans ponctuation interne).

## Moteur alternatif (optionnel) : Azure Neural
Voix plus polie (`hy-AM-AnahitNeural`) mais nécessite un compte Azure (clé) :
```bash
export AZURE_SPEECH_KEY=...  AZURE_SPEECH_REGION=francecentral
.venv-tts/bin/python tts/generate.py --all --engine azure
```

## Repères
- Voix humaines natives (oreille de référence) : https://forvo.com/languages/hy/
- Piper est robotique-léger mais correct ; pour vérifier un mot, recoupe avec Forvo.
