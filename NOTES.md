# Notes & préférences d'apprentissage

## ⚙️ Règles de génération — LIRE EN PREMIER

### Caractères arméniens
- **Jamais taper** de caractères arméniens directement dans Edit/Write/Bash heredoc.
  Les codepoints arméniens (U+0531–U+058F) sont visuellement identiques à des caractères cyrilliques/grecs → erreurs silencieuses sans aucun avertissement.
- **Toujours** générer via Python : `chr(0x569)+chr(0x587)+chr(0x575)` pour թeyl (thé).
- Vérifier les codepoints via `hexdump -C` sur un fichier existant, ou en décodant les URLs Forvo (percent-encoding).

### Structure HTML — composants
Avant d'écrire une leçon, lire `assets/lesson-template.html` et partir de ce squelette.
Structures obligatoires (ne pas improviser) :
- Carte flip : `<div class="flip"><div class="front"><span class="prompt-hint">…</span>…</div><div class="back">…</div></div>`
- QCM option : `<button class="opt" data-correct="1">texte</button>`
- Son : `<button class="sound" data-hy="[arménien via Python]">🔊</button>`
  ⚠️ **NE PAS écrire `data-src=""`** dans le HTML initial — omettre complètement l'attribut `data-src`.
  `generate.py --update-html` l'injecte avant `data-hy` ; un `data-src=""` vide crée un attribut dupliqué
  et force le fallback Web Speech API (mauvaise qualité). **Bug récurrent — 3e occurrence en L05.**
- Saisie : `<div class="saisie"><p class="q">…</p><div class="saisie-row"><input lang="hy"><button class="saisie-submit">→</button></div><div class="saisie-answer" data-answer="[minuscule via Python]">[affiché si faux]</div><div class="feedback"></div></div>`
- Bilan copiable (`assets/report.js`, ajouté 04/07) : bouton **« 📋 Copier mon bilan »** injecté
  automatiquement avant `<div class="footer">` sur toute page qui charge le script. Scanne
  `.quiz`/`.saisie`/`.flip` déjà répondus et copie un résumé texte dans le presse-papier, pour que
  Jérémie le colle directement au professeur (Claude) — permet de baser les learning-records sur de
  vraies preuves plutôt que sur du déclaratif. Ajouter `<script src="../assets/report.js"></script>`
  après les autres scripts dans toute nouvelle leçon (déjà fait dans le template et les leçons 0001-0006).
  ⚠️ `data-answer` doit être en **minuscule** arménien (Python `.lower()`) — la comparaison JS est insensible à la casse mais c'est la convention.

### Assets JS — règle IIFE
Tout nouveau bloc CSS dans un fichier `assets/*.js` doit être dans une IIFE :
`(function(){ const css=\`…\`; const s=document.createElement('style'); s.textContent=css; document.head.appendChild(s); })();`
Raison : `audio.js` et `flashcard.js` sont chargés ensemble — `const` global en double = SyntaxError silencieuse.

### Cohérence dialogue
Après chaque `<div class="line">` : vérifier que l'arménien (`.hy`) et la phonétique (`<small>[…]`) contiennent le même nombre de mots. Corriger immédiatement si différent.

### Checklist pré-livraison (obligatoire avant chaque leçon)
1. Vérifier via Python que les codepoints de chaque span `.hy` sont tous dans [0x531–0x58F].
2. Générer l'audio Piper ET injecter les data-src **en une commande** :
   `.venv-tts/bin/python tts/generate.py --lesson NNNN --update-html`
   (les boutons 🔊 seront automatiquement mis à jour dans le HTML)
3. Ouvrir dans le navigateur via http://127.0.0.1:8765 (serveur HTTP local) pour tester l'audio.
4. Vérifier cohérence mots arménien ↔ phonétique dans chaque réplique du dialogue.
5. **Appeler `/validate-armenian-lesson --lesson NNNN`** — valide le fond pédagogique
   (Unicode arménien, IPA, data-src, traductions, cohérence). Corriger avant livraison.

### Saisie libre — phrases complètes (ajouté 04/07, L07)
L'arménien est **pro-drop** (le pronom sujet peut être omis, l'auxiliaire porte la personne — cf.
GLOSSARY.md). Pour un exercice de saisie demandant une phrase complète, ne pas piéger l'apprenant
sur l'absence du pronom sujet : soit accepter les deux formes (avec/sans pronom), soit préciser
explicitement dans la question qu'on veut la forme emphatique avec pronom.

**Note serveur HTTP** : `python3 -m http.server 8765 --bind 127.0.0.1 &` depuis `~/Learning/Armenian`.
Les leçons sont à http://127.0.0.1:8765/lessons/NNNN-*.html (audio Piper fonctionne via HTTP).

---

## 📍 OÙ ON EN EST (maj 05/07/2026)
- **Leçons faites** : 0001 Salutations · 0002 Se présenter · 0003 À table · 0004 La famille ·
  0005 Sentiments (ուրախ, տխուր, հոգնած, լավ, վատ, սոված + structure Ես [adj] եմ) ·
  0006 Déplacements en ville (որտեղ, ձախ, աջ, ուղիղ, զուգարան, տաքսի + structure Որտե՞ղ + է) ·
  0007 La négation (չեմ/չես/չի + bonus չէ/հա « non/oui » familiers — 7/8, détail ci-dessous) ·
  0008 Verbes de mouvement (գնալ/գալ, présent en -ում/-իս + auxiliaire ém/es/é, négation
  avec inversion de l'ordre des mots — maîtrisé, 8/8 le 04/07) ·
  0009 Le temps (երբ, այսօր, վաղը, առավոտ, երեկո + ե՞րբ + position du mot de temps +
  ռ/ր — QCM 6/6, mais saisie 1/3 (78% global), le 05/07) ·
  0010 Révision ciblée production (pas de nouveau vocabulaire — եմ/է, գալ/գնում, խ/ղ —
  11/12, 92%, le 05/07, détail ci-dessous : écart reconnaissance/production de L09 comblé) ·
  0011 En visite (հյուր, Բարի գալուստ, Ցտեսություն, Հաջողություն + consolidation de
  Ինչպե՞ս ես depuis L1 — 8/8, 100%, le 05/07) ·
  0012 Les jours (օր, ինչ, Ուրբաթ, Շաբաթ, Կիրակի + Ի՞նչ օր է այսօր, suite de L09 —
  7/8, 88%, le 05/07) ·
  **0013 Repas approfondi** (ուտել/ուտում եմ, խմել/խմում եմ, մի քիչ + ordre des mots à
  l'affirmatif + ՞ sur verbe simple — **7/7, 100%, le 06/07** après correction d'un bug de
  conception, détail ci-dessous) ·
  **0014 Parler des autres** (նա, անել/անում է, Ի՞նչ է անում — 3e personne -ում+է, jusque-là
  vue en grammaire mais jamais pratiquée — **6/8, 75%, le 10/07**, détail ci-dessous) ·
  **0015 Survie conversationnelle** (Չեմ հասկանում, Խնդրում եմ դանդաղ խոսեք/կրկնեք, Ի՞նչ է
  սա — formules figées, pas de grammaire nouvelle — **6/8, 75%, le 11/07**, détail ci-dessous) ·
  **0016 Petits mots de conversation** (Վայ, Իսկապե՞ս, Հրաշալի է, Ինչքան լավ է — réactions,
  pas de grammaire nouvelle — **7/8, 88%, le 12/07**, détail ci-dessous).
- **Prochaine session → Leçon 0017** : liste de 5 sujets validée en session de planification
  du 10/07 (voir `~/.claude/plans/drifting-percolating-gem.md` si besoin de la retrouver) —
  prochain sur la liste : **exprimer ses goûts** (aimer/ne pas aimer), réutilisable à chaque
  repas/visite. Puis dans l'ordre : projets de la journée, famille élargie + âge/profession.
  Le blocage de production reste orthographique/moteur mais s'améliore (88% en L16 vs 75%
  en L14/L15) : **ե/է** (3 occurrences), **ն/մ** (2 occurrences), **ե/ւ** (1 occurrence),
  **հ initial parfois chuté** — aucune nouvelle occurrence en L16, à confirmer si la
  tendance se maintient. **ինչքան** (L16) : mot neuf non rappelé une fois, à revoir en
  révision légère (pas encore une confusion récurrente). Le suffixe possessif **-ս** oublié
  une fois sur եղբայրս (L14) est à revérifier. Vocabulaire voyage/aéroport toujours en
  attente (backlog, priorité basse).
- **Vu hors-leçon le 11/07 (question directe de Jérémie, pas d'exercice)** :
  **Ես մի քիչ հայերեն խոսում եմ** [Yes mi kitch hayeren khosum em] = je parle un peu
  arménien. Réutilise **մի քիչ** (L13) + **եմ** ; introduit **հայերեն** (la langue
  arménienne) et **խոսում/խոսել** (parler — même racine que **խոսեք** vu en L15). Sourcé
  via Omniglot + Wiktionary. Pas encore d'évidence QCM/saisie — candidat pour être repris
  dans une prochaine leçon afin d'obtenir une vraie évidence de maîtrise, plutôt que resté
  comme simple exposition.
- **L16 — petits mots de conversation, meilleur score depuis L13 (7/8, 88%, bilan copié
  12/07)** :
  - Deuxième sujet de la liste de 5 validée en session de planification (`/plan` du 10/07).
  - QCM 5/5 — toutes les réactions reconnues, y compris le rappel L14 (Նա ուրախ է).
  - Saisie 2/3 : Իսկապե՞ս et Հրաշալի է corrects du premier coup ; Ինչքան լավ է écrit
    « ....... լավ է » — ինչքան non rappelé (mot neuf pas encore ancré, pas une confusion
    de lettres).
  - 3/3 cartes-flip vues.
  - Deux bugs de frappe détectés et corrigés en session avant livraison (caractère
    cyrillique glissé dans un lien Forvo, signe d'emphase ՛ ajouté par erreur dans le
    dialogue) — voir `learning-records/0016-petits-mots-de-conversation.md`.
- **L15 — survie conversationnelle, grammaire (formules figées) acquise, orthographe à
  retravailler (6/8, 75%, bilan copié 11/07)** :
  - Sujet choisi en tête d'une liste de 5 proposée en session de planification (`/plan`
    du 10/07) — la leçon jugée à plus fort effet de levier avant le voyage.
  - Bug de mise en scène du dialogue corrigé en session (réplique mal attribuée à la
    belle-mère) — voir `learning-records/0015-survie-conversationnelle.md`.
  - QCM 5/5 — les 4 formules toutes reconnues, y compris le rappel de չէ (L07).
  - Saisie 1/3 : **Ի՞նչ է սա** correct ; **ասկանում** pour **հասկանում** (հ initial chuté,
    déjà vu en L04 puis considéré consolidé — réapparu ~2 semaines après) ; **խնդրում ւմ
    կրկնէք** pour **Խնդրում եմ, կրկնեք** (ւ pour ե, nouveau ; է pour ե dans **կրկնէք** —
    élargit ե/է à une confusion générale, pas juste en position initiale).
  - 3/3 cartes-flip vues.
- **L14 — parler des autres, grammaire acquise mais orthographe à retravailler (6/8, 75%,
  bilan copié 10/07)** :
  - Motivé par la demande explicite de Jérémie en début de session : des sujets pour
    discuter avec sa belle-famille au quotidien, pas seulement parler de lui-même.
  - QCM 5/5 — 3e personne (ուտում է, Ի՞նչ է անում, Չի ուտում) et extension du moule
    [adjectif]+է (Քույրս ուրախ է) tous corrects.
  - Saisie 1/3 : **Նա ուտում է** correct ; **ի՞նչ է ամում** pour **ի՞նչ է անում** (ն/մ,
    2e occurrence après L13 → confusion confirmée) ; **էղբայր գնում է** pour **Եղբայրս
    գնում է** (ե/է initiale, 2e occurrence après L12 → confusion confirmée, + suffixe -ս
    oublié, 1 seule occurrence).
  - 3/3 cartes-flip vues.
- **L13 — repas approfondi, maîtrisé après correction (7/7, 100%, bilan copié 06/07)** :
  - ⚠️ **Bug de conception corrigé en session** : la 1re version de la leçon inversait à
    tort l'ordre des mots à l'affirmatif (Հաց **եմ** ուտում au lieu de Հաց ուտում **եմ**),
    par sur-généralisation de la règle de négation de L08. Détecté car la réponse de
    Jérémie («հաց ուտում եմ», la forme standard) avait été marquée fausse à tort. Leçon,
    audio et Anki corrigés et régénérés en cours de session — voir
    `learning-records/0013-repas-approfondi.md` pour le détail.
  - Après correction : **QCM 5/5 cumulé**, **Saisie 3/3**, 3/3 cartes-flip.
  - Nouveau : **մի քիչ** (un peu) et le signe **՞ posé sur un verbe simple** (question
    oui/non sans mot interrogatif, ex. Ուզու՞մ ես) — les deux maîtrisés dès le 2e essai.
  - Point mineur à surveiller : **ն/մ** confondues une fois (խնում pour խմում) au 1er
    essai — possible effet de hâte plutôt qu'une vraie confusion, une seule occurrence.
- **L12 — les jours, réussi (7/8, 88%, bilan copié 05/07)** :
  - Niveau volontairement relevé (saisie en phrases complètes, transfert de la règle de
    position L09 vers un mot totalement nouveau) suite au retour « c'était facile » sur
    L11 — bon calibrage : score solide mais pas parfait.
  - QCM 5/5 — y compris le point culturel sur l'étymologie des jours (numérique
    lundi–jeudi vs emprunts irréguliers Ուրբաթ/Շաբաթ/Կիրակի).
  - Saisie 2/3 — Ի՞նչ օր է այսօր et Ուրբաթ է corrects. Seule faute : **կիրակի գալիս էմ**
    au lieu de **կիրակի գալիս եմ** — confusion **ե/է** sur la lettre initiale du mot եմ
    lui-même (différent de la confusion եմ/է déjà connue sur le choix de personne).
    Une seule occurrence, à reconfirmer avant de le tracker comme récurrent.
  - 3/3 cartes-flip vues.
- **L11 — en visite, maîtrisé (8/8, 100%, bilan copié 05/07)** :
  - QCM 5/5 — y compris le rappel de **Ինչպե՞ս ես** (introduit en L1, jamais testé jusqu'ici,
    enfin évidence-backed) et la distinction registre Ցտեսություն (sûr partout) vs
    Հաջողություն (informel, entre proches).
  - Saisie 3/3 — բարի գալուստ, հյուր, Ցտեսություն tous corrects en production libre dès la
    première exposition. Contraste avec l'écart reco/prod habituel sur du vocabulaire neuf
    (vu en L09) — probablement grâce à la forte réutilisation de structures déjà acquises
    ([adjectif]+եմ de L05, lien direct avec L1).
  - 3/3 cartes-flip vues. Aucune faute — aucun point de vigilance nouveau à surveiller.
- **L10 — révision ciblée production, réussie (11/12, 92%, bilan copié 05/07)** :
  - QCM 6/6 sur les 3 points (attendu, déjà acquis en reconnaissance depuis L09).
  - Saisie 5/6 — net progrès vs 1/3 en L09 : **եմ/է et գալ/գնում désormais fiables en
    production libre** (Անունս Ժերեմի է, Վաղը գալիս եմ, Այսօր չեմ գնում tous corrects).
    **խ/ղ** également corrects (վաղը, տխուր).
  - Seule faute : **այսօր** écrit **այսոր** (sans օ) — point ո/օ, qui n'était PAS dans le
    périmètre ciblé aujourd'hui (déjà noté fragile en L09 sur ce même mot). Pas un échec de
    la méthode — juste un point différent, pas encore travaillé en exercice dédié.
  - 3/3 cartes-flip vues.
- **L09 — le temps, QCM maîtrisé mais production à retravailler (7/9, 78%, bilan copié 05/07)** :
  - QCM 6/6, y compris les deux pièges les plus difficiles (lettre ռ roulée vs ր, et la
    combinaison այսօր + չե՞ս + գալիս mêlant L07+L08+nouveau vocab).
  - Saisie 1/3 : 3 erreurs de production alors que les points sous-jacents étaient corrects en
    QCM — écart reconnaissance/production à surveiller :
    1. **վախը** au lieu de **վաղը** (խ/ղ confondues à l'écrit — nouvelle paire de lettres,
       cf. GLOSSARY.md).
    2. **այսոր** au lieu de **այսօր** (ո/օ — այսօր est un composé qui garde օ en interne).
    3. **չէմ** au lieu de **չեմ**, et **գնում** au lieu de **գալիս** — confirment les deux
       confusions déjà connues (եմ/է ci-dessous, et գալ/գնում du L08) : maîtrisées en
       reconnaissance, pas encore fiables en production libre.
  - 3/3 cartes-flip vues.
- **L08 — verbes de mouvement, maîtrisé (8/8, 100%, bilan copié 04/07)** :
  - Réutilise **ուր** (L06, contraste avec որտեղ) et l'auxiliaire ém/es/é (L01/L07).
  - Piège 1 : **գալ** est monosyllabique → participe **-իս** (գալիս), pas -ում (գալում) —
    **QCM et saisie corrects**.
  - Piège 2 : négation des verbes de mouvement **inverse l'ordre des mots** — auxiliaire négatif
    AVANT le participe (չեմ գնում, pas գնում չեմ) — extension de la règle չեմ/չես/չի de L07 —
    **QCM et saisie (sans pronom) corrects**.
  - Score parfait malgré l'enchaînement L07+L08 le même jour (rythme testé avec succès aujourd'hui).
  - Correction de fond : GLOSSARY.md avait un exemple ուր sans le signe interrogatif ՞ et une
    ponctuation finale ASCII « ; » au lieu du point arménien « ։ » — corrigé (*Ու՞ր ես գնում։*).
- **L07 — négation, maîtrisée (7/8, bilan copié 04/07)** :
  - QCM 5/5, y compris le piège sur l'irrégularité **չի** (3e pers., pas "չէ" comme la logique le
    suggérerait) et le choix de **չէ** pour refuser poliment une offre de thé.
  - Saisie 2/3 : le seul "raté" (phrase complète sans le pronom **Ես**) est en réalité une
    **bonne réponse** — l'arménien étant *pro-drop*, "Հոգնած չեմ" est correct et naturel
    (règle ajoutée plus haut dans ce fichier pour les futures leçons).
  - **Correction de fond** : le glossaire indiquait par erreur "չե [che]" pour la 3e personne
    depuis la L05 — corrigé après vérification croisée (Wikibooks Armenian/Grammar) avant la leçon.
- **Points L06 à reconfirmer plus tard** : ա [a] vs խ [kh], ն [n] vs մ [m] (pas retestés depuis).
- **Decks Anki L03/L04** : en réalité déjà générés (27–28/06) — la mention "en attente" était
  **obsolète**, corrigée aujourd'hui. Tous les decks 0001→0007 sont à jour dans `anki/`.
- **Phase langue** : objectif 50/50 HY toujours visé, à évaluer en L08.
- **⚠️ Échéance voyage** : mi-juillet 2026 — moins de deux semaines restantes.
- Détails outils (Anki/TTS/Piper/deck `Armenian-lessons`) : voir sections plus bas. Lancer Claude depuis `~/Learning/Armenian`.

## Rythme & continuité (préférence Jérémie, 24/06)
- **Une session NEUVE chaque jour** (`cd ~/Learning/Armenian && claude`, puis `/teach`). NE PAS empiler
  avec `--continue` : une session trop longue se fait résumer et perd en efficacité.
- La continuité passe par les **fichiers** : à la FIN de chaque session, mettre à jour le « 📍 OÙ ON EN EST »
  ci-dessus + `learning-records/` + `GLOSSARY.md`. C'est ça qui permet à une session fraîche de reprendre net.
- `--continue` seulement pour reprendre une tâche interrompue **le même jour**.

## Format des sessions
- **10 min/jour max**, structure cible : 2 min révision · 3 min nouveau · 3 min exercices · 2 min dialogue immersif.
- Toujours attendre la réponse de l'apprenant avant d'enchaîner. Ne pas submerger.
- Correction immédiate de TOUTES les erreurs (prononciation, grammaire, vocabulaire) + explication claire.
- Récap en fin de session : appris / erreurs / à revoir.
- Bilan hebdomadaire (mots appris, points de grammaire maîtrisés).

## Langue d'enseignement (à faire évoluer)
- Phase 1 actuelle : ~70 % français / 30 % arménien.
- Passer à 50/50 → 30/70 → 100 % HY quand le niveau le permet (à évaluer par moi).

## ⭐ Préférence : ÉQUILIBRE oral / lecture / écrit + AUDIO (précisé 24/06)
- Veut un **équilibre** des trois (pas tout-oral). Garder QCM/écrit ET ajouter shadowing + lecture à voix haute.
- Pour le **vrai oral** (parler en temps réel) : Claude Code est texte-only, et **ne peut pas transcrire d'audio** (ni Whisper ni Vosk dispo). → Montage : app vocale (Claude mobile / ChatGPT / Gemini) = partenaire de parole ; moi = coach/programme/correction. Pont = Jérémie colle le **transcript texte** ici. Voir `voice-partner-prompt.md`.
- Objectif progressif validé : **conversations full-arménien** après quelques leçons (monter le % HY).
- Audio : génération de fichiers TTS bloquée côté serveur ici. Solution = page `reference/02-audio-ecoute.html` avec bouton 🔊 (synthèse de l'appareil, lang hy-AM) + liens **Forvo** (voix natives). Si pas de voix hy sur l'appareil → s'appuyer sur Forvo, et lui suggérer d'installer un pack voix arménien.
- Chaque nouvelle leçon : ajouter les nouveaux mots à la fiche audio.

## Supports attendus
- Fiches Anki pour chaque nouveau mot (recto = arménien ; verso = traduction | prononciation | exemple).
- Prononciation en transcription latine simple + API si utile. (Pas de génération audio possible ici → recommander YouTube/Forvo.)
- Export Markdown de chaque leçon pour Obsidian (date, thème, vocab, grammaire, exos + corrections).
- Vocab thématique du quotidien familial (nourriture, transports, sentiments, maison, famille).

## Ton
- Encourageant, bienveillant, professionnel, concis. Pas de jargon.

## Préférences personnelles (à compléter au fil des sessions)
- Prénom : **Jérémie** → en arménien : Ժերեմի [Jérémie]. Nationalité : français (ֆրանսիացի).
- Travaille en remote-control avec clavier arménien sur téléphone (écrit en script HY directement).
- Oral vs écrit : à l'aise pour produire en **script arménien** dès le jour 1 (rapide).
- **Profil visuel (identifié 17/07/2026)** : astigmatisme (flou différentiel
  horizontal/vertical, aggravé par petite taille et faible contraste) +
  dyslexie légère. Conséquences pour toutes les futures leçons/fiches :
  privilégier un **contraste fort** (encre noire `--ink` plutôt que le rouge
  thématique `--hy` pour les mots-clés à décoder) et une **taille généreuse**
  avec espacement large ; pour des lettres/formes confondables, **entraîner
  en isolation** (une à la fois, via de vrais mots) avant de les confronter
  entre elles — les présenter groupées d'emblée peut renforcer la confusion.
  Voir `lessons/0017-majuscules-pieges.html` pour un exemple appliqué. Pour
la pratique active (« écrit »), Jérémie a choisi explicitement la **saisie
clavier** (il a un clavier arménien configuré sur son téléphone) plutôt que
le traçage tactile ou une fiche imprimable — chaque bloc-lettre a un flip
puis une saisie du même mot, pas une nouvelle vocabulaire.
- Points de blocage récurrents :
  - `ո` initial = « vo » (écrit ո, dit vo).
  - Choix եմ vs է : un nom/3e personne prend **է** (ex. « Անունս … է »), pas եմ. Reconfirmé en
    saisie L09 (05/07) — maîtrisé en QCM, pas encore fiable en production libre.
  - Tendance à ajouter une lettre parasite (հ devant ուրախ).
  - **խ vs ղ** (nouveau, observé L09 05/07) : deux lettres du fond de la gorge confondues à
    l'écrit en production libre (վաղը écrit վախը). À surveiller comme ա/խ (L06, non retesté).
  - **գալ vs գնում** (venir/partir, L08) : maîtrisé en QCM mais confondu en saisie libre L09
    (05/07) — écart reconnaissance/production à travailler.
  - **ն vs մ** (confirmé récurrent, L13+L14) : խմում→խնում (06/07) puis անում→ամում (10/07,
    sens inverse). Candidat pour un exercice de discrimination dédié.
  - **ե vs է** (confirmé récurrent, L12+L14+L15, confusion élargie) : եմ→էմ (05/07), puis
    եղբայրս→էղբայր (10/07, position initiale), puis **կրկնեք→կրկնէք** (11/07, **pas** en
    position initiale — la confusion touche ե/է en général, pas seulement en tête de mot).
    Distinct du choix եմ/է selon la personne (déjà maîtrisé). Candidat pour un exercice de
    discrimination dédié.
  - **հ initial parfois chuté** : identifié en L04 (28/06, 3 occurrences : համով→ամով,
    Շնորհակալություն→Շնորակալ, Բավական→Բավական) puis considéré consolidé. **Réapparu en
    L15** (11/07) : հասկանում→ասկանում. Reste fragile sous pression de production libre,
    malgré ~2 semaines d'écart.
  - **ե vs ւ** (nouveau, L15 11/07, 1 occurrence) : եմ→ւմ. Possible glissement clavier
    plutôt qu'une vraie confusion de lettres — à confirmer si ça se reproduit.
  - **Majuscules piégeuses en lecture de rue** (identifié 17/07, en Arménie) : confusion par
    groupes, pas par paires isolées — **Groupe 1** Դ/Ղ/Ռ, **Groupe 2** Ձ/Ջ/Ծ/Ճ, **Groupe 3**
    Յ/Ց. Une première hypothèse par paires (Դ↔Տ, Ձ↔Ջ, Ց↔Ո, dans
    `majuscules-a-verifier.md`) était fausse — corrigée en session après comparaison visuelle.
    Travaillé en isolation (cf. profil visuel ci-dessus) dans
    `lessons/0017-majuscules-pieges.html`. Ծ et Ճ n'avaient aucun mot maîtrisé dans
    `GLOSSARY.md` — nouveaux mots utilisés (ծով, ճաշ), vérifiés via Wiktionnaire.
    **Mise à jour 20/07/2026** : Զ (crue isolée) rejoint en fait le **Groupe 2**, qui s'élargit
    aussi à **Չ** (jamais signalée avant) — **Groupe 2 complet : Ձ/Ջ/Ծ/Ճ/Զ/Չ** (6 lettres).
    Jérémie précise que **Զ↔Ջ est la paire la plus dure** de tout le groupe. Չ n'est pas
    encore dans la leçon 0017 (identifiée après coup) — à ajouter, avec un mot réel à sourcer
    (absent de `GLOSSARY.md`, comme Ծ/Ճ l'étaient).

## Convention de prononciation utilisée dans ce cours
- Transcription latine « à la française » entre crochets, ex. [barév].
- L'accent tombe presque toujours sur la **dernière syllabe** en arménien.
- **եմ = [em]**, pas [yem] — le glide [y] appartient au pronom Ես [yes], pas au verbe.
  De même : ես = [es], է = [e]. Confirmé par la femme de Jérémie + fichier source 0001.json.
- **Voyelle épenthétique** : en arménien, un [e/ə] s'insère dans les clusters consonantiques.
  Ex : տխուր se prononce [**te**khour], pas [tokhour]. La lettre ը représente ce son schwa.

## Convention Anki — FORMAT PRINCIPAL : .apkg avec son (fixée 24/06)
- **Source unique par leçon** : `tts/lesson_data/NNNN.json` (champs `hy`, `hy_clean`, `pron`, `fr`, `ex_hy`, `ex_fr`).
- `.venv-tts/bin/python tts/generate.py --lesson NNNN` → produit `anki/NNNN-slug.apkg` : **import unique**,
  son arménien **intégré** (lecture auto), 3 sens (reconnaissance / production / saisie).
- **Moteur du son = Piper local** (modèle `tts/models/hy_AM-gor-medium.onnx`, arménien ORIENTAL `hy_AM`).
  Hors-ligne, sans compte, sans clé. venv dédié Python 3.12 `.venv-tts`. Procédure : `tts/README.md`.
  - ⚠️ Décisions vérifiées le 24/06 : Google/gTTS/Edge n'ont **pas** d'arménien ; Meta MMS n'a que
    l'arménien **occidental** (hyw, mauvais dialecte) ; Azure a l'oriental mais exige un compte
    (le vieux tenant MSN de Jérémie est bloqué). → Piper (`davit312/piper-TTS-Armenian`) = seule
    voix neuronale **orientale** locale et gratuite. Azure reste dispo en option `--engine azure`.
- Modèles de cartes partagés : `tts/anki_models.py` (IDs stables — ne pas changer). Audio en cache dans `audio/`.
- **Paquet racine Anki = `Armenian-lessons`** (constante `DECK_PARENT` dans `generate.py`) : Jérémie a
  renommé ainsi pour éviter la confusion avec un autre deck « Armenian » déjà présent (24/06).
  Structure : `Armenian-lessons::NNNN Titre::{Reconnaissance|Saisie|Écoute}`. Anki identifie les paquets
  par ID, donc les renommages manuels de Jérémie sont préservés au ré-import.
- **3 compétences par défaut = 4 cartes/mot** (demandé 24/06) :
  - **Reconnaissance** (HY→FR) — *lecture*.
  - **Saisie** (FR→HY tapé) — *écriture*.
  - **Écoute** (son seul, AUCUN texte au recto → deviner le sens) — *oral*. **2 cartes** : le mot ET la phrase.
  Ces 3 compétences sont distinctes (pas de redondance). La **Production** (FR→HY de tête) reste
  redondante avec la Saisie → off par défaut, réactivable via `--with-production`.
  - 💡 Volume : 4 cartes/mot, ça monte vite. Si trop par jour, suspendre le sous-paquet
    `Arménien::NNNN …::Écoute` (Parcourir → clic droit → Suspendre).
- **Pour toute nouvelle leçon** : créer le JSON puis relancer `generate.py`. Ne plus produire de TSV à la main.

### Ancien format (fallback lisible, sans son) — TSV
Les `anki/NNNN-*.tsv` restent comme secours lisible / sans clé Azure :
  1. `NNNN-theme.tsv` — reconnaissance (HY → FR), type **Basique**, Verso 3 lignes HTML.
  2. `NNNN-theme-production.tsv` — production (FR → HY), type **Basique**.
  3. `NNNN-theme-saisie.tsv` — saisie (FR → HY tapé), type **Basique (saisie de la réponse)**, Verso = arménien pur.
  Import TSV : Tabulation, « Autoriser le HTML », champs Recto/Verso. Jérémie aime le mode saisie (clavier arménien).
