// Captura un visor de código y registros reales; no simula una terminal.
const fs = require('fs');
const { chromium } = require(process.env.PLAYWRIGHT_PATH || 'playwright');
(async () => {
  const panels = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
  const browser = await chromium.launch({ channel: 'msedge', headless: true });
  const page = await browser.newPage({ viewport: { width: 1000, height: 100 } });
  const images = {};
  for (const panel of panels) {
    await page.setContent('<html lang="es"><meta charset="utf-8"><style>body{margin:0;background:#f3f6f1;color:#173f31;font:16px Segoe UI;padding:30px}h1{font-size:22px;margin:0 0 10px}p{color:#647368;font-size:13px}pre{background:white;border:1px solid #d4dfd7;border-radius:12px;padding:24px;font:20px/1.4 Consolas,monospace;white-space:pre-wrap;overflow-wrap:anywhere}</style><h1></h1><p>FarmaPoint · Lab 09 · Visor de archivos y registros de ejecución</p><pre></pre></html>');
    await page.locator('h1').textContent();
    await page.evaluate(({title,text})=>{document.querySelector('h1').textContent=title;document.querySelector('pre').textContent=text;}, panel);
    images[panel.name] = (await page.screenshot({fullPage:true})).toString('base64');
  }
  await browser.close();
  process.stdout.write(JSON.stringify(images));
})().catch(e=>{console.error(e);process.exit(1)});
