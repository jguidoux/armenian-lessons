/* ============================================================
   Composant réutilisable : exercice de saisie libre
   - .saisie : bloc exercice avec champ texte arménien
   - Comparaison insensible à la casse (toLowerCase) côté JS
   - Enter ou bouton → pour valider
   ============================================================ */

(function () {

  document.addEventListener('keydown', function (e) {
    if (e.key !== 'Enter') return;
    const input = e.target.closest && e.target.closest('.saisie input');
    if (input) { e.preventDefault(); check(input.closest('.saisie')); }
  });

  document.addEventListener('click', function (e) {
    const btn = e.target.closest('.saisie .saisie-submit');
    if (btn) check(btn.closest('.saisie'));
  });

  function check(block) {
    if (block.classList.contains('answered')) return;
    const input = block.querySelector('input');
    const answerEl = block.querySelector('.saisie-answer');
    const typed = input.value.trim().toLowerCase();
    const expected = (answerEl.dataset.answer || '').toLowerCase();
    const correct = typed === expected;
    block.classList.add('answered');
    block.classList.add(correct ? 'ok' : 'no');
    input.disabled = true;
    const btn = block.querySelector('.saisie-submit');
    if (btn) btn.disabled = true;
    const fb = block.querySelector('.feedback');
    if (fb) {
      fb.classList.add('show');
      fb.textContent = correct
        ? '✓ Correct !'
        : '✗ La réponse est : ' + answerEl.textContent.trim();
    }
  }

  (function () {
    const css = `
.saisie {
  border: 1.5px solid var(--rule); border-radius: 12px;
  padding: 1.3rem 1.5rem; margin: 1.3rem 0; background: #fff;
  box-shadow: 0 2px 8px rgba(0,0,0,.06);
}
.saisie .q { font-weight: 700; margin: 0 0 1rem; font-size: 1rem; line-height: 1.4; }
.saisie-row { display: flex; gap: 0.6rem; align-items: center; }
.saisie input {
  flex: 1; padding: 0.65rem 0.9rem;
  border: 1.5px solid var(--rule); border-radius: 9px;
  font: inherit; font-size: 1.05rem;
  font-family: "Noto Serif Armenian", "Sylfaen", "DejaVu Serif", serif;
  background: var(--paper); color: var(--ink);
  transition: border-color .14s;
}
.saisie input:focus { outline: none; border-color: var(--accent); }
.saisie input:disabled { opacity: 0.7; }
.saisie .saisie-submit {
  padding: 0.65rem 1.1rem;
  border: 1.5px solid var(--accent); border-radius: 9px;
  background: var(--accent); color: #fff;
  font: inherit; font-size: 1rem; cursor: pointer; transition: .14s;
}
.saisie .saisie-submit:hover:not(:disabled) { filter: brightness(0.88); }
.saisie .saisie-submit:disabled { opacity: 0.45; cursor: default; }
.saisie-answer { display: none; }
.saisie .feedback {
  display: none; margin-top: 0.9rem;
  padding: 0.65rem 1rem; border-radius: 9px; font-size: 0.95rem;
}
.saisie .feedback.show { display: block; }
.saisie.ok input  { border-color: var(--good); }
.saisie.no input  { border-color: #c44; }
.saisie.ok .feedback { background: #e7f6ec; color: var(--good); border-left: 3px solid var(--good); }
.saisie.no .feedback { background: #fff8e6; color: #7a5200; border-left: 3px solid var(--warn); }
`;
    const s = document.createElement('style'); s.textContent = css; document.head.appendChild(s);
  })();

})();
