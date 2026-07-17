/* ============================================================
   Composant réutilisable : auto-correction & cartes-éclair
   Utilisé par les leçons pour la pratique en rappel actif.
   - .flip   : carte cliquable (recto -> verso)
   - .quiz   : QCM avec correction immédiate
   ============================================================ */

document.addEventListener('click', function (e) {
  /* ---- Cartes à retourner (rappel actif) ---- */
  const card = e.target.closest('.flip');
  if (card) { card.classList.toggle('revealed'); return; }

  /* ---- QCM : clic sur une réponse ---- */
  const opt = e.target.closest('.quiz .opt');
  if (opt) {
    const q = opt.closest('.quiz');
    if (q.classList.contains('answered')) return;
    q.classList.add('answered');
    const correct = opt.dataset.correct === '1';
    opt.classList.add(correct ? 'right' : 'wrong');
    if (!correct) {
      const good = q.querySelector('.opt[data-correct="1"]');
      if (good) good.classList.add('right');
    }
    const fb = q.querySelector('.feedback');
    if (fb) { fb.classList.add('show'); fb.classList.add(correct ? 'ok' : 'no'); }
  }
});

/* Styles injectés pour les composants (gardés avec le JS pour la portabilité) */
(function() { const css = `
.flip {
  cursor: pointer;
  border: 1.5px solid var(--rule); border-radius: 12px;
  padding: 1.1rem 1.3rem 0.9rem; margin: 1.2rem 0;
  background: #fff;
  box-shadow: 0 4px 14px rgba(0,0,0,.10);
  transition: box-shadow .18s, transform .18s;
  overflow: hidden;
}
.flip:hover { box-shadow: 0 7px 20px rgba(0,0,0,.15); transform: translateY(-2px); }

.flip .prompt-hint {
  display: block;
  background: var(--accent-soft); color: var(--accent);
  font-family: ui-sans-serif, system-ui, sans-serif;
  font-size: 0.7rem; font-weight: 700;
  text-transform: uppercase; letter-spacing: .1em;
  margin: -1.1rem -1.3rem 0.9rem;
  padding: 0.45rem 1.3rem;
  border-bottom: 1px solid #cde;
}

.flip::after {
  content: '▼  appuyer pour révéler';
  display: block; text-align: center;
  font-family: ui-sans-serif, system-ui, sans-serif;
  font-size: 0.65rem; text-transform: uppercase; letter-spacing: .08em;
  color: var(--muted); margin-top: 0.8rem;
  padding-top: 0.5rem; border-top: 1px dashed var(--rule);
}
.flip.revealed::after { display: none; }

.flip .back {
  display: none;
  margin-top: 0.8rem; padding: 0.75rem 1rem;
  border-radius: 8px;
  background: var(--hy-soft); border-left: 3px solid var(--hy);
  font-size: 1.1rem;
}
.flip.revealed .back { display: block; }
.flip.revealed { border-color: var(--hy-soft); }

.quiz {
  border: 1.5px solid var(--rule); border-radius: 12px;
  padding: 1.3rem 1.5rem; margin: 1.3rem 0; background: #fff;
  box-shadow: 0 2px 8px rgba(0,0,0,.06);
  counter-reset: opt-ctr;
}
.quiz .q { font-weight: 700; margin-bottom: 1rem; font-size: 1rem; line-height: 1.4; }
.quiz .opt {
  counter-increment: opt-ctr;
  display: flex; align-items: center; gap: 0.85rem;
  width: 100%; text-align: left; padding: 0.7rem 1rem; margin: 0.45rem 0;
  border: 1.5px solid var(--rule); border-radius: 10px;
  background: var(--paper); cursor: pointer;
  font: inherit; font-size: 0.95rem; transition: .14s;
}
.quiz .opt::before {
  content: counter(opt-ctr, upper-alpha);
  flex-shrink: 0;
  width: 1.7rem; height: 1.7rem; border-radius: 50%;
  border: 1.5px solid var(--rule);
  display: flex; align-items: center; justify-content: center;
  font-size: 0.72rem; font-family: ui-sans-serif, system-ui, sans-serif;
  font-weight: 700; color: var(--muted); transition: .14s;
}
.quiz .opt:hover:not([disabled]) { border-color: var(--accent); background: var(--accent-soft); }
.quiz .opt:hover:not([disabled])::before { border-color: var(--accent); color: var(--accent); }
.quiz.answered .opt { cursor: default; }
.quiz .opt.right { background: #e7f6ec; border-color: var(--good); color: var(--good); font-weight: 600; }
.quiz .opt.right::before { background: var(--good); border-color: var(--good); color: #fff; content: '✓'; }
.quiz .opt.wrong { background: #fbeaea; border-color: #c44; color: #999; text-decoration: line-through; }
.quiz .opt.wrong::before { background: #c44; border-color: #c44; color: #fff; content: '✗'; }
.quiz .feedback { display: none; margin-top: 1rem; padding: 0.75rem 1rem; border-radius: 9px; font-size: 0.9rem; }
.quiz .feedback.show { display: block; }
.quiz .feedback.ok { background: #e7f6ec; color: var(--good); border-left: 3px solid var(--good); }
.quiz .feedback.no { background: #fff8e6; color: #7a5200; border-left: 3px solid var(--warn); }
`;
const s = document.createElement('style');
s.textContent = css;
document.head.appendChild(s); })();
