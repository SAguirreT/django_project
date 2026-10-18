"""Genera el informe con respuestas y evidencias reales del Lab 09."""
from pathlib import Path
from xml.sax.saxutils import escape
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak, Table, TableStyle, KeepTogether
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.utils import ImageReader
from reportlab.lib.pagesizes import A4

ROOT = Path(__file__).resolve().parent
EV = ROOT / 'evidencias'
OUT = ROOT / 'Informe_Lab09_FarmaPoint.pdf'
styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name='TitleFP', fontName='Helvetica-Bold', fontSize=34, leading=39, textColor=colors.HexColor('#113d36'), spaceAfter=18))
styles.add(ParagraphStyle(name='SectionFP', fontName='Helvetica-Bold', fontSize=19, leading=24, textColor=colors.HexColor('#113d36'), spaceAfter=14))
styles.add(ParagraphStyle(name='BodyFP', fontName='Helvetica', fontSize=10.5, leading=15, spaceAfter=10))
styles.add(ParagraphStyle(name='CaptionFP', fontName='Helvetica', fontSize=8.5, leading=12, textColor=colors.HexColor('#56695e'), spaceAfter=12))
styles.add(ParagraphStyle(name='CellFP', fontSize=9, leading=12))
story = []
def p(text, style='BodyFP'):
    story.append(Paragraph(text, styles[style]))
def heading(text): p(text, 'SectionFP')
def page(title):
    if story: story.append(PageBreak())
    heading(title)
def pic(name, caption, height=380):
    path=EV / (name+'.png')
    w,h=ImageReader(str(path)).getSize()
    scale=min(490/w,height/h)
    story.append(KeepTogether([Image(str(path),width=w*scale,height=h*scale), Spacer(1,7), Paragraph(caption,styles['CaptionFP'])]))
def table(rows,widths):
    data=[[Paragraph(escape(str(v)).replace('\n','<br/>'),styles['CellFP']) for v in row] for row in rows]
    t=Table(data,colWidths=widths,hAlign='LEFT')
    t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#e1eddf')),('VALIGN',(0,0),(-1,-1),'TOP'),('LINEBELOW',(0,0),(-1,-1),.4,colors.HexColor('#d5dfd6')),('LEFTPADDING',(0,0),(-1,-1),8),('RIGHTPADDING',(0,0),(-1,-1),8),('TOPPADDING',(0,0),(-1,-1),8),('BOTTOMPADDING',(0,0),(-1,-1),8)]))
    story.append(t);story.append(Spacer(1,12))

p('DESARROLLO DE APLICACIONES EMPRESARIALES','CaptionFP')
story.append(Spacer(1,25))
p('FarmaPoint<br/>Laboratorio 09','TitleFP')
p('Introducción a React, JSX y Vite','SectionFP')
p('Interfaz de inventario, categorías y ventas con datos locales.')
story.append(Spacer(1,25))
table([['Integrantes','Curso / entrega'],['Dario Maza\nSheila Aguirre\nJose Contreras','Desarrollo de Aplicaciones Empresariales\n4 - C24 - Sección CD\n17 de octubre de 2026']], [245,245])
p('<b>Docente:</b> Yunior Bestard Aroche')
p('<b>Repositorio:</b> <link href="https://github.com/SAguirreT/django_project" color="#14826d">https://github.com/SAguirreT/django_project</link>')
p('<b>Commit del frontend:</b> 6a3a66512b4a56ed9eda498ce7af54b3e3598742')
p('Entrega en PDF y con los integrantes indicados. Se desarrollan los 14 ejercicios de la guía, con justificación, código y resultados verificables. Los datos de productos y clientes son ficticios.')
p('Alcance: React complementa al proyecto Django. Los datos se escriben en arreglos; en esta sesión no se consume la API REST ni se modifican registros de la base de datos.')
p('Las imágenes de la aplicación son capturas reales de Edge. Las imágenes de código y comandos muestran un visor de archivos y registros de ejecución, identificado como tal; no son fotografías de una terminal.','CaptionFP')

page('1. Verificar Node.js y npm')
p('Se verificó Node.js <b>v24.15.0</b> y npm <b>11.12.1</b>. Node permite ejecutar las herramientas de desarrollo de JavaScript; npm instala los paquetes. React es la biblioteca que construye la interfaz y Vite inicia el servidor y genera la compilación.')
table([['Elemento','Python / Django','JavaScript / React'],['Lenguaje','Python; HTML en templates','JavaScript y JSX'],['Gestor de paquetes','pip','npm'],['Dependencias declaradas','requirements.txt','package.json y package-lock.json'],['Dependencias instaladas','Entorno virtual: venv/Lib/site-packages','node_modules/'],['Servidor de desarrollo','python manage.py runserver','npm run dev (ejecuta Vite)']],[115,183,192])
p('<b>Justificación:</b> Node.js no equivale a Django: es un entorno de ejecución. React se encarga de la vista; Django mantiene modelos, validaciones, persistencia y API.')
pic('entorno','E1-E2. Versiones y salida registrada de instalación y arranque.',300)

page('2. Crear y ejecutar el proyecto')
p('Se creó <b>frontend/</b> en la raíz del mismo repositorio. Se usó la plantilla oficial React + JavaScript de create-vite, se ejecutó npm install y se inició Vite en el puerto 5173. La captura siguiente conserva la página inicial antes de sustituirla por FarmaPoint.')
p('<b>Secuencia:</b> npm create vite@latest frontend -- --template react; cd frontend; npm install; npm run dev. La URL solicitada es http://localhost:5173/. Las pruebas finales usan http://127.0.0.1:5173/, que apunta al servidor IPv4 local.')
p('<b>Incidencia resuelta:</b> el lanzador inicial devolvió EBADF al crear archivos. Se ejecutó directamente el CLI oficial create-vite 9.2.1 descargado por npm con --template react --no-interactive. La instalación terminó correctamente. Se conservan los registros de error y recuperación; no se presenta el intento fallido como una ejecución exitosa.')
p('Para los scripts npm de este entorno Windows se utilizó PowerShell como script-shell. Se configuró Vite con --configLoader native para evitar el problema de archivos temporales. El README documenta el ajuste local.')
pic('inicial','E2. Página inicial real de la plantilla, antes de editar App.jsx.',340)

page('3. Reconocer la estructura')
table([['Archivo / carpeta','Función y comparación con Django'],['index.html','Contenedor HTML único con div#root. Se parece al esqueleto de base.html, pero Vite lo sirve sin procesar templates de Django.'],['src/main.jsx','Punto de entrada: createRoot monta App dentro de root. Es un arranque de interfaz; no reemplaza manage.py.'],['src/App.jsx','Componente principal: datos locales, expresiones y JSX. Cumple parte del papel visual que tenía el template.'],['package.json','Declara paquetes y scripts. Equivale parcialmente a requirements.txt; además contiene comandos de desarrollo.'],['package-lock.json','Fija las versiones resueltas para repetir la instalación.'],['node_modules/','Paquetes descargados por npm; equivalente práctico a los paquetes del entorno virtual. No se versiona.']],[130,360])
pic('estructura','E3. Inventario de archivos del frontend; dependencias y compilación se conservan solo localmente.',300)

page('4. Primer JSX con expresiones')
p('Se vaciaron App.css e index.css para observar el HTML sin estilos de la plantilla. El primer componente mostró el nombre de la aplicación en h1. <b>{nombre}</b> inserta una variable y <b>{2 + 3}</b> evalúa un cálculo. Esta etapa se capturó antes de construir la interfaz final.')
p('<b>Justificación:</b> las llaves permiten evaluar expresiones de JavaScript dentro del JSX. No son las dobles llaves del motor de templates de Django: se ejecutan en el entorno de la interfaz React.')
pic('codigo_primero','E4. Código de la etapa inicial.',210)
pic('primer_jsx_detalle','E4. Resultado: FarmaPoint y cinco productos de ejemplo (recorte de la captura inicial).',160)

page('5. Lista con map() y key')
p('El arreglo productos contiene cinco registros. Cada objeto conserva los campos de ProductoSerializer: id, nombre, descripcion, precio, stock, categoria y categoria_nombre. El precio sigue siendo una cadena, como en la respuesta JSON del Lab 08.')
p('La lista se construye con <b>visibles.map(p =&gt; ...)</b>; visibles se obtiene filtrando productos. Cada artículo usa <b>key={p.id}</b>. La función moneda utiliza <b>Number(valor).toFixed(2)</b> para mostrar dos decimales.')
p('<b>Equivalencia:</b> map transforma cada objeto en un elemento JSX. En Django se recorría la colección con {% for producto in productos %} ... {% endfor %}. La key permite que React identifique cada elemento cuando cambia la lista; no se usa la posición del arreglo.')
pic('codigo_funciones','E5. Conversión de importes, datos calculados y filtro local.',210)
pic('codigo_condiciones','E5-E6. Lista con key basada en id y mensajes condicionales.',200)

page('5. Arreglo de productos en App.jsx')
pic('codigo_datos','E5. Cinco objetos con id y decimales como texto; campos del serializer de productos.',630)

page('5. Evidencia de los cinco productos')
pic('inventario','E5. Catálogo completo: cinco productos, 41 unidades y precios con dos decimales.',620)

page('6. Renderizado condicional')
p('El ternario comprueba p.stock &gt; 0: muestra <b>Disponible</b> con la cantidad o <b>Agotado</b>. El operador &amp;&amp; añade <b>¡Últimas unidades!</b> cuando el stock está entre 1 y 3. Ibuprofeno tiene cero unidades; Alcohol tiene tres y Mascarillas tiene dos.')
p('Otro ternario muestra <b>No hay registros</b> cuando visibles.length === 0. Se comprobó tanto una búsqueda sin coincidencias como la sustitución temporal del arreglo productos por []. Después de la prueba se restauraron los cinco registros.')
p('<b>Justificación:</b> el ternario selecciona una de dos salidas. &amp;&amp; incorpora contenido solo cuando la condición es verdadera. La condición usa comparaciones booleanas para evitar que React muestre accidentalmente el número 0.')
pic('vacio_detalle','E6. Resultado real con productos = []; el total de productos y stock baja a cero.',350)

page('7. Relación 1:N con listas anidadas')
p('ventas contiene dos objetos con cliente y detalles. Cada detalle incluye un producto, cantidad, precio_unitario y subtotal. Esta forma corresponde a VentaReadSerializer y DetalleVentaReadSerializer. Se aplica un map por venta y otro por detalle, con key={v.id} y key={d.id}.')
p('<b>Total calculado:</b> la venta 101 suma 2 × 5.50 + 1 × 12.00 + 1 × 4.90 = <b>S/ 27.90</b>. La venta 102 suma 2 × 12.00 = <b>S/ 24.00</b>. El total no se copia del campo total: se recalcula con reduce. Para la suma se convierten los importes a céntimos enteros y se divide entre 100 al final.')
p('<b>Justificación:</b> Venta tiene muchos DetalleVenta. DetalleVenta es también el modelo intermedio entre Venta y Producto, y conserva datos propios de la relación: cantidad y precio unitario.')
pic('codigo_ventas','E7. map anidado, key en ambos niveles, total y conteo.',330)

page('7. Evidencia de categorías y ventas')
pic('categorias_ventas','E7-E12. Tres categorías y dos ventas. Totales y conteos calculados: tres líneas y una línea.',580)

page('8. Estilos y flujo completo')
p('Se aplican clases mediante className y reglas propias en App.css: .app define el contenedor, aside el menú, .available el estado disponible y .sold el agotado, entre otras. Las media queries adaptan el diseño al ancho de un teléfono.')
p('La barra de cada venta usa <b>style={{ width: ..., backgroundColor: ..., height: ... }}</b>. Es un objeto JavaScript; backgroundColor se escribe en camelCase. Su ancho depende de la cantidad de líneas de detalle.')
p('Se cambió temporalmente Paracetamol 500 mg por Paracetamol actualizado en el arreglo y Vite actualizó la página mediante HMR. Luego se restauró el dato. npm run lint y npm run build terminaron con código 0; sus registros aparecen en el ejercicio 13.')
pic('codigo_css','E8. Extractos reales de App.css: estructura y colores de estado.',340)

page('8. Diferencia con Django Templates')
p('En la Semana 6, Django recibía la solicitud, consultaba los datos y renderizaba HTML en el servidor mediante templates, extends, include, for e if. Aquí React monta componentes en el navegador y recalcula la vista cuando cambia el estado. La búsqueda y las categorías usan useState para actualizar la lista sin solicitar otra página.')
p('React no reemplaza Django. Django mantiene la base de datos y la API. Para conectarlos falta sustituir los arreglos por datos obtenidos con fetch u otro cliente HTTP, administrar carga y errores, adaptar la paginación results si está habilitada y configurar la URL de API. Si frontend y backend usan orígenes distintos, se necesita un proxy de desarrollo o CORS; las operaciones autenticadas también requieren manejar sus credenciales y permisos. Esa conexión no se implementa en el Lab 09.')
pic('hmr_detalle','E8. Cambio temporal de un dato visible sin recargar manualmente la página.',350)

page('9. Identificar la investigación propia')
p('La investigación de FarmaPoint y la aplicación de prácticas están en el mismo repositorio. Para la Parte 2 se reutiliza la interfaz de farmacia, identificando de forma explícita sus siete entidades: cinco originales, una de relación 1:1 y el modelo intermedio M:N.')
table([['Grupo','Entidades y relación'],['Cinco originales','Categoria, Producto, Proveedor, Cliente y Venta.'],['Entidad 1:1','PerfilCliente: OneToOneField hacia Cliente.'],['Modelo intermedio','DetalleVenta: une Venta y Producto con cantidad y precio_unitario.']],[120,370])
table([['Criterio','Aplicación concreta'],['Dos entidades mostradas','Producto y Categoria; ambas con arreglo propio y map con id.'],['Campo condicional','Producto.stock: agotado, disponible y últimas unidades.'],['Relación anidada','Venta -> detalles -> producto; DetalleVenta es el intermedio M:N.'],['JSON de referencia','GET /api/v1/productos/, GET /api/v1/categorias/ y GET /api/v1/ventas/.'],['Forma del arreglo','Se modelan los objetos de cada recurso; si la respuesta está paginada, corresponden a los elementos de results, no al envoltorio count/next/previous.']],[120,370])
p('<b>Justificación:</b> no hace falta mostrar las siete entidades en pantalla; la guía pide escoger dos y una relación. Proveedor y PerfilCliente se identifican en models.py, pero no se inventa un endpoint para ellos. Los campos usados se contrastaron con serializers.py del Lab 08.')

page('9. Checklist de la Parte 2')
table([['Criterio','Verificación'],['1. Node y npm','v24.15.0 y 11.12.1; ejercicio 1.'],['2. frontend y servidor','Carpeta raíz y Vite en el puerto 5173; ejercicios 2-3.'],['3. JSX y expresiones','Título {nombre}, {productos.length} y {unidades}; ejercicios 4-5.'],['4. Dos listas con key','Producto y Categoria usan sus id; ejercicios 5 y 10.'],['5. Condicional y lista vacía','Ternario, && y productos = []; ejercicios 6 y 11.'],['6. Relación anidada','ventas.map y detalles.map; ejercicios 7 y 12.'],['7. className y CSS','App.css e inline style; ejercicios 8 y 11.'],['8. Consola, lint y build','Sin eventos de error/advertencia; comandos con salida 0; ejercicio 13.'],['9. Comparación y API','Diferencias con templates y pasos futuros explicados en ejercicio 8.']],[170,320])
p('El checklist se basa en el estado final probado. La prueba automatizada también verificó cinco productos, tres categorías, dos ventas, filtros, importes, HMR, ausencia de desbordamiento horizontal a 390 px y cero solicitudes a /api/.')

page('10. JSX y listas de la investigación')
p('Los arreglos productos y categorias se escribieron dentro de App.jsx. Producto conserva categoria como identificador y categoria_nombre como campo de lectura. Categoria contiene id, nombre y descripcion. No se sustituyó esta forma por campos inventados para la pantalla.')
p('La lista de categorías usa categorias.map(c =&gt; ...) y key={c.id}. Cada tarjeta muestra nombre, descripción y un conteo calculado mediante productos.filter(...).length. Al pulsarla, setCategoria actualiza el filtro local.')
p('<b>Justificación:</b> las dos listas representan entidades distintas. Un arreglo se transforma en tarjetas de categorías y otro en artículos de productos, manteniendo identificadores estables y expresiones entre llaves.')
pic('codigo_categorias','E10. Arreglo de categorías declarado dentro de App.jsx.',240)
pic('codigo_listas','E10. Renderizado con map y key; conteo y filtro por categoría.',190)

page('11. Condicionales y estilos de la investigación')
p('La investigación usa el stock de Producto para las dos condiciones: el ternario muestra disponibilidad y &amp;&amp; agrega el aviso de pocas unidades. La lista vacía tiene un mensaje independiente. El ejemplo de cero existencias no recibe la advertencia de pocas unidades porque se exige stock &gt; 0.')
p('className asigna product, price, badge, available y sold. App.css define sus colores y distribución. La barra de ventas utiliza style con un objeto JavaScript y un ancho derivado del número de detalles. Así se cumplen estilos externos y en línea dentro de la misma interfaz.')
p('<b>Cómo demostrarlo:</b> señalar Ibuprofeno agotado y Alcohol con últimas unidades; escribir un nombre inexistente y pulsar Limpiar filtros para regresar al catálogo. Para demostrar específicamente el arreglo vacío, sustituir productos por [] y después restaurarlo.')
pic('codigo_condiciones','E11. Condiciones reales en App.jsx.',190)
pic('vacio_detalle','E11. Mensaje de lista vacía comprobado.',220)

page('12. Modelo intermedio de la investigación')
p('Venta.productos declara ManyToManyField con through=DetalleVenta. En React la relación se representa con ventas[].detalles[].producto. Cada venta contiene un arreglo de líneas; cada línea conserva cantidad y precio_unitario, además del producto anidado.')
p('El map exterior identifica la venta y el interior identifica el detalle. totalVenta usa reduce para sumar los importes. También se muestra v.detalles.length: tres líneas en la venta 101 y una en la 102. No se usa el id del producto como clave del detalle; la entidad renderizada tiene su propio id.')
p('<b>Cómo demostrarlo:</b> abrir Detalle de ventas, calcular manualmente 11.00 + 12.00 + 4.90 y comparar con S/ 27.90. Después localizar ventas.map y v.detalles.map en App.jsx. El campo total del JSON se conserva como referencia, pero la pantalla muestra el total calculado.')
pic('categorias_ventas','E12. Relación del proyecto de investigación, total y conteo por venta.',420)

page('13. Verificación final')
p('npm run lint y npm run build finalizaron con código 0. La plantilla instalada usa <b>Oxlint</b> en su script lint. Vite compiló 17 módulos. Las pruebas de Edge registraron cero advertencias y cero errores de página, además de cero solicitudes a la API.')
p('Se comprobó que git ls-files frontend/node_modules frontend/dist no devuelve archivos. Ambas carpetas están ignoradas. package-lock.json sí se publica porque fija dependencias. El diagnóstico refleja las acciones probadas, no una garantía sobre escenarios futuros.')
pic('comprobaciones','E13. Salidas reales de npm y eventos capturados del navegador. El arreglo vacío de advertencias confirma que no se observaron avisos de key.',510)

page('14. Publicar en GitHub')
p('Se actualizó el README de la raíz y el del frontend con instalación, ejecución, funciones visibles y demostración. Desde la raíz se entra a frontend, se ejecuta npm install y después npm run dev. npm run build genera los archivos locales de producción.')
p('<b>Repositorio:</b> <link href="https://github.com/SAguirreT/django_project" color="#14826d">https://github.com/SAguirreT/django_project</link>')
p('<b>Código:</b> <link href="https://github.com/SAguirreT/django_project/tree/main/frontend" color="#14826d">github.com/SAguirreT/django_project/tree/main/frontend</link>')
p('El commit 6a3a665 incorpora la interfaz y sus instrucciones. La salida de push confirma la actualización de main. Este informe y las evidencias se publican en un commit posterior para conservar la trazabilidad del código ya probado.')
pic('publicacion','E14. Registro del commit y publicación del frontend; no se añadieron dependencias ni dist.',400)

page('Conclusiones y preparación para sustentar')
p('1. React permite construir la vista mediante componentes, expresiones, map y condiciones. Django continúa siendo responsable del modelo de datos y de la API.')
p('2. Conservar la forma de los serializers facilita la integración futura. En este laboratorio los importes se mantienen como cadenas y solo se convierten al calcular o formatear.')
p('3. Las claves estables, la lista vacía y las condiciones de stock permiten mostrar cambios sin confundir registros. El modelo DetalleVenta conserva la información propia de cada venta.')
p('4. La compilación y las pruebas del navegador comprobaron la interfaz entregada. Los archivos generados y las dependencias se excluyeron del repositorio.')
table([['Pregunta probable','Respuesta y demostración'],['¿Qué hace map?','Convierte cada registro en JSX. Mostrar productos y categorias en App.jsx.'],['¿Para qué sirve key?','Identifica elementos entre renderizados. Señalar key={p.id} y key={d.id}.'],['¿Qué cambia con el ternario y &&?','El ternario elige dos salidas; && añade una salida opcional. Mostrar agotado y pocas unidades.'],['¿Dónde está la relación?','Venta -> DetalleVenta -> Producto. Mostrar el map anidado y el total 27.90.'],['¿Ya consume Django?','No. Los datos son arreglos locales. Explicar fetch, estado, carga y errores como integración futura.'],['¿Cómo probar la lista vacía?','Vaciar temporalmente productos, guardar y ver No hay registros. Restaurar el arreglo.']],[170,320])
p('<b>Fuentes:</b> guía GLAB-S09-YBESTARD-2026-02 proporcionada por el usuario; models.py y serializers.py del repositorio; <link href="https://vite.dev/guide/" color="#14826d">Vite: Getting Started</link>; <link href="https://react.dev/learn/rendering-lists" color="#14826d">React: Rendering Lists</link>. Los registros de ejecución y capturas se conservan en lab09/evidencias/.')

def decorate(canvas,doc):
    canvas.setStrokeColor(colors.HexColor('#d6e0d5'));canvas.line(50,47,A4[0]-50,47)
    canvas.setFont('Helvetica',8);canvas.setFillColor(colors.HexColor('#647368'))
    canvas.drawString(50,32,'FarmaPoint | Laboratorio 09 | 17.10.2026')
    canvas.drawRightString(A4[0]-50,32,str(doc.page))

doc=SimpleDocTemplate(str(OUT),pagesize=A4,rightMargin=50,leftMargin=50,topMargin=45,bottomMargin=62,title='FarmaPoint - Laboratorio 09',author='Dario Maza; Sheila Aguirre; Jose Contreras')
doc.build(story,onFirstPage=decorate,onLaterPages=decorate)
print(OUT)
