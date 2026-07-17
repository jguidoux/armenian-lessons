# Ajouter le son (prononciation arménienne) aux cartes Anki

Je ne peux pas livrer des fichiers .mp3 directement (téléchargement audio bloqué côté serveur).
Deux façons d'avoir le son dans Anki — Anki génère la voix lui-même.

## Option A — TTS natif Anki (gratuit, sans module)
Marche sur Anki Desktop + AnkiDroid. Requiert une **voix arménienne** installée sur l'appareil
(Réglages système → Synthèse vocale / Voix → ajouter « Arménien »).

Éditer le **modèle de carte** : ouvrir une note → bouton **« Cartes… »**, puis ajouter la balise.

- Jeu **Reconnaissance** (arménien au Recto) → dans le **Recto** :
  ```
  {{Recto}}
  {{tts hy_AM:Recto}}
  ```
- Jeux **Production** / **Saisie** (arménien au Verso) → dans le **Verso** :
  ```
  {{tts hy_AM:Verso}}
  ```

La carte lit l'arménien automatiquement à l'affichage.
Limite : voix système robotique, absente sur certains appareils.

## Option B — module HyperTTS (voix plus naturelle, recommandé)
1. Anki Desktop → Outils → Modules complémentaires → Obtenir des modules → code **111623432** → redémarrer.
2. Browse → sélectionner les cartes → menu **HyperTTS** → langue **Arménien (hy)** + une voix → appliquer au champ arménien.
3. Insère un `[sound:…]` dans chaque carte (audio embarqué, dispo hors-ligne ensuite).

## Repère
- Champ arménien = **Recto** dans `NNNN-theme.tsv` ; = **Verso** dans `-production.tsv` et `-saisie.tsv`.
- Voix natives humaines (écoute de référence) : https://forvo.com/languages/hy/
