// Capturas y comprobaciones reales del frontend en Edge.
const { chromium } = require(process.env.PLAYWRIGHT_PATH || 'playwright');
const fs = require('fs');
const path = require('path');
(async () => {
  const mode = process.argv[2] || 'final';
  const browser = await chromium.launch({channel:'msedge',headless:true});
  const page = await browser.newPage({viewport:{width:1440,height:1000}});
  const consoleIssues = [], errors = [], apiRequests = [];
  page.on('console', msg => { if(['error','warning'].includes(msg.type())) consoleIssues.push(msg.text()); });
  page.on('pageerror', error => errors.push(error.message));
  page.on('request', request => { if(request.url().includes('/api/')) apiRequests.push(request.url()); });
  const response = await page.goto('http://127.0.0.1:5173/');
  if(response.status()!==200) throw new Error('La página no respondió con 200');
  await page.locator('h1').first().waitFor();
  await page.evaluate(()=>document.fonts.ready);
  const captures = {};
  const capture = async name => { captures[name] = (await page.screenshot({fullPage:true})).toString('base64'); };
  if(mode==='inicial' || mode==='primer_jsx') {
    await capture(mode);
  } else {
    const assert = (condition,message) => { if(!condition) throw new Error(message); };
    assert(await page.locator('[data-testid="producto"]').count()===5,'Deben aparecer cinco productos');
    assert(await page.locator('[data-testid="categoria"]').count()===3,'Deben aparecer tres categorías');
    assert(await page.locator('[data-testid="venta"]').count()===2,'Deben aparecer dos ventas');
    assert(await page.getByText('Agotado',{exact:true}).count()===1,'Falta Agotado');
    assert(await page.getByText('¡Últimas unidades!',{exact:true}).count()===2,'Faltan avisos de poco stock');
    assert((await page.locator('[data-testid="total-venta"]').allTextContents()).join('|').includes('27.90'),'Total venta 101 incorrecto');
    assert((await page.locator('[data-testid="total-venta"]').allTextContents()).join('|').includes('24.00'),'Total venta 102 incorrecto');
    await capture('interfaz_completa');
    await page.getByRole('searchbox').fill('inexistente');
    await page.getByText('No hay registros',{exact:true}).waitFor();
    await capture('busqueda_vacia');
    await page.getByRole('button',{name:'Limpiar filtros'}).click();
    assert(await page.locator('[data-testid="producto"]').count()===5,'Restauración incorrecta');
    await page.getByRole('button',{name:'Filtrar por Higiene'}).click();
    assert(await page.locator('[data-testid="producto"]').count()===2,'Filtro por categoría incorrecto');
    await page.getByRole('button',{name:'Limpiar filtros'}).click();
    const appPath=path.join(__dirname,'../frontend/src/App.jsx');
    const original=fs.readFileSync(appPath,'utf8');
    if(!original.includes('Paracetamol 500 mg')) throw new Error('Fuente inesperada');
    try {
      fs.writeFileSync(appPath,original.replace('const productos = [','const productosBase = [').replace('// FIN PRODUCTOS','// FIN PRODUCTOS\nconst productos = []'));
      await page.getByText('No hay registros',{exact:true}).waitFor();
      assert(await page.locator('[data-testid="producto"]').count()===0,'El arreglo no está vacío');
      await capture('arreglo_vacio');
    } finally { fs.writeFileSync(appPath,original); }
    await page.locator('[data-testid="producto"]').first().waitFor();
    await page.waitForTimeout(1100);
    try {
      fs.writeFileSync(appPath,original.replace('"nombre": "Paracetamol 500 mg"','"nombre": "Paracetamol actualizado"'));
      await page.getByRole('searchbox').fill('');
      await page.getByRole('button',{name:'Limpiar filtros'}).click();
      await page.getByText('Paracetamol actualizado',{exact:true}).first().waitFor();
      await capture('actualizacion_hmr');
    } finally { fs.writeFileSync(appPath,original); }
    await page.getByText('Paracetamol 500 mg',{exact:true}).first().waitFor();
    await page.setViewportSize({width:390,height:844});
    assert(await page.evaluate(()=>document.documentElement.scrollWidth<=window.innerWidth),'Desbordamiento horizontal móvil');
    await capture('movil');
    assert(consoleIssues.length===0,'Advertencias: '+consoleIssues.join(';'));
    assert(errors.length===0,'Errores: '+errors.join(';'));
    assert(apiRequests.length===0,'El laboratorio no debe consumir la API');
  }
  await browser.close();
  process.stdout.write(JSON.stringify({captures,diagnostico:{modo:mode,http:200,advertencias:consoleIssues,errores:errors,solicitudes_api:apiRequests}}));
})().catch(error=>{console.error(error);process.exit(1)});
