"""Modèles Anki partagés pour le cours d'arménien.

Quatre modèles genanki réutilisés par toutes les leçons, avec un style cohérent
avec assets/lesson.css (rouge HY #8a1c1c, sarcelle #2c5f6f). IDs stables : ne JAMAIS
les changer, sinon Anki crée des doublons de type de note à la réimport.

Chaque modèle a un champ `Audio` qui reçoit la balise [sound:...] ; quand il est
non vide, Anki joue le son automatiquement à l'affichage de la face concernée.
"""

import genanki

# IDs stables (générés une fois). Ne pas modifier.
MODEL_RECOGNITION_ID = 1607392319
MODEL_PRODUCTION_ID = 1607392320
MODEL_TYPING_ID = 1607392321
MODEL_LISTENING_ID = 1607392322

# Style commun, aligné sur assets/lesson.css
_CSS = """
.card {
  font-family: "Noto Serif Armenian", "Iowan Old Style", Georgia, serif;
  font-size: 22px;
  text-align: center;
  color: #1a1a1a;
  background: #fdfcf8;
  padding: 18px;
}
.hy { color: #8a1c1c; font-weight: 600; font-size: 34px; line-height: 1.3; }
.fr { font-size: 24px; }
.pron { color: #2c5f6f; font-family: ui-monospace, Menlo, monospace; font-size: 18px; margin-top: 6px; }
.ex { color: #6b6256; font-style: italic; font-size: 18px; margin-top: 12px; }
.ex .hy { font-size: 22px; }
hr#answer { border: none; border-top: 1px solid #e2dccd; margin: 14px 0; }
.tag { font-family: ui-sans-serif, system-ui, sans-serif; font-size: 12px;
  text-transform: uppercase; letter-spacing: .08em; color: #6b6256; }
"""

# 1) RECONNAISSANCE : on voit l'arménien (+ son auto), on retrouve le sens.
recognition_model = genanki.Model(
    MODEL_RECOGNITION_ID,
    "Arménien — Reconnaissance (HY→FR)",
    fields=[
        {"name": "hy"},
        {"name": "pron"},
        {"name": "fr"},
        {"name": "ex_hy"},
        {"name": "ex_fr"},
        {"name": "Audio"},
    ],
    templates=[
        {
            "name": "Reconnaissance",
            "qfmt": '<div class="hy">{{hy}}</div>{{Audio}}',
            "afmt": (
                '{{FrontSide}}<hr id="answer">'
                '<div class="fr">{{fr}}</div>'
                '<div class="pron">[{{pron}}]</div>'
                '<div class="ex"><span class="hy">{{ex_hy}}</span><br>{{ex_fr}}</div>'
            ),
        }
    ],
    css=_CSS,
)

# 2) PRODUCTION : on voit le sens FR, on se rappelle l'arménien (révélé + son auto).
production_model = genanki.Model(
    MODEL_PRODUCTION_ID,
    "Arménien — Production (FR→HY)",
    fields=[
        {"name": "fr"},
        {"name": "hy"},
        {"name": "pron"},
        {"name": "Audio"},
    ],
    templates=[
        {
            "name": "Production",
            "qfmt": '<div class="tag">Dis en arménien</div><div class="fr">{{fr}}</div>',
            "afmt": (
                '{{FrontSide}}<hr id="answer">'
                '<div class="hy">{{hy}}</div>'
                '<div class="pron">[{{pron}}]</div>{{Audio}}'
            ),
        }
    ],
    css=_CSS,
)

# 3) SAISIE : on voit le sens FR, on TAPE l'arménien (comparaison auto), + son à la révélation.
typing_model = genanki.Model(
    MODEL_TYPING_ID,
    "Arménien — Saisie (FR→HY tapé)",
    fields=[
        {"name": "fr"},
        {"name": "hy_clean"},
        {"name": "pron"},
        {"name": "Audio"},
    ],
    templates=[
        {
            "name": "Saisie",
            "qfmt": (
                '<div class="tag">Écris en arménien</div>'
                '<div class="fr">{{fr}}</div>{{type:hy_clean}}'
            ),
            "afmt": (
                '<div class="fr">{{fr}}</div>'
                '<hr id="answer">{{type:hy_clean}}'
                '<div class="pron">[{{pron}}]</div>{{Audio}}'
            ),
        }
    ],
    css=_CSS,
)

# 4) ÉCOUTE PURE : on entend l'arménien (son seul, AUCUN texte), on devine le sens.
#    `Key` (1er champ) = identifiant lisible en navigateur, JAMAIS affiché sur la carte.
listening_model = genanki.Model(
    MODEL_LISTENING_ID,
    "Arménien — Écoute (son→sens)",
    fields=[
        {"name": "Key"},
        {"name": "hy"},
        {"name": "pron"},
        {"name": "fr"},
        {"name": "ex_hy"},
        {"name": "ex_fr"},
        {"name": "Audio"},
    ],
    templates=[
        {
            "name": "Écoute",
            # Recto : uniquement le son (lecture auto + bouton rejouer) + indice neutre.
            "qfmt": '<div class="tag">👂 Écoute et devine</div>{{Audio}}',
            # Verso : on révèle tout. Champs vides gérés par sections conditionnelles.
            "afmt": (
                '<div class="tag">👂 Écoute</div>{{Audio}}'
                '<hr id="answer">'
                '<div class="hy">{{hy}}</div>'
                '{{#pron}}<div class="pron">[{{pron}}]</div>{{/pron}}'
                '<div class="fr">{{fr}}</div>'
                '{{#ex_hy}}<div class="ex"><span class="hy">{{ex_hy}}</span><br>{{ex_fr}}</div>{{/ex_hy}}'
            ),
        }
    ],
    css=_CSS,
)
