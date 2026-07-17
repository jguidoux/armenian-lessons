/* ============================================================
   Composant audio réutilisable
   - Bouton 🔊 avec data-src="path/file.mp3" : lit le fichier
     MP3 local (Piper TTS) — prioritaire, meilleure qualité.
   - Bouton 🔊 avec data-hy="..." seulement : fallback sur la
     synthèse vocale du navigateur (lang hy-AM).
   - Si aucune voix arménienne n'est dispo, renvoie vers Forvo.
   Usage avec MP3 : <button class="sound" data-src="../audio/hy_0001_abc.mp3" data-hy="Բարևւ">🔊</button>
   Usage fallback  : <button class="sound" data-hy="Բարևւ">🔊</button>
   ============================================================ */

let HY_VOICE = null;
function pickArmenianVoice() {
  const voices = speechSynthesis.getVoices() || [];
  HY_VOICE = voices.find(v => v.lang && v.lang.toLowerCase().startsWith('hy')) || null;
}
if ('speechSynthesis' in window) {
  pickArmenianVoice();
  speechSynthesis.onvoiceschanged = pickArmenianVoice;
}

let _currentAudio = null;

function _speakTTS(btn) {
  const text = btn.dataset.hy;
  if (!text || !('speechSynthesis' in window)) return;
  speechSynthesis.cancel();
  const u = new SpeechSynthesisUtterance(text);
  u.lang = 'hy-AM';
  if (HY_VOICE) u.voice = HY_VOICE;
  u.rate = 0.82;
  u.pitch = 1.0;
  btn.classList.add('playing');
  u.onend = () => btn.classList.remove('playing');
  u.onerror = () => btn.classList.remove('playing');
  speechSynthesis.speak(u);
  if (!HY_VOICE) {
    const warn = document.getElementById('no-voice-warning');
    if (warn) warn.style.display = 'block';
  }
}

document.addEventListener('click', function (e) {
  const btn = e.target.closest('.sound');
  if (!btn) return;

  // Priorité 1 : fichier MP3 local (Piper TTS)
  if (btn.dataset.src) {
    if (_currentAudio) { _currentAudio.pause(); _currentAudio.currentTime = 0; }
    _currentAudio = new Audio(btn.dataset.src);
    btn.classList.add('playing');
    _currentAudio.onended = () => btn.classList.remove('playing');
    _currentAudio.onerror = () => {
      btn.classList.remove('playing');
      _speakTTS(btn);   // fallback TTS si le fichier local échoue (ex. file://)
    };
    _currentAudio.play().catch(() => {});
    return;
  }

  // Priorité 2 : synthèse vocale du navigateur
  _speakTTS(btn);
});


(function() { const css = `
.sound { cursor: pointer; border: 1px solid var(--rule); background: #fff; border-radius: 6px;
  font-size: 1rem; line-height: 1; padding: 0.3rem 0.5rem; transition: .12s; }
.sound:hover { border-color: var(--accent); background: var(--accent-soft); }
.sound.playing { background: var(--accent); border-color: var(--accent); }
.sound-row { display: flex; align-items: center; gap: 0.6rem; flex-wrap: wrap;
  padding: 0.55rem 0; border-bottom: 1px solid var(--rule); }
.sound-row .hy { font-size: 1.3rem; min-width: 9rem; }
.sound-row .pron { min-width: 9rem; }
.sound-row .fr { color: var(--muted); flex: 1; }
.sound-row a.forvo { font-size: 0.78rem; }
`; const s = document.createElement('style'); s.textContent = css; document.head.appendChild(s); })();
