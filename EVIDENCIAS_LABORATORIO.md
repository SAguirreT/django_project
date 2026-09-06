# Evidencias — GLAB-S03: Sistema de gestión de farmacia

Este documento reúne las capturas que deben adjuntarse al informe. Ejecuta los comandos desde `farmacia_project/src` y pega cada imagen debajo de su título.

## 1. Migraciones

### 1.1 `makemigrations`

Comando:

```bash
py manage.py makemigrations farmacia
```

<!-- Pega aquí la captura de la salida de makemigrations. -->

La migración inicial creó las tablas para Categoria, Producto, Proveedor, Cliente y Venta.

### 1.2 `migrate`

Comando:

```bash
py manage.py migrate
```

<!-- Pega aquí la captura de la salida de migrate. -->

Las migraciones pendientes se aplicaron en la base de datos SQLite.

### 1.3 `showmigrations`

Comando:

```bash
py manage.py showmigrations farmacia
```

<!-- Pega aquí la captura donde se vea [X] 0001_initial. -->

La marca `[X]` confirma que la migración de la aplicación fue aplicada correctamente.

## 2. Relaciones entre entidades

Inicia la aplicación:

```bash
py manage.py runserver
```

### 2.1 Categoría y producto

1. Registra una categoría desde `http://127.0.0.1:8000/categoria/nuevo/`.
2. Registra un producto y selecciona esa categoría.
3. Abre `http://127.0.0.1:8000/productos/`.

<!-- Pega aquí la captura del listado de productos mostrando su categoría. -->

La relación `Producto.categoria` es una clave foránea: una categoría puede tener varios productos.

### 2.2 Cliente y venta

1. Registra un cliente desde `http://127.0.0.1:8000/cliente/nuevo/`.
2. Registra una venta y selecciona ese cliente.
3. Abre `http://127.0.0.1:8000/ventas/`.

<!-- Pega aquí la captura del listado de ventas mostrando el cliente asociado. -->

La relación `Venta.cliente` es una clave foránea: un cliente puede tener varias ventas.

## 3. CRUD completo de Producto

### 3.1 CREATE

Abre `http://127.0.0.1:8000/productos/nuevo/`, completa el formulario y registra el producto.

<!-- Pega aquí la captura del formulario antes de registrar. -->

<!-- Pega aquí la captura del listado después del registro. -->

El formulario usa `ProductoForm.save()`, que Django ORM traduce conceptualmente a `INSERT` en SQLite.

### 3.2 READ

Abre `http://127.0.0.1:8000/productos/`.

<!-- Pega aquí la captura del listado de productos. -->

La vista consulta los datos con `Producto.objects.all()`, equivalente conceptualmente a una operación `SELECT`.

### 3.3 UPDATE

Desde el listado, selecciona **Editar**, modifica el registro y guarda.

<!-- Pega aquí la captura del formulario de edición. -->

<!-- Pega aquí la captura del listado con el producto actualizado. -->

El guardado de un objeto existente ejecuta una actualización (`UPDATE`) mediante Django ORM.

### 3.4 DELETE

Desde el listado, selecciona **Eliminar**.

<!-- Pega aquí la captura de la pantalla de confirmación. -->

Confirma la eliminación y captura el listado actualizado.

<!-- Pega aquí la captura del listado después de eliminar. -->

La eliminación solo ocurre mediante una petición POST y utiliza `delete()` a través de Django ORM.

## 4. Flujo de persistencia de Producto

```text
Navegador
  ↓
URL
  ↓
Vista
  ↓
Modelo Producto
  ↓
Django ORM
  ↓
SQLite
  ↓
redirect / render
  ↓
Template
  ↓
Navegador
```

| Operación | URL | Operación ORM | SQL conceptual |
| --- | --- | --- | --- |
| Crear | `/productos/nuevo/` | `form.save()` | `INSERT` |
| Consultar | `/productos/` | `Producto.objects.all()` | `SELECT` |
| Actualizar | `/productos/<id>/editar/` | `form.save()` | `UPDATE` |
| Eliminar | `/productos/<id>/eliminar/` | `objeto.delete()` | `DELETE` |
