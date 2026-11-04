// Проверка страницы в headless Chromium: ошибки консоли, исключения, 404, FPS, скриншот.
// Запуск: NODE_PATH=$(npm root -g) node tools/check.mjs <url> <screenshot.png> [--wait 4000] [--click] [--mobile] [--full]
import { createRequire } from 'module';
const require = createRequire(import.meta.url);
const { chromium } = require('playwright');

const args = process.argv.slice(2);
const url = args[0], out = args[1];
if (!url || !out) { console.log('usage: check.mjs <url> <out.png> [--wait ms] [--click] [--mobile] [--full]'); process.exit(2); }
const opt = (k) => args.includes(k);
const wi = args.indexOf('--wait');
const wait = wi >= 0 ? Number(args[wi + 1]) : 4000;
const mobile = opt('--mobile');

const browser = await chromium.launch({
  args: ['--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist', '--autoplay-policy=no-user-gesture-required'],
});
const ctx = await browser.newContext({
  viewport: mobile ? { width: 390, height: 844 } : { width: 1280, height: 720 },
  deviceScaleFactor: 1, isMobile: mobile, hasTouch: mobile,
});
const page = await ctx.newPage();
const errors = [], warnings = [], failed = [];
page.on('console', (m) => {
  if (m.type() === 'error') errors.push(m.text().slice(0, 300));
  else if (m.type() === 'warning') warnings.push(m.text().slice(0, 200));
});
page.on('pageerror', (e) => errors.push('EXCEPTION: ' + String(e.message).slice(0, 300)));
page.on('requestfailed', (r) => failed.push(`${r.failure()?.errorText} ${r.url()}`));
page.on('response', (r) => { if (r.status() >= 400) failed.push(`${r.status()} ${r.url()}`); });

await page.addInitScript(() => {
  window.__frames = 0;
  const raf = window.requestAnimationFrame.bind(window);
  (function tick() { window.__frames++; raf(tick); })();
});

const t0 = Date.now();
try { await page.goto(url, { waitUntil: 'load', timeout: 30000 }); }
catch (e) { errors.push('NAVIGATION: ' + e.message); }
if (opt('--click')) {
  await page.waitForTimeout(800);
  const vp = page.viewportSize();
  await page.mouse.click(vp.width / 2, vp.height / 2).catch(() => {});
}
const f0 = await page.evaluate(() => window.__frames).catch(() => 0);
await page.waitForTimeout(wait);
const f1 = await page.evaluate(() => window.__frames).catch(() => 0);
await page.screenshot({ path: out, fullPage: opt('--full') });
const fps = ((f1 - f0) / (wait / 1000)).toFixed(1);

console.log(JSON.stringify({
  url, screenshot: out, load_ms: Date.now() - t0 - wait, fps_in_sandbox: Number(fps),
  console_errors: errors, failed_requests: [...new Set(failed)], warnings: warnings.slice(0, 5),
}, null, 1));
await browser.close();
