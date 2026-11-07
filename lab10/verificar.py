"""Comprueba interacciones reales y captura las dos partes del laboratorio.""" # Describe el objetivo del script.
import json, os # Importa el registro estructurado y la configuración del navegador.
from pathlib import Path # Resuelve las rutas de evidencias.
from playwright.sync_api import sync_playwright, expect # Importa Chromium y aserciones de interfaz.
E = Path(__file__).parent / 'evidencias' # Define el destino de las capturas.
os.environ.setdefault('PLAYWRIGHT_BROWSERS_PATH', '/workspace/work/browsers') # Usa el navegador instalado dentro del espacio de trabajo.
with sync_playwright() as p: # Abre el contexto de automatización.
    browser = p.chromium.launch() # Inicia Chromium sin interfaz gráfica.
    page = browser.new_page(viewport={'width': 1440, 'height': 1050}) # Fija un tamaño reproducible.
    mensajes = [] # Acumula advertencias y errores reales.
    page.on('console', lambda m: mensajes.append(m.text) if m.type in ('warning', 'error') else None) # Observa los problemas de consola.
    page.on('pageerror', lambda e: mensajes.append(str(e))) # Observa excepciones no controladas.
    page.goto('http://127.0.0.1:5173/') # Carga el frontend de desarrollo.
    for parte, selector in [('parte1', '#inventario'), ('parte2', '#investigacion > section')]: # Repite la prueba en las dos listas independientes.
        zona = page.locator(selector) # Limita las interacciones a la parte seleccionada.
        expect(zona.get_by_test_id('producto')).to_have_count(5) # Verifica los cinco datos originales.
        zona.screenshot(path=str(E / f'{parte}_antes.png')) # Captura la lista antes del clic.
        zona.get_by_role('button', name='Reservar Paracetamol 500 mg', exact=True).click() # Incrementa un contador local.
        expect(zona.get_by_text('Reservas: 1', exact=True)).to_be_visible() # Verifica el estado después del clic.
        expect(zona.get_by_role('button', name='Reservar Ibuprofeno 400 mg', exact=True)).to_be_disabled() # Comprueba el bloqueo por falta de stock.
        expect(zona.get_by_test_id('producto').filter(has_text='Vitamina C').get_by_text('Reservas: 1')).to_have_count(0) # Comprueba que no se comparte el contador.
        zona.screenshot(path=str(E / f'{parte}_clic.png')) # Captura la interacción completada.
        buscar = zona.get_by_label('Buscar producto') # Obtiene el buscador controlado.
        for consulta, cantidad, sufijo in [('PARA', 1, 'busqueda1'), ('zzzz', 0, 'busqueda2')]: # Prueba coincidencias insensibles a mayúsculas y un resultado vacío.
            buscar.fill(consulta) # Dispara onChange con el valor escrito.
            expect(zona.get_by_test_id('producto')).to_have_count(cantidad) # Verifica la cantidad filtrada.
            zona.screenshot(path=str(E / f'{parte}_{sufijo}.png')) # Registra cada búsqueda.
        buscar.fill('') # Restablece la búsqueda para probar el formulario.
        zona.get_by_label('Nombre', exact=True).fill('Producto de prueba') # Controla el campo de nombre.
        zona.get_by_label('Precio', exact=True).fill('0') # Viola la regla real del serializer.
        zona.get_by_label('Stock', exact=True).fill('2') # Completa un stock válido.
        zona.get_by_role('button', name='Agregar producto', exact=True).click() # Ejecuta onSubmit sin navegación.
        expect(zona.get_by_role('alert')).to_have_text('El precio debe ser mayor que cero.') # Verifica el mensaje de validación.
        expect(zona.get_by_test_id('producto')).to_have_count(5) # Confirma que el envío inválido no agrega datos.
        zona.screenshot(path=str(E / f'{parte}_invalido.png')) # Captura el rechazo de la validación.
        zona.get_by_label('Precio', exact=True).fill('7.50') # Corrige el precio según la regla de Django.
        zona.get_by_role('button', name='Agregar producto', exact=True).click() # Agrega un producto con un arreglo nuevo.
        expect(zona.get_by_test_id('producto')).to_have_count(6) # Verifica la inserción local.
        expect(zona.get_by_label('Nombre', exact=True)).to_have_value('') # Comprueba la limpieza del formulario.
        zona.screenshot(path=str(E / f'{parte}_valido.png')) # Captura el envío correcto.
    assert page.locator('#ventas').inner_text().count('27.90') == 1 # Verifica el primer total calculado.
    page.locator('#ventas').screenshot(path=str(E / 'relacion.png')) # Captura Venta y DetalleVenta.
    mutacion = page.evaluate("() => { 'use strict'; const props = Object.freeze({nombre: 'Original'}); try { props.nombre = 'Cambio'; } catch (e) { return e.name + ': ' + e.message; } }") # Reproduce de forma aislada el error de modificar props congeladas.
    assert 'TypeError' in mutacion # Confirma el error sin introducir fallos en la aplicación.
    page.set_viewport_size({'width': 390, 'height': 844}) # Comprueba una pantalla móvil.
    page.screenshot(path=str(E / 'movil.png')) # Captura el diseño adaptable.
    assert page.evaluate('document.documentElement.scrollWidth <= innerWidth') # Detecta desbordamiento horizontal.
    assert not mensajes, mensajes # Exige una consola sin errores ni advertencias.
    (E / 'navegador.json').write_text(json.dumps({'resultado': 'OK', 'partes_verificadas': 2, 'consola': mensajes, 'mutacion_props_aislada': mutacion, 'pruebas': ['contadores independientes', 'stock agotado', 'dos búsquedas', 'envío inválido', 'envío válido', 'limpieza de campos', 'total calculado', 'móvil sin desbordamiento']}, ensure_ascii=False, indent=2)) # Guarda la evidencia verificable.
    browser.close() # Libera el navegador.
