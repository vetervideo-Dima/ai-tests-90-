# vendor/

Локальные копии библиотек (из npm). Страницы тестов подключают их по относительному пути — без CDN.

| Библиотека | Версия | Путь |
|---|---|---|
| three.js | 0.187.0 | `vendor/three/build/three.module.js`, аддоны: `vendor/three/examples/jsm/` |
| gsap (+ все плагины) | 3.15.1 | `vendor/gsap/gsap.min.js`, `vendor/gsap/ScrollTrigger.min.js`, … (UMD, обычный `<script>`) |
| p5.js | 1.11.13 | `vendor/p5/p5.min.js` |
| lottie-web | 5.13.0 | `vendor/lottie-web/lottie.min.js` |
| Tailwind CSS (browser build) | 4.3.4 | `vendor/tailwindcss/tailwind.browser.js` (`<script src>`; стили в `<style type="text/tailwindcss">`) |
| marked | 18.1.3 | `vendor/marked/marked.esm.js` (для страниц сайта) |

Importmap из `tests/NN-slug/v1/index.html`:

```html
<script type="importmap">
{ "imports": {
  "three": "../../../vendor/three/build/three.module.js",
  "three/addons/": "../../../vendor/three/examples/jsm/"
} }
</script>
```
