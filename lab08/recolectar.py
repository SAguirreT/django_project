"""Ejecuta peticiones HTTP reales y mediciones ORM para el informe del Lab 08."""
import json
import os
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / 'farmacia_project/src'
OUT = ROOT / 'lab08/evidencias'
os.environ['FARMAPOINT_DB'] = str(ROOT / 'lab08/demo.sqlite3')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
sys.path.insert(0, str(SRC))
import django
django.setup()
from django.db import connection, transaction
from django.test.utils import CaptureQueriesContext
from farmacia.models import Producto, Farmacia, Venta, EvaluacionUbicacion, Zona
from farmacia.serializers import ProductoSerializer, FarmaciaSerializer, VentaReadSerializer, EvaluacionUbicacionSerializer

BASE = 'http://127.0.0.1:8008'
evidencias = {}

def save(key, value):
    evidencias[key] = value
    (OUT / (key + '.json')).write_text(json.dumps(value, ensure_ascii=False, indent=2, default=str), encoding='utf-8')

def http(key, method, path, body=None, expected=200):
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(BASE + path, data=data, method=method,
        headers={'Accept': 'application/json', 'Content-Type': 'application/json'})
    try:
        response = urllib.request.urlopen(req, timeout=15)
    except urllib.error.HTTPError as error:
        response = error
    with response:
        raw = response.read().decode()
        parsed = json.loads(raw) if raw else None
        value = {'metodo': method, 'url': BASE + path, 'cuerpo_enviado': body,
                 'estado_http': response.status, 'respuesta': parsed}
    assert value['estado_http'] == expected, value
    save(key, value)
    return parsed

try:
    urllib.request.urlopen(BASE + '/api/v1/', timeout=2).close()
except Exception:
    log = (OUT / 'servidor.log').open('w', encoding='utf-8')
    proc = subprocess.Popen([sys.executable, '-u', 'manage.py', 'runserver', '127.0.0.1:8008', '--noreload'],
        cwd=SRC, env=os.environ.copy(), stdout=log, stderr=log, creationflags=subprocess.CREATE_NO_WINDOW)
    for _ in range(30):
        try:
            urllib.request.urlopen(BASE + '/api/v1/', timeout=1).close()
            break
        except Exception:
            time.sleep(.3)
    else:
        raise RuntimeError('El servidor no inició: ' + (OUT / 'servidor.log').read_text())

p = Producto.objects.filter(nombre__contains='[LAB08]').select_related('categoria').first()
save('E02_C02_objeto', {'expresion': 'ProductoSerializer(producto).data', 'resultado': ProductoSerializer(p).data})
save('E02_C03_queryset', {'expresion': 'ProductoSerializer(Producto.objects.select_related("categoria"), many=True).data',
    'resultado': ProductoSerializer(Producto.objects.select_related('categoria'), many=True).data})
datos = {'nombre': 'Temporal validacion LAB08', 'descripcion': '', 'precio': '2.50', 'stock': 1, 'categoria': p.categoria_id}
with transaction.atomic():
    s = ProductoSerializer(data=datos)
    assert s.is_valid(), s.errors
    obj = s.save()
    save('E03_C02_valido', {'is_valid': True, 'validated_data': s.validated_data,
         'save_id': obj.pk, 'persistido': Producto.objects.filter(pk=obj.pk).exists(), 'limpieza': 'rollback al finalizar la prueba'})
    transaction.set_rollback(True)
s = ProductoSerializer(data={**datos, 'precio': '0'})
save('E03_C03_invalido', {'is_valid': s.is_valid(), 'errors': s.errors})

http('E04_C03_lista', 'GET', '/api/v1/basico/productos/')
http('E04_C04_detalle', 'GET', f'/api/v1/basico/productos/{p.pk}/')
http('E05_C03_api_root', 'GET', '/api/v1/')
http('E06_C01_get_lista', 'GET', '/api/v1/productos/')
http('E06_C02_get_detalle', 'GET', f'/api/v1/productos/{p.pk}/')
created = http('E06_C03_post_valido', 'POST', '/api/v1/productos/', datos, 201)
url = f'/api/v1/productos/{created["id"]}/'
http('E06_C04_post_invalido', 'POST', '/api/v1/productos/', {**datos, 'precio': '0'}, 400)
http('E06_C05_patch', 'PATCH', url, {'stock': 3}, 200)
http('E06_C06_delete', 'DELETE', url, expected=204)
http('E06_C07_no_encontrado', 'GET', url, expected=404)
assert not Producto.objects.filter(pk=created['id']).exists()

for label, serializer, before, after in [
    ('E07', VentaReadSerializer, Venta.objects.order_by('pk'),
     Venta.objects.select_related('cliente').prefetch_related('detalles__producto__categoria').order_by('pk')),
    ('E12', EvaluacionUbicacionSerializer, EvaluacionUbicacion.objects.order_by('pk'),
     EvaluacionUbicacion.objects.select_related('zona').order_by('pk'))]:
    with CaptureQueriesContext(connection) as c1:
        a = serializer(before, many=True).data
    with CaptureQueriesContext(connection) as c2:
        b = serializer(after, many=True).data
    assert a == b
    keys = ('E07_C03_consultas_antes', 'E07_C04_consultas_despues') if label == 'E07' else ('E12_C03_antes', 'E12_C04_despues')
    for key, captured in zip(keys, [c1, c2]):
        save(key, {'registros': len(a), 'consultas': len(captured), 'serializacion_completa': True,
             'respuestas_iguales': a == b, 'sql': [x['sql'] for x in captured]})

http('E07_C05_respuesta_api', 'GET', '/api/v1/ventas/1/')
http('E07_solo_lectura', 'POST', '/api/v1/ventas/', {}, 405)
http('E08_C04_search', 'GET', '/api/v1/productos/?search=Analgesico')
http('E08_C05_ordering', 'GET', '/api/v1/productos/?ordering=precio')
http('E08_C06_combinacion', 'GET', '/api/v1/productos/?search=Analgesico&ordering=precio&disponible=true')
http('E08_C07_action_resultado', 'GET', '/api/v1/productos/con-stock/')
save('E09_C03_tabla_equivalencias', {'simple': 'Producto; precio > 0', 'relacionado': 'Venta -> DetalleVenta -> Producto',
    'investigacion': ['Zona', 'Farmacia', 'EvaluacionUbicacion'], 'estado': 'Farmacia.estado',
    'relaciones': ['Zona 1:N Farmacia', 'Zona 1:N EvaluacionUbicacion'],
    'querysets': ['ProductoQuerySet.con_stock()', 'FarmaciaQuerySet.activas()'],
    'cantidades': {'zonas': Zona.objects.count(), 'farmacias': Farmacia.objects.count(), 'evaluaciones': EvaluacionUbicacion.objects.count()},
    'estados_demo': list(Farmacia.objects.values_list('estado', flat=True).distinct()),
    'nota': 'Antes de sembrar, no había farmacias locales. Los estados son datos ficticios explícitos.'})
z = Zona.objects.first()
datos_f = {'nombre': 'Botica temporal [LAB08]', 'tipo': 'Independiente', 'zona': z.pk, 'distancia_metros': 100, 'estado': 'Activa'}
for key, distance in [('E10_C02_validacion_valida', 100), ('E10_C03_validacion_invalida', 0)]:
    s = FarmaciaSerializer(data={**datos_f, 'distancia_metros': distance})
    valid = s.is_valid()
    save(key, {'datos': s.initial_data, 'is_valid': valid, 'validated_data': s.validated_data, 'errors': s.errors})
http('E11_C03_http_200', 'GET', '/api/v1/farmacias/')
created = http('E11_C04_http_201', 'POST', '/api/v1/farmacias/', datos_f, 201)
url = f'/api/v1/farmacias/{created["id"]}/'
http('E11_C05_http_400', 'POST', '/api/v1/farmacias/', {**datos_f, 'distancia_metros': 0}, 400)
http('E11_C07_http_204', 'DELETE', url, expected=204)
http('E11_C06_http_404', 'GET', url, expected=404)
http('E11_zonas', 'GET', '/api/v1/zonas/')
http('E12_C05_respuesta', 'GET', '/api/v1/evaluaciones/1/')
http('E12_solo_lectura', 'POST', '/api/v1/evaluaciones/', {}, 405)
http('E13_C04_search', 'GET', '/api/v1/farmacias/?search=Botica')
http('E13_C05_ordering', 'GET', '/api/v1/farmacias/?ordering=distancia_metros')
http('E13_C06_filtro_parametro', 'GET', '/api/v1/farmacias/?estado=activa')
http('E13_C07_action_resultado', 'GET', '/api/v1/farmacias/activas/?search=Botica&ordering=distancia_metros')
for path in ['/', '/productos/', '/ventas/1/', '/detalles-venta/']:
    response = urllib.request.urlopen(BASE + path)
    assert response.status == 200
save('regresion_html', {'rutas': ['/', '/productos/', '/ventas/1/', '/detalles-venta/'], 'estado': 200})
(OUT / 'resultados.json').write_text(json.dumps(evidencias, ensure_ascii=False, indent=2, default=str), encoding='utf-8')
print(json.dumps({'evidencias': len(evidencias), 'ventas_antes': evidencias['E07_C03_consultas_antes']['consultas'],
    'ventas_despues': evidencias['E07_C04_consultas_despues']['consultas'],
    'evaluaciones_antes': evidencias['E12_C03_antes']['consultas'], 'evaluaciones_despues': evidencias['E12_C04_despues']['consultas']}))
