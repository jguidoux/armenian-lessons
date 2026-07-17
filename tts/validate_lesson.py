#!/usr/bin/env python3
"""
validate_lesson.py — Validation pédagogique des leçons arméniennes.

Usage:
    python3 tts/validate_lesson.py --lesson 0005
    python3 tts/validate_lesson.py --all

Exit codes: 0=OK  1=avertissements  2=erreurs
"""

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent

# ── Table IPA de référence (arménien oriental) ──────────────────────────────
# Source: https://fr.wikipedia.org/wiki/Alphabet_arm%C3%A9nien
IPA_REF = {
    0x561: ["ɑ"],           # ա
    0x562: ["b"],           # բ
    0x563: ["ɡ"],           # գ  ← U+0261, pas g latin
    0x564: ["d"],           # դ
    0x565: ["e", "je"],     # ե  (médian / initial)
    0x566: ["z"],           # զ
    0x567: ["ɛ"],           # է
    0x568: ["ə"],           # ը  ← schwa U+0259
    0x569: ["tʰ"],          # թ
    0x56A: ["ʒ"],           # ժ
    0x56B: ["i"],           # ի
    0x56C: ["l"],           # լ
    0x56D: ["χ"],           # խ  ← U+03C7 OBLIGATOIRE (uvulaire)
    0x56E: ["ts"],          # ծ
    0x56F: ["k"],           # կ
    0x570: ["h"],           # հ
    0x571: ["dz"],          # ձ
    0x572: ["ʁ"],           # ղ  ← uvulaire U+0281 (arménien oriental ; fr.wikipedia.org/wiki/Alphabet_arménien)
    0x573: ["tʃ"],          # ճ
    0x574: ["m"],           # մ
    0x575: ["j"],           # յ
    0x576: ["n"],           # ն
    0x577: ["ʃ"],           # շ
    0x578: ["o", "vo"],     # ո  (médian / initial)
    0x579: ["tʃʰ"],         # չ
    0x57A: ["p"],           # պ
    0x57B: ["dʒ"],          # ջ
    0x57C: ["r"],           # ռ  (roulée)
    0x57D: ["s"],           # ս
    0x57E: ["v"],           # վ
    0x57F: ["t"],           # տ
    0x580: ["ɾ"],           # ր  ← battue U+027E
    0x581: ["tsʰ"],         # ց
    0x582: ["w", "u"],      # ւ  (partie de ու)
    0x583: ["pʰ"],          # փ
    0x584: ["kʰ"],          # ք
    0x585: ["o"],           # օ
    0x586: ["f"],           # ֆ
    0x587: ["ev", "yev"],   # և  ligature
}

# Symboles IPA INTERDITS pour certaines lettres arméniennes
IPA_FORBIDDEN = {
    0x56D: ["x", "х"],  # խ → ni x latin (0078) ni х cyrillique (0445)
    0x568: ["e"],            # ը → pas e simple (doit être ə U+0259)
    0x563: ["g"],            # գ → pas g simple (doit être ɡ U+0261, acceptable warning)
    0x580: ["r"],            # ր → pas r simple (doit être ɾ U+027E, acceptable warning)
    0x572: ["ɣ"],            # ղ → pas ɣ vélaire (doit être ʁ U+0281 uvulaire, arménien oriental)
}

ARMENIAN_RANGE = range(0x531, 0x590)
CYRILLIC_RANGE = range(0x400, 0x500)
LATIN_BASIC    = range(0x41, 0x7B)   # A-z

ALLOWED_IN_HY  = set(" \t\n") | {".", ",", "!", "?", ":", ";", "«", "»", "—", "-",
                                   "՝",  # ՝ apostrophe arménienne
                                   "՞",  # ՞ point interrogatif
                                   "։",  # ։ point final
                                   "֊",  # ֊ tiret
                                   "«", "»",
                                   "_",  # ___ placeholder fill-in-the-blank
                                   "[", "]",  # [prénom] placeholders intentionnels
                                   "…",  # … ellipse (U+2026)
                                   }


def is_armenian(c):
    return ord(c) in ARMENIAN_RANGE


def check_armenian_unicode(text, context=""):
    """Vérifie que le texte ne contient que des caractères arméniens valides."""
    errors = []
    for i, c in enumerate(text):
        cp = ord(c)
        if c in ALLOWED_IN_HY:
            continue
        if cp not in ARMENIAN_RANGE:
            category = "cyrillique" if cp in CYRILLIC_RANGE else \
                       "latin"     if cp in LATIN_BASIC     else \
                       f"U+{cp:04X}"
            errors.append(f"  ERREUR [{context}] char {repr(c)} ({category}) pos={i} : «{text}»")
    return errors


def letters_in_armenian(word):
    """Retourne les codepoints arméniens (hors ponctu./espaces) d'un mot."""
    return [ord(c) for c in word if ord(c) in ARMENIAN_RANGE]


def check_ipa_for_word(hy_word, ipa_str, context=""):
    """Vérifie que l'IPA utilisée est cohérente avec les lettres arméniennes."""
    warnings = []
    errors = []
    for cp in letters_in_armenian(hy_word):
        if cp not in IPA_FORBIDDEN:
            continue
        for bad_sym in IPA_FORBIDDEN[cp]:
            if bad_sym in ipa_str:
                letter = chr(cp)
                expected = IPA_REF.get(cp, ["?"])[0]
                severity = "ERREUR" if cp == 0x56D else "AVERT."
                msg = (f"  {severity} [{context}] IPA «{ipa_str}» contient «{bad_sym}» "
                       f"pour {letter} (U+{cp:04X}) → attendu «{expected}»")
                (errors if severity == "ERREUR" else warnings).append(msg)
    return errors, warnings


def validate_html(lesson_id):
    candidates = list(ROOT.glob(f"lessons/{lesson_id}-*.html"))
    if not candidates:
        return [f"  ERREUR fichier HTML introuvable pour leçon {lesson_id}"], [], 0
    html_file = candidates[0]
    html = html_file.read_text(encoding="utf-8")
    errors, warnings = [], []
    hy_count = 0

    # 1. Caractères arméniens dans les spans .hy
    # Les placeholders [xxx] sont intentionnels — retirés avant contrôle
    for m in re.finditer(r'class="hy[^"]*"[^>]*>([^<]+)<', html):
        text = m.group(1).strip()
        if not text:
            continue
        hy_count += 1
        clean = re.sub(r'\[[^\]]*\]', '', text)  # retire [prénom], [___], etc.
        errs = check_armenian_unicode(clean, f"HTML .hy «{text[:20]}»")
        errors.extend(errs)

    # 2. data-src non vide
    for m in re.finditer(r'<button class="sound"([^>]*)>', html):
        attrs = m.group(1)
        if 'data-src=""' in attrs:
            errors.append(f"  ERREUR [HTML] data-src vide dans bouton son")
        if attrs.count("data-src=") > 1:
            errors.append(f"  ERREUR [HTML] attribut data-src dupliqué")

    # 3. IPA dans les spans .pron — croiser avec les .hy précédents
    hy_spans  = re.findall(r'class="hy[^"]*"[^>]*>([^<]+)<', html)
    pron_spans = re.findall(r'class="pron"[^>]*>([^<]+)<', html)
    for hy_w, ipa_w in zip(hy_spans, pron_spans):
        hy_w = hy_w.strip(); ipa_w = ipa_w.strip()
        errs, warns = check_ipa_for_word(hy_w, ipa_w, f"HTML pron «{hy_w}»")
        errors.extend(errs); warnings.extend(warns)

    # 4. IPA dans les phonétiques de dialogue [entre crochets]
    for m in re.finditer(r'<small>\[([^\]]+)\]', html):
        ipa_txt = m.group(1)
        # Vérifier symboles interdits universellement
        if chr(0x0445) in ipa_txt:
            errors.append(f"  ERREUR [HTML dialogue] х cyrillique (U+0445) dans phonétique «{ipa_txt}»")
        if chr(0x0078) in ipa_txt and "χ" not in ipa_txt:
            warnings.append(f"  AVERT. [HTML dialogue] x latin dans phonétique «{ipa_txt}» (attendu χ si son /χ/)")

    # 5. Cohérence dialogue : mots arménien == mots phonétique par ligne
    for m in re.finditer(
        r'<div class="line">.*?<span class="hy">([^<]+)</span>\s*<small>\[([^\]]+)\]',
        html, re.DOTALL
    ):
        hy_words   = m.group(1).strip().split()
        pron_words = m.group(2).strip().split()
        if len(hy_words) != len(pron_words):
            warnings.append(
                f"  AVERT. [dialogue] mots HY={len(hy_words)} ≠ PRON={len(pron_words)} "
                f"pour «{m.group(1).strip()[:30]}»"
            )

    return errors, warnings, hy_count


def validate_json(lesson_id):
    json_file = ROOT / "tts" / "lesson_data" / f"{lesson_id}.json"
    if not json_file.exists():
        return [f"  ERREUR JSON introuvable : {json_file}"], [], 0
    data = json.loads(json_file.read_text(encoding="utf-8"))
    errors, warnings = [], []
    required = {"hy", "hy_clean", "pron", "fr", "ex_hy", "ex_fr"}

    for i, entry in enumerate(data.get("entries", [])):
        ctx = f"JSON entrée {i+1} «{entry.get('hy','?')[:15]}»"
        missing = required - set(entry.keys())
        if missing:
            errors.append(f"  ERREUR [{ctx}] champs manquants : {missing}")
            continue

        # Arménien pur dans hy et ex_hy
        # Les placeholders [xxx] dans ex_hy sont intentionnels — on les retire avant contrôle
        for field in ("hy", "hy_clean", "ex_hy"):
            text = entry[field]
            if field == "ex_hy":
                text = re.sub(r'\[[^\]]*\]', '', text)  # retire [prénom], [nom], etc.
            errs = check_armenian_unicode(text, f"{ctx} .{field}")
            errors.extend(errs)

        # hy_clean sans ponctuation arménienne spéciale
        for bad_cp in (0x055E, 0x0589):
            if chr(bad_cp) in entry["hy_clean"]:
                warnings.append(
                    f"  AVERT. [{ctx}] hy_clean contient U+{bad_cp:04X} (doit être nettoyé)"
                )

        # IPA dans pron
        errs, warns = check_ipa_for_word(entry["hy"], entry["pron"], f"{ctx} .pron")
        errors.extend(errs); warnings.extend(warns)

    return errors, warnings, len(data.get("entries", []))


def validate_lesson(lesson_id):
    print(f"\n{'='*55}")
    print(f"  Leçon {lesson_id}")
    print(f"{'='*55}")

    html_errors, html_warns, hy_count = validate_html(lesson_id)
    json_errors, json_warns, entry_count = validate_json(lesson_id)

    all_errors   = html_errors + json_errors
    all_warnings = html_warns  + json_warns

    # Rapport
    sections = [
        ("Arménien Unicode + cyrillique", [e for e in all_errors   if "cyrillique" in e or "ERREUR [HTML .hy" in e or "ERREUR [JSON" in e]),
        ("IPA",                           [e for e in all_errors   if "IPA" in e or "pron" in e] +
                                          [w for w in all_warnings if "IPA" in w or "pron" in w or "phonétique" in w]),
        ("data-src",                      [e for e in all_errors   if "data-src" in e]),
        ("Cohérence dialogue",            [w for w in all_warnings if "dialogue" in w and "IPA" not in w]),
        ("Structure JSON",                [e for e in all_errors   if "JSON" in e or "champ" in e or "hy_clean" in e] +
                                          [w for w in all_warnings if "hy_clean" in w]),
    ]

    has_error = bool(all_errors)
    has_warn  = bool(all_warnings)

    for title, items in sections:
        if items:
            icon = "❌" if any(i.startswith("  ERREUR") for i in items) else "⚠️ "
            print(f"\n{icon} {title}")
            for item in items:
                print(item)
        else:
            print(f"  ✅ {title} : OK")

    # Résumé
    print(f"\n{'─'*55}")
    print(f"  {hy_count} spans .hy · {entry_count} entrées JSON")
    if all_errors:
        print(f"  ❌ {len(all_errors)} erreur(s) — à corriger avant livraison")
    if all_warnings:
        print(f"  ⚠️  {len(all_warnings)} avertissement(s)")
    if not all_errors and not all_warnings:
        print("  ✅ Tout est valide.")

    return 2 if all_errors else (1 if all_warnings else 0)


def main():
    ap = argparse.ArgumentParser(description="Validation pédagogique des leçons arméniennes")
    ap.add_argument("--lesson", help="Numéro de leçon, ex. 0005")
    ap.add_argument("--all",    action="store_true", help="Valider toutes les leçons")
    args = ap.parse_args()

    if args.all or not args.lesson:
        lessons = sorted({p.name[:4] for p in ROOT.glob("lessons/[0-9][0-9][0-9][0-9]-*.html")})
        if not lessons:
            print("Aucune leçon trouvée.")
            sys.exit(0)
        worst = 0
        for lid in lessons:
            worst = max(worst, validate_lesson(lid))
        sys.exit(worst)
    else:
        sys.exit(validate_lesson(args.lesson))


if __name__ == "__main__":
    main()
