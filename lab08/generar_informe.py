"""Genera el informe a partir de código, resultados y capturas verificadas."""
import io
import json
from pathlib import Path
from xml.sax.saxutils import escape

from PIL import Image as PILImage, ImageChops
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, PageBreak,
                                Image, Table, TableStyle, KeepTogether)

HERE = Path(__file__).resolve().parent
OUT = HERE / 'evidencias'
results = json.loads((OUT / 'resultados.json').read_text(encoding='utf-8'))
publication = json.loads((OUT / 'publicacion.json').read_text(encoding='utf-8'))
manifest = json.loads((HERE / 'capturas_manifest.json').read_text(encoding='utf-8'))
specs = dict(json.loads((HERE / 'solicitudes.json').read_text(encoding='utf-8')))
CODE = publication['commit_codigo']
REPO = 'https://github.com/SAguirreT/django_project'

chapters = [
('Instalar DRF e identificar recursos',
 'Se revisó main en GitHub al 17 de octubre de 2026, revisión 8c901e4. Esta versión ya incorporaba Django REST Framework, ProductoQuerySet.con_stock(), serializers, vistas genéricas y ViewSets. Se integró en la copia local preservando las modificaciones previas de las semanas 6 y 7. Se verificó Django 5.2.17 y DRF 3.18.3, con rest_framework en INSTALLED_APPS.',
 'Producto se utiliza como recurso simple y Venta como recurso relacionado. Zona, Farmacia y EvaluacionUbicacion cubren la investigación de ubicaciones. La API reutiliza los modelos y no añade tablas. La configuración permite elegir una SQLite separada mediante FARMAPOINT_DB. manage.py check no reportó problemas y makemigrations --check --dry-run no detectó cambios.',
 'DRF incorpora acceso JSON sin sustituir la interfaz HTML ni el Admin. El PDF de partida afirmaba que no había un QuerySet personalizado: esa descripción se actualizó porque el repositorio de hoy sí lo contiene.'),
('ModelSerializer y serialización',
 'ProductoSerializer define id, nombre, descripcion, precio, stock, categoria y categoria_nombre. El identificador categoria permite escribir la relación; categoria_nombre es de solo lectura y obtiene el nombre mediante source="categoria.nombre".',
 'Se serializó un producto y después los tres productos ficticios con many=True. Los resultados reales están en E02_C02_objeto.json y E02_C03_queryset.json. La colección se consultó con select_related("categoria") para evitar consultas adicionales por cada nombre de categoría.',
 'El serializer convierte instancias del ORM en tipos representables por el renderizador JSON. many=True indica una colección; no cambia los registros ni sustituye una consulta.'),
('Deserialización y validación',
 'validate_precio rechaza valores iguales o menores que cero. La entrada válida usó precio 2.50, stock 1 y una categoría existente. is_valid() devolvió True; validated_data incluyó un Decimal y la instancia relacionada. save() creó un objeto y se comprobó su existencia dentro de una transacción.',
 'La prueba inválida envió precio 0: is_valid() devolvió False y errors incluyó el campo precio. La creación válida se revirtió explícitamente al terminar la demostración, de modo que no dejó un producto temporal. Los datos que fallan validación nunca se guardaron.',
 'La validación del serializer protege las entradas de la API antes de persistirlas. No constituye una restricción universal de la base de datos para escrituras que omitan el serializer.'),
('Vistas genéricas',
 'Se conservaron ProductoListCreateAPIView y ProductoRetrieveUpdateDestroyAPIView del repositorio. La primera resuelve GET y POST de colección; la segunda resuelve GET, PUT, PATCH y DELETE de un producto. Ambas utilizan ProductoSerializer y cargan la categoría con select_related.',
 'Se comprobaron GET /api/v1/basico/productos/ y GET /api/v1/basico/productos/1/, ambos con HTTP 200. Las rutas HTML existentes permanecieron disponibles.',
 'El prefijo basico conserva la etapa de vistas genéricas para demostrar el ejercicio. La API principal usa el router en otra dirección; ninguna URL queda registrada dos veces para las mismas operaciones.'),
('ModelViewSet y DefaultRouter',
 'La API principal utiliza DefaultRouter y registra categorías, productos, farmacias, ventas, zonas y evaluaciones. Los cuatro primeros recursos proceden de la revisión pública; zonas y evaluaciones se incorporaron para cubrir la investigación descrita en el PDF.',
 'GET /api/v1/ devolvió HTTP 200 con los seis recursos. Las operaciones de productos están en /api/v1/productos/ y /api/v1/productos/<id>/. Se conserva el prefijo versionado del repositorio actual en lugar de cambiarlo al /api/ orientativo del documento.',
 'ModelViewSet agrupa las acciones CRUD y el router genera los patrones de lista y detalle. La separación por prefijos permite comparar la etapa genérica con la implementación principal sin conflictos de resolución.'),
('CRUD y códigos HTTP',
 'Se ejecutaron peticiones HTTP reales a productos mediante urllib contra el servidor local de demostración. Se registró método, URL, cuerpo enviado, código y respuesta. El producto temporal creado por POST fue el mismo que se modificó y eliminó.',
 'Resultados: GET lista 200; GET detalle 200; POST válido 201; POST con precio 0, 400; PATCH stock, 200; DELETE, 204 sin cuerpo; GET posterior al mismo ID, 404. También se comprobó en el ORM que el registro borrado ya no existía.',
 'Las capturas corresponden a un visor de resultados HTTP, no a Postman ni Thunder Client. Se adjunta una colección importable de Postman para reproducir el recorrido si el docente exige esa interfaz concreta. La API devuelve datos; los templates generan páginas HTML.'),
('Solo lectura con relación anidada',
 'VentaReadSerializer incluye ClienteSerializer y una colección de DetalleVentaReadSerializer. Cada detalle incorpora ProductoSerializer, cantidad, precio unitario y subtotal. VentaReadOnlyViewSet publica lista y detalle y rechaza POST con HTTP 405.',
 'Se serializaron las mismas tres ventas, con seis detalles y sus productos, antes y después de optimizar. La versión sin precarga realizó 19 consultas y la optimizada 4. Ambas respuestas fueron iguales. Se usa select_related("cliente") y prefetch_related("detalles__producto__categoria").',
 'Se incluyó categoría en la precarga porque ProductoSerializer muestra categoria_nombre. La medición evalúa serializer.data completo; no mide solamente list(queryset), que omitiría los accesos anidados y produciría una comparación engañosa.'),
('Búsqueda ordenamiento filtro y acción',
 'ProductoViewSet usa SearchFilter sobre nombre, descripción y categoría; OrderingFilter permite nombre, precio y stock. El parámetro disponible selecciona productos con o sin existencias. La acción con-stock reutiliza ProductoQuerySet.con_stock() y también respeta los filtros.',
 'La búsqueda Analgesico devolvió dos registros; el orden por precio mostró 5.50, 8.90 y 12.00; búsqueda y orden combinados devolvieron 5.50 y 12.00. La acción con-stock devolvió los dos productos cuyo stock es positivo. Farmacia filtra el campo estado con comparación sin distinguir mayúsculas.',
 'Los filtros componen consultas reutilizables. Se conserva la acción con-stock existente y se añade activas para Farmacia en el ejercicio 13, cubriendo ambas variantes del repositorio y del PDF.'),
('Recursos de la investigación propia',
 'La investigación de ubicaciones utiliza Zona, Farmacia y EvaluacionUbicacion. Zona describe distrito, población, flujo y accesibilidad. Farmacia registra nombre, tipo, distancia y estado. EvaluacionUbicacion guarda competencia, centros de salud, alquiler, ventas estimadas y viabilidad.',
 'Farmacia y EvaluacionUbicacion tienen ForeignKey a Zona: una zona puede tener muchas farmacias y evaluaciones. La base de demostración contiene tres registros de cada modelo. La base local no tenía farmacias al revisarla; los valores Activa, Inactiva y ACTIVA se introdujeron expresamente como datos ficticios.',
 'Se conservan además las siete entidades del módulo comercial. No se duplican modelos para implementar la API. La tabla de equivalencias documenta los recursos, relaciones, validaciones y QuerySets utilizados.'),
('Serializers de la investigación',
 'Se implementaron ZonaSerializer, FarmaciaSerializer y EvaluacionUbicacionSerializer. Farmacia recibe la zona por su identificador y muestra zona_nombre de solo lectura. EvaluacionUbicacion presenta una ZonaSerializer anidada y se expone únicamente para lectura.',
 'FarmaciaSerializer valida distancia_metros > 0. La entrada de 100 metros devolvió is_valid=True; la de 0 metros devolvió False y un error del campo. Se mantienen las opciones Alta, Media y Baja del modelo de evaluación y los tipos definidos en el ORM.',
 'Cada serializer define la representación de su recurso. La validación del campo numérico se realiza antes de crear o actualizar. Un campo anidado read_only no permite escribir automáticamente el objeto relacionado.'),
('ViewSets y códigos HTTP de investigación',
 'ZonaViewSet y FarmaciaViewSet ofrecen operaciones CRUD mediante ModelViewSet. Sus registros se añadieron al mismo DefaultRouter utilizado por la API principal. Los detalles se obtienen mediante el identificador de cada recurso.',
 'Las peticiones HTTP a farmacias produjeron 200 en GET, 201 al crear, 400 con distancia 0, 204 al eliminar el registro temporal y 404 al consultar ese ID eliminado. El CRUD de zonas y el PATCH de ambos recursos se comprobaron además en pruebas automatizadas que verifican los valores persistidos.',
 'Los códigos permiten distinguir una operación válida, un dato rechazado y un recurso inexistente. DELETE se ejecutó solo sobre el registro creado para la prueba. La eliminación de zonas conserva las reglas CASCADE ya definidas por el modelo.'),
('Recurso anidado y optimización',
 'EvaluacionUbicacionReadOnlyViewSet usa EvaluacionUbicacionSerializer con la zona anidada. get_queryset() aplica select_related("zona") y un orden estable por clave primaria. La API responde con la evaluación y la información de su zona en el mismo JSON.',
 'Sobre las tres evaluaciones ficticias, la serialización completa realizó 4 consultas sin optimizar y 1 con select_related. Se comprobó igualdad de respuestas. GET de evaluación devolvió 200; POST devolvió 405. Las pruebas automatizadas también rechazan PATCH y DELETE.',
 'La relación es una ForeignKey y puede resolverse con una unión SQL. Esto evita la consulta adicional de zona por cada evaluación y mantiene la salida de solo lectura.'),
('Filtros y acción en investigación',
 'FarmaciaViewSet permite búsqueda por nombre, tipo, estado y nombre de zona, y orden por nombre, distancia o estado. get_queryset() aplica ?estado= mediante estado__iexact. La acción activas reutiliza FarmaciaQuerySet.activas().',
 'La búsqueda Botica devolvió tres registros, ordenados por distancia en 150, 300 y 450 metros. ?estado=activa devolvió dos. /activas/?search=Botica&ordering=distancia_metros devolvió las activas de 150 y 450 metros. La prueba automatizada verifica también que una condición contradictoria estado=Inactiva en /activas/ devuelve una lista vacía.',
 'La acción pasa por filter_queryset y conserva la paginación si se configura más adelante. La regla del QuerySet evita repetir la lógica de selección de farmacias activas.'),
('Documentación verificación y publicación',
 'Se actualizaron los README y los documentos de evidencia del Lab 08, las dependencias y las instrucciones de ejecución. El informe contiene los tres integrantes solicitados. Se revisaron los cambios y se publicaron con autorización expresa del usuario en main.',
 f'El código se publicó en el commit {CODE}. La copia de publicación, basada en main, ejecutó 25 pruebas correctas. La copia local conservó los cambios adicionales de Semana 7 y ejecutó 32 pruebas correctas. Ambas comprobaciones de esquema finalizaron sin cambios. Las diferencias de cantidad corresponden a esas pruebas locales adicionales.',
 'Las capturas incluyen el estado previo, commit y push reales. La publicación excluye bases SQLite, respaldos, entornos virtuales y archivos temporales. El informe y las evidencias se incorporan en un segundo commit documental para no alterar la referencia del código verificado.'),
]

summary = [
('Código base revisado', '8c901e4, publicado el 17 de octubre de 2026'),
('Código complementario publicado', CODE[:12]),
('Integrantes', 'Dario Maza; Sheila Aguirre; Jose Contreras'),
('Entorno', 'Django 5.2.17; Django REST Framework 3.18.3; SQLite'),
('Pruebas de la versión publicada', '25 correctas'),
('Pruebas de la copia local con Semana 7', '32 correctas'),
('Consultas al serializar ventas', '19 antes; 4 después; respuestas iguales'),
('Consultas al serializar evaluaciones', '4 antes; 1 después; respuestas iguales'),
('Evidencias', '69 PNG; respuestas HTTP JSON; scripts y colección Postman'),
]

fontdir=Path('C:/Windows/Fonts')
pdfmetrics.registerFont(TTFont('ArialStudy',str(fontdir/'arial.ttf')))
pdfmetrics.registerFont(TTFont('ArialStudyBold',str(fontdir/'arialbd.ttf')))
pdfmetrics.registerFontFamily('ArialStudy',normal='ArialStudy',bold='ArialStudyBold')
styles=getSampleStyleSheet()
styles.add(ParagraphStyle(name='BodyStudy',fontName='ArialStudy',fontSize=10.3,leading=15,spaceAfter=9))
styles.add(ParagraphStyle(name='TitleStudy',fontName='ArialStudyBold',fontSize=25,leading=31,spaceAfter=18,textColor=colors.black))
styles.add(ParagraphStyle(name='HeadingStudy',fontName='ArialStudyBold',fontSize=17,leading=22,spaceAfter=12,textColor=colors.black))
styles.add(ParagraphStyle(name='CaptionStudy',fontName='ArialStudy',fontSize=8.7,leading=12,spaceAfter=7,textColor=colors.HexColor('#334155')))
styles.add(ParagraphStyle(name='SmallStudy',fontName='ArialStudy',fontSize=9,leading=13,spaceAfter=7))
story=[]
md=['# Laboratorio 08 Django REST Framework\n\nFarmaPoint\n\nIntegrantes: Dario Maza, Sheila Aguirre y Jose Contreras.\n\nFecha de revisión: 17 de octubre de 2026.\n']
def para(s,style='BodyStudy'):
    return Paragraph(escape(s),styles[style])
def add(s,style='BodyStudy'):
    story.append(para(s,style))
def figure(key, caption=None):
    path=OUT/(key+'.png')
    im=PILImage.open(path).convert('RGB')
    # Retira solo márgenes blancos para aprovechar el área impresa; el PNG original se conserva.
    bbox=ImageChops.difference(im,PILImage.new('RGB',im.size,'white')).getbbox()
    if bbox:
        left,top,right,bottom=bbox
        im=im.crop((max(0,left-10),max(0,top-10),min(im.width,right+10),min(im.height,bottom+10)))
    width=499
    ratio=width/im.width
    height=im.height*ratio
    if height>620:
        ratio=620/im.height; width=im.width*ratio; height=620
    bio=io.BytesIO(); im.save(bio,format='PNG'); bio.seek(0)
    caption=caption or specs.get(key+'.png',key)
    caption=caption.split('GLAB-S08')[0].strip()
    block=[para(key+'  '+caption,'CaptionStudy'),Image(bio,width=width,height=height),Spacer(1,14)]
    story.append(KeepTogether(block))

add('Laboratorio 08\nDjango REST Framework'.replace('\n',' '),'TitleStudy')
add('FarmaPoint','HeadingStudy')
add('Desarrollo de Aplicaciones Empresariales')
add('Integrantes: Dario Maza, Sheila Aguirre y Jose Contreras.')
add('Docente: Yunior Bestard Aroche. Revisión: 17 de octubre de 2026.')
add('Este informe desarrolla los 14 ejercicios del documento GLAB_S08_django.pdf sobre la versión actual del repositorio. Se implementó y comprobó la API de productos, ventas y ubicaciones, preservando las páginas HTML y el administrador.')
rows=[[para(k,'SmallStudy'),para(v,'SmallStudy')] for k,v in summary]
table=Table(rows,colWidths=[180,319],hAlign='LEFT')
table.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),('BACKGROUND',(0,0),(0,-1),colors.HexColor('#edf2f7')),('LINEBELOW',(0,0),(-1,-1),.4,colors.HexColor('#ccd5df')),('LEFTPADDING',(0,0),(-1,-1),9),('RIGHTPADDING',(0,0),(-1,-1),9),('TOPPADDING',(0,0),(-1,-1),7),('BOTTOMPADDING',(0,0),(-1,-1),5)]))
story.append(table);story.append(Spacer(1,15))
story.append(Paragraph('Repositorio: <link href="'+REPO+'" color="#174a7c">'+REPO+'</link>',styles['SmallStudy']))
story.append(PageBreak())
add('Alcance y método de comprobación','HeadingStudy')
for s in [
 'La revisión original del PDF era una propuesta sin ejecución ni capturas. El repositorio consultado hoy ya tenía una implementación parcial. Se conservó ese trabajo y se completaron los recursos y comprobaciones que el PDF exige, sin presentar los resultados anteriores como pruebas de esta ejecución.',
 'Se usó una base SQLite de demostración separada: una categoría, tres productos, tres clientes, tres ventas, seis detalles, tres zonas, tres farmacias y tres evaluaciones. Todos los registros llevan LAB08. Las pruebas automatizadas usan otra base temporal independiente.',
 'Las imágenes de código son capturas de un visor de los archivos reales, con líneas numeradas. Las imágenes de resultados son capturas de JSON producido por peticiones HTTP efectivas al servidor local. Las salidas de serialización proceden de un script Python con Django inicializado, equivalente al código ejecutable en manage.py shell. No se presentan estas imágenes como una terminal ni como Postman.',
 'Las pantallas navegables de DRF se capturaron directamente en Edge. Se adjunta una colección Postman con variables y encadenamiento de IDs para repetir el CRUD. Si se exige estrictamente una captura dentro de Postman o Thunder Client, debe repetirse allí; la evidencia incluida utiliza otro cliente HTTP.',
 'La configuración es local y la API conserva AllowAny de DRF. Las operaciones de escritura de los recursos CRUD no requieren autenticación. Esta entrega no certifica seguridad de producción ni añade facturación, permisos por rol o escritura anidada de ventas.',
 'La copia pública fue preparada desde main para publicar únicamente el trabajo del Lab 08. Los cambios locales previos de Semana 7 se conservaron en la carpeta original y se probaron por separado. Por eso se informan 25 pruebas en publicación y 32 en el entorno local.',
]: add(s);md.append(s+'\n')
add('Mapa de lectura','HeadingStudy')
for i,(title,*_) in enumerate(chapters,1): add(f'{i:02}. {title}','SmallStudy')

for i,(title,response,verification,why) in enumerate(chapters,1):
    story.append(PageBreak())
    add(f'Ejercicio {i:02} {title}','HeadingStudy')
    add(response);add(verification);add('Justificación. '+why)
    md.extend([f'\n## Ejercicio {i:02} {title}\n',response+'\n',verification+'\n','**Justificación.** '+why+'\n'])
    if i==6:
        rows=[[para('Operación','SmallStudy'),para('HTTP real','SmallStudy')]]
        for op,status in [('GET lista / detalle','200'),('POST válido','201'),('POST inválido','400'),('PATCH','200'),('DELETE','204'),('GET tras eliminar','404')]: rows.append([para(op,'SmallStudy'),para(status,'SmallStudy')])
        t=Table(rows,colWidths=[370,129]);t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#edf2f7')),('GRID',(0,0),(-1,-1),.3,colors.lightgrey),('VALIGN',(0,0),(-1,-1),'TOP')]));story.append(t);story.append(Spacer(1,12))
    for item in manifest:
        if item['key'].startswith(f'E{i:02}_'):
            figure(item['key'])
            md.append(f"![{item['key']}](evidencias/{item['key']}.png)\n")

story.append(PageBreak());add('Comprobación visual del navegador','HeadingStudy')
add('Las siguientes capturas son páginas reales de DRF y de la interfaz HTML consultadas en http://127.0.0.1:8008. La venta de muestra muestra dos productos y un total de 17.50.')
for key,caption in [('API_navegador','Índice de la API con seis recursos.'),('Productos_navegador','Detalle de producto en la interfaz navegable DRF.'),('Venta_navegador','Respuesta de solo lectura con cliente y productos anidados.'),('HTML_navegador','La vista HTML de venta continúa disponible.')]: figure(key,caption)

story.append(PageBreak());add('Conclusiones','HeadingStudy')
conclusions=[
 'FarmaPoint expone seis recursos mediante una API versionada. Productos, categorías, zonas y farmacias admiten CRUD; ventas y evaluaciones son de solo lectura y muestran relaciones anidadas. Los serializers rechazan precios y distancias no positivos antes de guardar.',
 'Las comprobaciones HTTP produjeron los códigos 200, 201, 400, 404, 204 y 405 en los escenarios documentados. La igualdad de los JSON antes y después de precargar relaciones confirma que la optimización reduce consultas sin cambiar la información presentada.',
 'Se conservaron el HTML y Django Admin. Los QuerySets personalizados se reutilizan mediante acciones y filtros combinables. El código del laboratorio está publicado y cuenta con pruebas automatizadas; la configuración continúa siendo de desarrollo local.',
]
for s in conclusions:add(s)
add('Cómo reproducir','HeadingStudy')
for s in ['1. Clonar el repositorio y crear un entorno virtual. Instalar farmacia_project/src/requirements.txt.',
          '2. Desde farmacia_project/src, ejecutar migrate y sembrar_lab08. Para aislar los datos, definir FARMAPOINT_DB con la ruta de una SQLite de demostración.',
          '3. Ejecutar manage.py check y manage.py test farmacia. Iniciar runserver 127.0.0.1:8008.',
          '4. Abrir /api/v1/ e importar lab08/FarmaPoint_Lab08.postman_collection.json. Ajustar categoria_id y zona_id si se usa otra base.',
          '5. lab08/recolectar.py reproduce las peticiones y mediciones sobre lab08/demo.sqlite3; requiere que esa base haya sido migrada y sembrada. Los datos y salidas de referencia están en evidencias/.']:add(s)
add('Referencias','HeadingStudy')
for label,url in [('Repositorio y código publicado',REPO+'/commit/'+CODE),('Documento de trabajo','GLAB_S08_django.pdf, proporcionado por el usuario'),('Django REST Framework','https://www.django-rest-framework.org/'),('ViewSets','https://www.django-rest-framework.org/api-guide/viewsets/'),('Filtros','https://www.django-rest-framework.org/api-guide/filtering/')]:
    add(label+': '+url,'SmallStudy')
md.extend(['\n## Conclusiones\n',*conclusions,'\n## Repositorio\n'+REPO+'\n\nCommit de código: '+CODE])
(HERE/'INFORME.md').write_text('\n\n'.join(md),encoding='utf-8')

def footer(canvas,doc):
    canvas.saveState();canvas.setFont('ArialStudy',8)
    canvas.setFillColor(colors.HexColor('#526174'))
    canvas.drawString(48,28,'FarmaPoint | Laboratorio 08 | 17 de octubre de 2026')
    canvas.drawRightString(A4[0]-48,28,str(doc.page));canvas.restoreState()

doc=SimpleDocTemplate(str(HERE/'Informe_Lab08_FarmaPoint.pdf'),pagesize=A4,rightMargin=48,leftMargin=48,
    topMargin=45,bottomMargin=45,title='Laboratorio 08 Django REST Framework FarmaPoint',
    author='Dario Maza; Sheila Aguirre; Jose Contreras')
doc.build(story,onFirstPage=footer,onLaterPages=footer)
print(HERE/'Informe_Lab08_FarmaPoint.pdf')
