const { site, tests } = JSON.parse(document.getElementById('data').textContent);
const app = document.getElementById('app');
const esc = (s) => String(s ?? '').replace(/[&<>"]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
const STATUS = { ok: 'работает', partial: 'частично', broken: 'не работает', pending: 'ждёт прогона' };
const fmtTok = (t) => (t >= 1e6 ? (t / 1e6).toFixed(2) + 'M' : Math.round(t / 1e3) + 'k');
const hue = (w) => ['#d4ff3a', '#ff7a3a', '#3ad0ff', '#c77dff', '#5be08a', '#ff5d9e', '#ffd23a', '#3a7bff', '#ff4747', '#7affd8'][(w || 0) % 10];

const waves = [...new Set(tests.map((t) => t.wave).filter(Boolean))].sort((a, b) => a - b);
let filter = (() => { try { return localStorage.getItem('gal-filter') || 'all'; } catch { return 'all'; } })();

const s = site.summary;
app.innerHTML = `
<header class="hero">
  <div class="kicker">Бенчмарк · ${s.total} тестов · v1 one-shot / v2 доработка</div>
  <h1>${esc(site.config.site_title).replace('—', '— <em>')}</em></h1>
  <p>${esc(site.config.site_subtitle)}</p>
  <div class="stats">
    <span class="stat">прогнано <b>${s.done}</b> / ${s.total}</span>
    <span class="stat">работает <b>${s.ok}</b></span>
    <span class="stat">токены <b>${s.tokens ? fmtTok(s.tokens) : '—'}</b></span>
    <span class="stat">≈ <b>$${s.usd.toFixed(2)}</b></span>
    <span class="stat">время <b>${Math.round(s.minutes)} мин</b></span>
    ${site.config.model ? `<span class="stat">модель <b>${esc(site.config.model)}</b> · effort <b>${esc(site.config.effort)}</b></span>` : `<span class="stat">effort <b>${esc(site.config.effort)}</b></span>`}
  </div>
  <div class="note">Стоимость — оценка (API-эквивалент) по общему числу токенов исполнителя, не реальное списание.</div>
</header>
<nav class="filters"><div class="in" id="chips"></div></nav>
<section class="grid" id="grid"></section>
<footer>Каждая карточка → страница теста: промпт дословно, расход, что сломалось в v1 и что исправлено в v2, живой просмотр.
<br><a href="${esc(site.config.repo_url)}">Исходники на GitHub</a> · <a href="tests/index.json">tests/index.json</a></footer>`;

function chips() {
  const list = [['all', 'Все', tests.length], ['done', 'Готовые', tests.filter((t) => t.status !== 'pending').length]]
    .concat(waves.map((w) => [String(w), `${w}. ${site.waves[w] || ''}`.replace(/\s*\(адаптация.*?\)/, ' ✦'), tests.filter((t) => t.wave === w).length]));
  document.getElementById('chips').innerHTML = list
    .map(([k, label, c]) => `<button class="chip ${filter === k ? 'on' : ''}" data-k="${k}">${esc(label)}<span class="c">${c}</span></button>`)
    .join('');
}

function card(t) {
  const st = `s-${t.status}`;
  const thumb = t.shot
    ? `<img loading="lazy" src="tests/${t.slug}/${t.shot}" alt="">`
    : t.kind === 'text'
      ? `<div class="ph text">${esc(t.source).slice(0, 220)}</div>`
      : `<div class="ph" style="--h:${hue(t.wave)}">${String(t.n).padStart(2, '0')}</div>`;
  return `<a class="card" href="tests/${t.slug}/">
    <div class="thumb">${thumb}<span class="badge ${st}">${STATUS[t.status]}</span><span class="num">#${String(t.n).padStart(2, '0')}</span></div>
    <div class="body"><h3>${esc(t.title)}</h3><div class="g">${esc(t.genre)} · ${esc(t.fmt)}</div>
    <div class="meta-row">${t.usd != null ? `<span>≈ <b>$${t.usd.toFixed(2)}</b></span>` : ''}${t.tokens ? `<span><b>${fmtTok(t.tokens)}</b> ток.</span>` : ''}${t.minutes ? `<span><b>${Math.round(t.minutes)}</b> мин</span>` : ''}${!t.tokens ? '<span>волна ' + (t.wave ?? '—') + '</span>' : ''}</div></div></a>`;
}

function render() {
  chips();
  const list = tests.filter((t) => filter === 'all' || (filter === 'done' ? t.status !== 'pending' : String(t.wave) === filter));
  document.getElementById('grid').innerHTML = list.length ? list.map(card).join('') : '<div class="empty">Пока пусто — эта волна ещё не прогнана.</div>';
}
document.getElementById('chips').addEventListener('click', (e) => {
  const b = e.target.closest('.chip'); if (!b) return;
  filter = b.dataset.k; try { localStorage.setItem('gal-filter', filter); } catch {}
  render();
});
render();
