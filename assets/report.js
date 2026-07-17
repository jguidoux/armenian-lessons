/* ============================================================
   Composant réutilisable : bilan copiable
   Ajoute automatiquement, avant le pied de page (.footer), un bouton
   qui compile les réponses déjà données (.quiz, .saisie, .flip)
   en texte brut et le copie dans le presse-papier — pour que
   l'apprenant puisse le coller directement au professeur (Claude).
   ============================================================ */

(function () {

  function lessonMeta() {
    const kicker = document.querySelector('.kicker');
    const h1 = document.querySelector('h1');
    const m = kicker && kicker.textContent.match(/Leçon\s+(\d+)/);
    return {
      num: m ? m[1] : '????',
      title: h1 ? h1.textContent.trim() : document.title
    };
  }

  function buildReport() {
    const { num, title } = lessonMeta();
    const lines = [`=== Bilan Leçon ${num} — ${title} ===`, ''];
    let correct = 0, total = 0;

    const quizzes = Array.from(document.querySelectorAll('.quiz'));
    if (quizzes.length) {
      lines.push('[QCM]');
      quizzes.forEach((q, i) => {
        const question = (q.querySelector('.q') || {}).textContent || '';
        if (!q.classList.contains('answered')) {
          lines.push(`${i + 1}. ${question.trim()} → (non répondu)`);
          return;
        }
        total++;
        const chosen = q.querySelector('.opt.right, .opt.wrong');
        const isRight = chosen && chosen.classList.contains('right');
        const correctOpt = q.querySelector('.opt[data-correct="1"]');
        if (isRight) {
          correct++;
          lines.push(`${i + 1}. ${question.trim()} → ✓ ${chosen.textContent.trim()}`);
        } else {
          const chosenTxt = chosen ? chosen.textContent.trim() : '?';
          const goodTxt = correctOpt ? correctOpt.textContent.trim() : '?';
          lines.push(`${i + 1}. ${question.trim()} → ✗ a répondu « ${chosenTxt} », correct : « ${goodTxt} »`);
        }
      });
      lines.push('');
    }

    const saisies = Array.from(document.querySelectorAll('.saisie'));
    if (saisies.length) {
      lines.push('[Saisie]');
      saisies.forEach((s, i) => {
        const question = (s.querySelector('.q') || {}).textContent || '';
        if (!s.classList.contains('answered')) {
          lines.push(`${i + 1}. ${question.trim()} → (non répondu)`);
          return;
        }
        total++;
        const input = s.querySelector('input');
        const answerEl = s.querySelector('.saisie-answer');
        const typed = (input && input.value.trim()) || '';
        const isRight = s.classList.contains('ok');
        if (isRight) {
          correct++;
          lines.push(`${i + 1}. ${question.trim()} → ✓ a écrit « ${typed} »`);
        } else {
          const expected = answerEl ? answerEl.textContent.trim() : '?';
          lines.push(`${i + 1}. ${question.trim()} → ✗ a écrit « ${typed} », correct : « ${expected} »`);
        }
      });
      lines.push('');
    }

    const flips = Array.from(document.querySelectorAll('.flip'));
    if (flips.length) {
      const revealed = flips.filter(f => f.classList.contains('revealed')).length;
      lines.push(`[Cartes vues] ${revealed}/${flips.length}`);
      lines.push('');
    }

    if (total > 0) {
      const pct = Math.round((correct / total) * 100);
      lines.push(`Score global : ${correct}/${total} (${pct}%)`);
    } else {
      lines.push('(aucun exercice à correction automatique n\'a encore été fait)');
    }

    return lines.join('\n');
  }

  function copyReport(btn) {
    const text = buildReport();
    const markCopied = () => {
      const original = '📋 Copier mon bilan';
      btn.textContent = '✓ Copié — colle-le au professeur';
      btn.classList.add('copied');
      hideFallback();
      setTimeout(() => { btn.textContent = original; btn.classList.remove('copied'); }, 2500);
    };
    // navigator.clipboard n'existe que dans un contexte "sécurisé" (https, ou localhost
    // depuis l'ordi lui-même). Depuis un téléphone qui appelle l'IP du serveur, l'API est
    // absente ou refuse silencieusement — on ne peut PAS se fier à une promesse résolue
    // pour prouver que la copie a vraiment eu lieu.
    if (window.isSecureContext && navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(text).then(markCopied).catch(() => manualCopy(btn, text));
    } else {
      manualCopy(btn, text);
    }
  }

  function ensureFallbackBox() {
    let box = document.querySelector('.report-fallback');
    if (box) return box;
    const wrap = document.querySelector('.report-wrap');
    box = document.createElement('div');
    box.className = 'report-fallback';
    const hint = document.createElement('p');
    hint.className = 'report-hint';
    const ta = document.createElement('textarea');
    ta.readOnly = true;
    box.appendChild(hint);
    box.appendChild(ta);
    wrap.appendChild(box);
    return box;
  }

  function hideFallback() {
    const box = document.querySelector('.report-fallback');
    if (box) box.classList.remove('show');
  }

  function manualCopy(btn, text) {
    const box = ensureFallbackBox();
    const ta = box.querySelector('textarea');
    ta.value = text;
    box.classList.add('show');
    ta.focus();
    ta.select();
    ta.setSelectionRange(0, text.length);
    // Tenter execCommand maintenant que le champ est visible et sélectionné —
    // marche parfois là où l'API Clipboard moderne est bloquée. On VÉRIFIE la
    // valeur de retour au lieu de supposer que ça a marché.
    let worked = false;
    try { worked = document.execCommand('copy'); } catch (e) { worked = false; }
    const hint = box.querySelector('.report-hint');
    if (worked) {
      hint.textContent = '✓ Copié ! (si le collage ne marche pas, le texte reste sélectionné ci-dessous)';
    } else {
      hint.textContent = '👆 Sélectionne le texte ci-dessous et copie-le (appui long sur mobile, ou Ctrl/Cmd+C)';
    }
  }

  function injectButton() {
    const footer = document.querySelector('.footer');
    if (!footer) return;
    const wrap = document.createElement('div');
    wrap.className = 'report-wrap';
    const btn = document.createElement('button');
    btn.type = 'button';
    btn.className = 'report-btn';
    btn.textContent = '📋 Copier mon bilan';
    btn.addEventListener('click', () => copyReport(btn));
    wrap.appendChild(btn);
    footer.parentNode.insertBefore(wrap, footer);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', injectButton);
  } else {
    injectButton();
  }

  (function () {
    const css = `
.report-wrap { text-align: center; margin: 2em 0 0.5em; }
.report-btn {
  padding: 0.75rem 1.3rem;
  border: 1.5px solid var(--accent); border-radius: 10px;
  background: var(--accent-soft); color: var(--accent);
  font: inherit; font-size: 0.95rem; font-weight: 600; cursor: pointer;
  transition: .14s;
}
.report-btn:hover { background: var(--accent); color: #fff; }
.report-btn.copied { background: var(--good); border-color: var(--good); color: #fff; }
.report-fallback { display: none; max-width: 640px; margin: 1em auto 0; text-align: left; }
.report-fallback.show { display: block; }
.report-hint {
  font-size: 0.85rem; color: var(--muted); margin: 0 0 0.5em;
  font-family: ui-sans-serif, system-ui, sans-serif;
}
.report-fallback textarea {
  width: 100%; min-height: 220px; box-sizing: border-box;
  padding: 0.8rem 1rem; border: 1.5px solid var(--accent); border-radius: 10px;
  font-family: ui-monospace, "SF Mono", Menlo, monospace;
  font-size: 0.85rem; line-height: 1.5;
  background: var(--paper); color: var(--ink);
}
`;
    const s = document.createElement('style'); s.textContent = css; document.head.appendChild(s);
  })();

})();
