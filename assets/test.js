import { marked } from '../vendor/marked/marked.esm.js';

const D = JSON.parse(document.getElementById('data').textContent);
const t = D.test;
const app = document.getElementById('app');
const esc = (s) => String(s ?? '').replace(/[&<>"]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
const STATUS = { ok: 'работает', partial: 'частично', broken: 'не работает', pending: 'ждёт прогона' };
const fmtTok = (n) => (n >= 1e6 ? (n / 1e6).toFixed(2) + ' M' : Math.round(n / 1e3) + ' k');
const versions = ['v1', 'v2'].filter((v) => t.entries[v] || t.shots[v]);
let cur = (() => { const h = location.hash.slice(1); return versions.includes(h) ? h : versions.includes('v2') ? 'v2' : versions[0]; })();
let tab = 'prompt';

const kv = [
  ['статус', `<span class="badge s-${t.status}" style="position:static;display:inline-flex;background:none;padding:0">${STATUS[t.status]}</span>`],
  ['формат', esc(t.fmt)],
  ['волна', t.wave ? `${t.wave} · ${esc(t.wave_name)}` : '—'],
  t.model ? ['модель', esc(t.model)] : null,
  ['effort', esc(t.effort || '—')],
  ['токены', t.tokens ? fmtTok(t.tokens) : '—'],
  ['≈ цена', t.usd != null ? `$${t.usd.toFixed(2)} <span style="color:var(--faint)">(оценка)</span>` : '—'],
  ['время', t.minutes ? `${t.minutes} мин` : '—'],
  ['дата', esc(t.date || '—')],
].filter(Boolean);

app.innerHTML = `
<div class="top">
  <a class="home" href="../../">← <span class="lbl">Все тесты</span></a>
  <span class="sp"></span>
  ${D.prev ? `<a href="../${D.prev}/" title="${esc(D.prev_title)}">‹ <span class="lbl">${esc(D.prev_title)}</span></a>` : ''}
  ${D.next ? `<a href="../${D.next}/" title="${esc(D.next_title)}"><span class="lbl">${esc(D.next_title)}</span> ›</a>` : ''}
</div>
<div class="layout">
  <aside class="info">
    <div class="n">ТЕСТ #${String(t.n).padStart(2, '0')}</div>
    <h1>${esc(t.title)}</h1>
    <div class="genre">${esc(t.genre)}</div>
    <dl class="kv">${kv.map(([k, v]) => `<dt>${k}</dt><dd>${v}</dd>`).join('')}</dl>
    ${t.notes ? `<div class="callout" style="--s:var(--acc)"><b>Итог</b>${esc(t.notes)}</div>` : ''}
    ${t.v1_issues ? `<div class="callout" style="--s:var(--broken)"><b>Что было не так в v1</b>${esc(t.v1_issues)}</div>` : ''}
    ${t.v2_changes ? `<div class="callout" style="--s:var(--ok)"><b>Что сделано в v2</b>${esc(t.v2_changes)}</div>` : ''}
    <div class="tabs">
      <button class="btn" data-tab="prompt">Промпт</button>
      ${D.readme_md ? '<button class="btn" data-tab="readme">README</button>' : ''}
      ${t.files.length ? '<button class="btn" data-tab="files">Файлы</button>' : ''}
    </div>
    <div id="tab" class="md"></div>
  </aside>
  <main class="view">
    <div class="vbar">
      <div class="seg">${['v1', 'v2'].map((v) => `<button data-v="${v}" ${versions.includes(v) ? '' : 'disabled'}>${v === 'v1' ? 'v1 · one-shot' : 'v2 · доработка'}</button>`).join('')}</div>
      <span class="sp"></span>
      <button class="btn" id="shotbtn">Скриншот</button>
      <a class="btn" id="openbtn" target="_blank" rel="noopener">Открыть отдельно ↗</a>
    </div>
    <div class="stage" id="stage"></div>
  </main>
</div>`;

const stage = document.getElementById('stage');
let showShot = false;

function renderStage() {
  document.querySelectorAll('.seg button').forEach((b) => b.classList.toggle('on', b.dataset.v === cur));
  const entry = t.entries[cur];
  const shot = t.shots[cur];
  const open = document.getElementById('openbtn');
  const sb = document.getElementById('shotbtn');
  sb.style.display = shot && entry ? '' : 'none';
  sb.textContent = showShot ? 'Живой просмотр' : 'Скриншот';
  open.style.display = entry ? '' : 'none';
  if (entry) open.href = entry;
  if (!entry && !shot) {
    stage.innerHTML = `<div class="pending-box"><div><div class="big">${String(t.n).padStart(2, '0')}</div><p>${t.status === 'pending' ? 'Тест ещё не прогнан.' : 'Нет просматриваемого результата.'}</p></div></div>`;
    return;
  }
  if (showShot || !entry) { stage.innerHTML = `<img class="full" src="${shot}" alt="скриншот ${cur}">`; return; }
  const ext = entry.split('.').pop().toLowerCase();
  if (['mp4', 'webm', 'mov'].includes(ext)) stage.innerHTML = `<video src="${entry}" controls autoplay loop muted playsinline></video>`;
  else if (['png', 'jpg', 'jpeg', 'gif', 'webp'].includes(ext)) stage.innerHTML = `<img class="full" src="${entry}" alt="">`;
  else if (['md', 'txt'].includes(ext)) {
    stage.innerHTML = '<div class="mdview"><div class="md">Загрузка…</div></div>';
    fetch(entry).then((r) => r.text()).then((txt) => { stage.querySelector('.md').innerHTML = ext === 'md' ? marked.parse(txt) : `<pre>${esc(txt)}</pre>`; })
      .catch(() => { stage.querySelector('.md').textContent = 'Не удалось загрузить файл.'; });
  } else if (['py', 'pov', 'tsx', 'ts', 'js', 'json'].includes(ext)) {
    stage.innerHTML = '<div class="mdview"><div class="md"><pre><code>…</code></pre></div></div>';
    fetch(entry).then((r) => r.text()).then((txt) => { stage.querySelector('code').textContent = txt; });
  } else stage.innerHTML = `<iframe src="${entry}" allow="autoplay; microphone; fullscreen; clipboard-write"></iframe>`;
}

function renderTab() {
  document.querySelectorAll('.tabs .btn').forEach((b) => (b.style.color = b.dataset.tab === tab ? 'var(--fg)' : ''));
  const el = document.getElementById('tab');
  if (tab === 'prompt') {
    const md = D.prompt_md.replace(/^- \*\*Волна:\*\*.*$/m, '');
    const i = md.search(/^## /m);
    const head = i > 0 ? md.slice(0, i).replace(/^# .*$/m, '').trim() : '';
    const body = i > 0 ? md.slice(i) : md;
    el.innerHTML = marked.parse(body) + (head ? '<h2>О тесте</h2>' + marked.parse(head) : '');
  }
  else if (tab === 'readme') el.innerHTML = marked.parse(D.readme_md);
  else el.innerHTML = `<div class="files">${t.files.map((f) => `<a href="${encodeURI(f)}" target="_blank">${esc(f)}</a>`).join('<br>')}</div>`;
}

document.querySelector('.seg').addEventListener('click', (e) => {
  const b = e.target.closest('button'); if (!b || b.disabled) return;
  cur = b.dataset.v; showShot = false; history.replaceState(null, '', '#' + cur); renderStage();
});
document.getElementById('shotbtn').addEventListener('click', () => { showShot = !showShot; renderStage(); });
document.querySelector('.tabs').addEventListener('click', (e) => { const b = e.target.closest('[data-tab]'); if (b) { tab = b.dataset.tab; renderTab(); } });
document.addEventListener('keydown', (e) => {
  if (e.target.closest('input,textarea')) return;
  if (e.key === 'ArrowLeft' && D.prev) location.href = `../${D.prev}/`;
  if (e.key === 'ArrowRight' && D.next) location.href = `../${D.next}/`;
});
renderStage();
renderTab();
