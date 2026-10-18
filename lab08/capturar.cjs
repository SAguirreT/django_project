// Captura archivos y resultados reales en un visor; no simula VS Code ni Postman.
const fs = require('fs');
const path = require('path');
const {chromium} = require(process.env.PLAYWRIGHT_PATH || 'playwright');
const escape = text => text.replaceAll('&', '&amp;').replaceAll('<', '&lt;').replaceAll('>', '&gt;');
(async () => {
  const browser = await chromium.launch({channel:'msedge', headless:true});
  const page = await browser.newPage({viewport:{width:1440,height:900}, deviceScaleFactor:1});
  const manifest = JSON.parse(fs.readFileSync(path.join(__dirname,'capturas_manifest.json'),'utf8'));
  const captures = {};
  for (const item of manifest) {
    await page.setContent(`<!doctype html><meta charset="utf-8"><style>
      *{box-sizing:border-box}body{margin:0;padding:32px;background:#fff;color:#14243a;font:22px Arial}
      header{border-bottom:3px solid #163b60;padding-bottom:16px}h1{font-size:27px;margin:0 0 10px}
      p{font-size:19px;color:#4b5a6b;margin:0}pre{font:21px/1.45 Consolas,monospace;white-space:pre-wrap;overflow-wrap:anywhere;margin:20px 0 0}
      </style><header><h1>${escape(item.title)}</h1><p>FarmaPoint · Lab 08 · ${escape(item.key)}</p><p>${escape(item.kind)}</p></header>
      <pre>${escape(item.text)}</pre>`);
    captures[item.key] = (await page.screenshot({fullPage:true})).toString('base64');
  }
  for (const [name,url] of [['API_navegador','/api/v1/'],['Productos_navegador','/api/v1/productos/1/'],['Venta_navegador','/api/v1/ventas/1/'],['HTML_navegador','/ventas/1/']]) {
    const response = await page.goto('http://127.0.0.1:8008'+url);
    if(response.status()!==200) throw new Error(url+' HTTP '+response.status());
    captures[name] = (await page.screenshot({fullPage:true})).toString('base64');
  }
  await browser.close();
  process.stdout.write(JSON.stringify(captures));
})().catch(error=>{console.error(error);process.exit(1)});
