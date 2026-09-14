# Guía de capturas y códigos — Laboratorio 04

Ejecuta los comandos desde `farmacia_project/src`.

## Comandos para PowerShell

Tu terminal inicia en la raíz del repositorio, donde **no** existe
`manage.py`. Primero cambia de carpeta y después ejecuta cada comando en una
línea separada:

```powershell
cd .\farmacia_project\src
python manage.py check
python manage.py showmigrations farmacia
python manage.py runserver
```

No copies las tres líneas de `python manage.py ...` como una sola instrucción.
El símbolo `>>` significa que PowerShell está esperando que termines una orden
incompleta. Si aparece, presiona `Ctrl + C` y vuelve a ejecutar los comandos
anteriores uno por uno.

## 1. Preparación

```bash
python manage.py check
python manage.py showmigrations farmacia
python manage.py runserver
```

Captura la terminal mostrando `System check identified no issues` y las tres
migraciones marcadas con `[X]`: `0001_initial`, `0002...` y `0003...`.

<!-- Pega aquí la captura de check y showmigrations. -->

## 2. Código de relaciones

Captura `farmacia/models.py` mostrando estos fragmentos:

```python
class PerfilCliente(models.Model):
    cliente = models.OneToOneField(
        Cliente, on_delete=models.CASCADE, related_name='perfil'
    )
```

```python
class Producto(models.Model):
    categoria = models.ForeignKey(
        Categoria, on_delete=models.CASCADE, related_name='productos'
    )

class Venta(models.Model):
    cliente = models.ForeignKey(
        Cliente, on_delete=models.CASCADE, related_name='ventas'
    )
    productos = models.ManyToManyField(
        Producto, through='DetalleVenta', related_name='ventas'
    )
```

```python
class DetalleVenta(models.Model):
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE, related_name='detalles')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='detalles_venta')
    cantidad = models.PositiveIntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
```

<!-- Pega aquí la captura de models.py. -->

## 3. Datos mínimos para las evidencias

En el navegador crea estos registros, en este orden:

1. Una categoría, por ejemplo `Analgésicos`.
2. Dos productos de esa categoría, por ejemplo `Paracetamol` e `Ibuprofeno`.
3. Un cliente, por ejemplo `Ana Torres`.
4. Un perfil para ese cliente desde `/perfiles/nuevo/`.
5. Una venta para Ana Torres.
6. Dos detalles para la venta desde `/detalles-venta/nuevo/`.

Usa una combinación distinta de venta y producto por detalle, ya que el modelo
evita registrar dos veces el mismo producto en una venta.

## 4. Relación 1:1 — Cliente y PerfilCliente

Abre `http://127.0.0.1:8000/clientes/`.

Debe verse la dirección del perfil en la columna **Perfil (1:1)**. El acceso
directo usado por el template es:

```django
{{ objeto.perfil.direccion }}
```

<!-- Pega aquí la captura del cliente y su perfil. -->

Justificación: `CASCADE` elimina el perfil si se elimina su cliente, porque la
ficha complementaria no tiene sentido por sí sola.

## 5. Relación 1:N — Categoría, Producto y Cliente, Venta

Abre:

- `http://127.0.0.1:8000/categorias/`
- `http://127.0.0.1:8000/clientes/`

La lista de categorías recorre el acceso inverso:

```django
{% for producto in objeto.productos.all %}
    {{ producto.nombre }}
{% endfor %}
```

La lista de clientes muestra sus ventas mediante:

```django
{% for venta in objeto.ventas.all %}
    #{{ venta.pk }}
{% endfor %}
```

<!-- Pega aquí las capturas de categorías con productos y clientes con ventas. -->

## 6. Relación N:M — Venta, Producto y DetalleVenta

Abre `http://127.0.0.1:8000/ventas/<id>/`, sustituyendo `<id>` por el ID de la
venta creada.

El template recorre el modelo intermedio:

```django
{% for detalle in venta.detalles.all %}
    {{ detalle.producto.nombre }}
    {{ detalle.cantidad }}
    {{ detalle.precio_unitario }}
{% endfor %}
```

<!-- Pega aquí la captura de la venta y sus productos. -->

La vista evita consultas repetidas mediante:

```python
Venta.objects.select_related('cliente').prefetch_related('detalles__producto')
```

## 7. CRUD de DetalleVenta

| Operación | URL | Evidencia requerida |
| --- | --- | --- |
| Crear | `/detalles-venta/nuevo/` | Formulario con venta, producto, cantidad y precio. |
| Listar | `/detalles-venta/` | Tabla con venta, cliente, producto, cantidad y subtotal. |
| Editar | `/detalles-venta/<id>/editar/` | Formulario con cantidad o precio modificados. |
| Eliminar | `/detalles-venta/<id>/eliminar/` | Pantalla de confirmación y listado posterior. |

<!-- Pega aquí las cuatro capturas del CRUD. -->

## 8. Flujo ORM documentado

```text
Navegador
  → URL /ventas/<id>/
  → venta_detail
  → Venta.objects.select_related('cliente').prefetch_related('detalles__producto')
  → Django ORM
  → SQLite
  → contexto { venta }
  → venta_detail.html
  → Response
```

| Acción | ORM | SQL conceptual |
| --- | --- | --- |
| Consultar una venta | `get_object_or_404(...)` | `SELECT` con JOIN conceptual |
| Crear detalle | `form.save()` | `INSERT` |
| Editar detalle | `form.save()` | `UPDATE` |
| Eliminar detalle | `detalle.delete()` | `DELETE` |

## 9. Git

Captura el resultado de:

```bash
git log --oneline -3
git status
```

Los commits esperados incluyen `Lab 04: relaciones Django ORM` e `Integra
modelos de evaluación de ubicaciones`.

<!-- Pega aquí la captura de Git. -->

---

# Respuestas para los Ejercicios 1–8

Esta sección está redactada para copiarla en el campo **Descripción** de cada
ejercicio del laboratorio.

## Ejercicio 1 — Recuperar la aplicación de la Semana 3

**Descripción:** La aplicación Django se encuentra en `farmacia_project/src` y
la aplicación principal se llama `farmacia`. El modelo comercial principal es
`Cliente`, ya que registra a las personas que realizan ventas y posee una ficha
complementaria. Las entidades recuperadas de la Semana 3 son `Categoria`,
`Producto`, `Proveedor`, `Cliente` y `Venta`. Las views CRUD genéricas se
encuentran en `farmacia/views.py`, las URLs en `farmacia/urls.py` y los
templates en `templates/farmacia/`. Las migraciones aplicadas son `0001_initial`
(estructura original), `0002_detalleventa_venta_productos_perfilcliente_and_more`
(relaciones del Laboratorio 04) y `0003_zona_farmacia_evaluacionubicacion`
(módulo adicional de evaluación de ubicaciones).

**Capturas:** estructura de carpetas, `models.py`, `views.py`, templates y:

```powershell
cd .\farmacia_project\src
python manage.py showmigrations farmacia
```

## Ejercicio 2 — Relación uno a uno

**Descripción:** Se creó la entidad `PerfilCliente` como ficha complementaria
de `Cliente`. Un cliente puede tener como máximo un perfil y el perfil solo
existe si existe el cliente. La relación usa `OneToOneField` con el
`related_name='perfil'`, lo que permite acceder directamente con
`cliente.perfil`. Se eligió `on_delete=models.CASCADE` porque, si se elimina un
cliente, su ficha complementaria no debe quedar sin propietario.

```python
class PerfilCliente(models.Model):
    cliente = models.OneToOneField(
        Cliente,
        on_delete=models.CASCADE,
        related_name='perfil',
    )
    direccion = models.CharField(max_length=200)
    fecha_registro = models.DateField(auto_now_add=True)
    observaciones = models.TextField(blank=True)
```

**Capturas:** código anterior y `/clientes/` mostrando la columna Perfil (1:1).

## Ejercicio 3 — Relación uno a muchos

**Descripción:** Se conserva la relación `Cliente (1) → (N) Venta` de la
Semana 3. El lado "muchos" es `Venta`, porque un mismo cliente puede realizar
varias ventas, mientras que cada venta pertenece a un solo cliente. Por ese
motivo la `ForeignKey` se declara en `Venta`. El `related_name='ventas'`
permite consultar las ventas de forma inversa con `cliente.ventas.all()`.
También se utiliza `CASCADE`: al eliminar un cliente, sus ventas asociadas no
deben quedar sin cliente.

```python
class Venta(models.Model):
    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.CASCADE,
        related_name='ventas',
    )
```

**Capturas:** código anterior y `/clientes/` mostrando los enlaces de ventas.

## Ejercicio 4 — Muchos a muchos con modelo intermedio

**Descripción:** Se implementó la relación `Venta (N) ↔ (M) Producto`. Una
venta puede contener varios productos y un producto puede participar en muchas
ventas. Se usa `DetalleVenta` como modelo intermedio porque la relación tiene
datos propios: `cantidad` y `precio_unitario` (además se calcula `subtotal`).
`Venta.productos` declara `ManyToManyField` con `through='DetalleVenta'`.

```python
productos = models.ManyToManyField(
    Producto,
    through='DetalleVenta',
    related_name='ventas',
)
```

**Capturas:** `Venta`, `DetalleVenta`, el campo `through` y una venta con dos
productos en `/ventas/<id>/`.

## Ejercicio 5 — Migraciones

**Descripción:** Las migraciones fueron generadas y aplicadas con Django ORM.
La migración `0002` crea `PerfilCliente`, `DetalleVenta` y la relación N:M de
Venta con Producto. `0003` incorpora las entidades del módulo de evaluación de
ubicaciones que coexiste en el proyecto.

```powershell
cd .\farmacia_project\src
python manage.py makemigrations farmacia
python manage.py migrate
python manage.py showmigrations farmacia
```

**Capturas:** una captura de cada comando, mostrando `OK` y las marcas `[X]`.

## Ejercicio 6 — Consultas desde las Views

**Descripción:** `select_related()` se utiliza para cargar relaciones de un
solo objeto en la misma consulta, por ejemplo el perfil de cada cliente. Para
la relación N:M se utiliza `prefetch_related()` y se recuperan los detalles y
productos de una venta sin realizar una consulta repetida por cada detalle.

```python
# Relación 1:1 y acceso inverso 1:N
Cliente.objects.select_related('perfil').prefetch_related('ventas')

# Relación N:M mediante el modelo intermedio
Venta.objects.select_related('cliente').prefetch_related('detalles__producto')
```

**Captura:** función `entidad_list` y función `venta_detail` de `views.py`.

## Ejercicio 7 — Datos relacionados en Templates

**Descripción:** Los templates muestran las tres formas de navegación de
relaciones. El acceso directo muestra la dirección del perfil; el acceso
inverso recorre las ventas de un cliente; y el template de detalle de venta
recorre `DetalleVenta` para obtener cada producto, cantidad y precio.

```django
{# Acceso directo 1:1 #}
{{ objeto.perfil.direccion }}

{# Acceso inverso 1:N #}
{% for venta in objeto.ventas.all %}
  #{{ venta.pk }}
{% endfor %}

{# Modelo intermedio N:M #}
{% for detalle in venta.detalles.all %}
  {{ detalle.producto.nombre }} - {{ detalle.cantidad }}
{% endfor %}
```

**Capturas:** `/clientes/`, `/categorias/` y `/ventas/<id>/`.

## Ejercicio 8 — Flujo de una relación

**Descripción:** Para mostrar una venta y sus productos, el navegador solicita
`/ventas/<id>/`. La URL llama a `venta_detail`, que consulta `Venta` mediante
`select_related('cliente')` y `prefetch_related('detalles__producto')`. Django
ORM ejecuta consultas `SELECT` sobre SQLite y construye el objeto `venta` con
su cliente, detalles y productos. La view envía `venta` al contexto;
`venta_detail.html` recorre `venta.detalles.all` y produce la respuesta HTML.
Al registrar, editar o eliminar un detalle, `form.save()` representa
conceptualmente un `INSERT` o `UPDATE`, y `detalle.delete()` representa un
`DELETE`.

```text
Request → /ventas/<id>/ → venta_detail → ORM → SQLite →
venta (contexto) → venta_detail.html → Response
```
