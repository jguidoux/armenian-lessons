---
date: 2026-07-04
lesson: "0006 — Déplacements en ville"
---

# Leçon 0006 : se repérer en ville

## Vocabulaire introduit (6 mots)

| Arménien | Prononciation | Français |
|----------|--------------|---------|
| որտեղ | [vortégh] | où ? |
| ձախ | [dzakh] | gauche |
| աջ | [adj] | droite |
| ուղիղ | [oughígh] | tout droit |
| զուգարան | [zougaran] | toilettes |
| տաքսի | [taksi] | taxi |

## Point de grammaire : Որտե՞ղ + է

Même construction que Ո՞նց ես (L01) : mot interrogatif en tête, verbe être (է/ես/եմ) garde sa place.
- Որտե՞ղ է տաքսին։ — Où est le taxi ?
- Զուգարանը որտե՞ղ է։ — Où sont les toilettes ?

Aperçu (non maîtrisé) : suffixe -ը/-ն = article défini collé en fin de mot.

## Trois questions de fond posées par Jérémie — excellent niveau de vigilance

1. **-ը final** : Jérémie a détecté que ma translittération "zougarany" ne correspondait pas au son
   réel du **ը** (schwa [ə], transcrit **ë** dans ce cours) — corrigé en "zougaranë".
2. **գ vs ր dans զուգարան** : question sur la qualité de l'audio Piper (TTS local, limite connue de
   ce moteur gratuit sur les mots moins courants) — orthographe confirmée correcte via dictionnaire.
3. **ուր vs որտեղ** : Jérémie connaissait déjà **ուր** (où → direction/mouvement) et a questionné mon
   choix de **որտեղ** (où → position statique). Distinction confirmée et expliquée.
4. **ղ = ɣ ou ʁ ?** : Jérémie a challengé ma transcription IPA de **ղ** en citant
   fr.wikipedia.org/wiki/Alphabet_arménien. Il avait raison : en arménien oriental, ղ = **[ʁ]**
   (uvulaire, comme un R français), pas [ɣ] (vélaire). **Bug corrigé à la racine** dans
   `tts/validate_lesson.py` (IPA_REF + IPA_FORBIDDEN pour 0x572) — bénéficiera à toutes les leçons futures.

## Révision de session (erreurs L05 fraîches)

Correction en direct de deux confusions de lettres vues dans l'échange précédent :
- **ա** [a] vs **խ** [kh] (confondues dans Շնորհակալություն)
- **ն** [n] vs **մ** [m] (finale de Շնորհակալություն)

## Évidence de maîtrise

- **աջ** [adj] produit correctement en réponse isolée à une mise en situation (« si les toilettes
  sont à droite... »).
- **Bilan copié via le nouveau bouton 📋 (premier usage réel) : 5/5 (100%)** sur les exercices de la
  leçon (QCM « où est le taxi », « ձախ → tourner à gauche », bonus négation, saisie ուղիղ, saisie
  զուգարան) + 3/3 cartes-flip vues. Les deux QCM de révision (ա/խ, ն/մ) n'ont pas été refaits sur la
  page — déjà traités à l'oral en session, donc pas un oubli.
- Cette preuve confirme la maîtrise de **tout** le vocabulaire L06 (որտեղ, ձախ, աջ, ուղիղ, զուգարան,
  տաքսի), pas seulement աջ — à promouvoir dans GLOSSARY.md.

## À suivre

- Reprendre ուր (direction) dans une future leçon sur les verbes de mouvement (գնալ = aller).
- Decks Anki L03/L04 toujours en attente de génération (report récurrent, à vérifier).
- Le bouton 📋 bilan a été corrigé en session (il affichait "copié" même en cas d'échec silencieux de
  l'API presse-papier, typiquement depuis un téléphone) — comportement fiable confirmé par ce premier
  usage réel.
