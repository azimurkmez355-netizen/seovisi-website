// hazirla.py tarafından çağrılır: ekran görüntüsünü koyu, ışıklı zeminde pencere + yakın çekim kartı olarak çizer.
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');
const [isYolu, cikti] = process.argv.slice(2);
const isler = JSON.parse(fs.readFileSync(isYolu, 'utf8'));
const FONT = 'file://' + path.resolve(__dirname, '../../site/fontlar/plus-jakarta-sans.woff2');
const kacir = (m) => String(m).replace(/[&<>"]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
const sablon = (i) => `<!doctype html><html lang="tr"><head><meta charset="utf-8"><style>
@font-face{font-family:PJS;src:url('${FONT}') format('woff2');font-weight:400 800}
*{box-sizing:border-box;margin:0;padding:0}
body{width:1600px;height:1000px;overflow:hidden;position:relative;font-family:PJS,sans-serif;background:#111218}
.zemin{position:absolute;inset:0;background:radial-gradient(900px 620px at 0% 0%,rgba(43,192,113,.24),transparent 62%),radial-gradient(900px 720px at 100% 25%,rgba(90,112,255,.3),transparent 62%),radial-gradient(800px 520px at 55% 115%,rgba(90,112,255,.2),transparent 62%),#111218}
.kafes{position:absolute;inset:0;background-image:linear-gradient(rgba(255,255,255,.045) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,.045) 1px,transparent 1px);background-size:56px 56px;-webkit-mask-image:radial-gradient(ellipse 85% 80% at 50% 40%,#000 30%,transparent 82%)}
.pencere{position:absolute;left:58px;top:62px;width:1250px;border-radius:20px;background:#fff;overflow:hidden;box-shadow:0 0 0 1px rgba(255,255,255,.14),0 50px 120px -30px rgba(0,0,0,.85),0 0 160px -30px rgba(90,112,255,.55)}
.pencere-ust{height:38px;display:flex;align-items:center;gap:8px;padding:0 16px;background:#F3F4F6;border-bottom:1px solid #E5E7EB}
.pencere-ust i{width:12px;height:12px;border-radius:50%;background:#D1D5DB}
.pencere-ust span{margin:0 auto;padding:4px 16px;border-radius:7px;background:#E5E7EB;color:#6B7280;font-size:13px;font-weight:600;letter-spacing:.01em}
.pencere img{display:block;width:100%}
.yakin{position:absolute;right:46px;bottom:54px;width:${i.genislik}px;padding:14px 16px;border-radius:18px;background:#F3F3F2;overflow:hidden;box-shadow:0 0 0 1px rgba(21,22,26,.08),0 0 0 7px rgba(255,255,255,.07),0 40px 90px -18px rgba(0,0,0,.8)}
.yakin img{display:block;width:100%;border-radius:8px}
.etiket{position:absolute;right:46px;display:inline-flex;align-items:center;gap:12px;padding:12px 20px;border-radius:999px;background:rgba(20,21,27,.88);color:#fff;font-size:21px;font-weight:700;letter-spacing:-.01em;box-shadow:inset 0 0 0 1px rgba(255,255,255,.18),inset 0 1px 0 rgba(255,255,255,.2),0 18px 40px -12px rgba(0,0,0,.7)}
.etiket i{width:13px;height:13px;border-radius:4px;background:#2BC071;box-shadow:0 0 14px rgba(43,192,113,.9)}
</style></head><body><div class="zemin"></div><div class="kafes"></div>
<div class="pencere"><div class="pencere-ust"><i></i><i></i><i></i><span>app.seovisi.com.tr</span></div><img src="file://${i.ana}"></div>
<div class="yakin" id="yakin"><img src="file://${i.yakin}"></div>
<div class="etiket" id="etiket"><i></i>${kacir(i.etiket)}</div></body></html>`;
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1600, height: 1000 } });
  for (const i of isler) {
    const f = path.join(cikti, `vitrin-${i.ad}.html`);
    fs.writeFileSync(f, sablon(i));
    await p.goto('file://' + f);
    await p.evaluate(() => document.fonts.ready);
    await p.waitForFunction(() => [...document.images].every(x => x.complete));
    await p.evaluate(() => { const y = document.getElementById('yakin').getBoundingClientRect(); const e = document.getElementById('etiket'); e.style.top = (y.top - e.offsetHeight - 16) + 'px'; });
    await p.screenshot({ path: path.join(cikti, `vitrin-${i.ad}.png`) });
  }
  await b.close();
  console.log('tamam');
})();
