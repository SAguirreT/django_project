import { useState } from 'react'
import './App.css'

// Datos locales con los campos de los serializers del Lab 08.
const productos = [
  {
    "id": 1,
    "nombre": "Paracetamol 500 mg",
    "descripcion": "Caja de 10 tabletas",
    "precio": "5.50",
    "stock": 24,
    "categoria": 1,
    "categoria_nombre": "Analgésicos"
  },
  {
    "id": 2,
    "nombre": "Ibuprofeno 400 mg",
    "descripcion": "Caja de 10 cápsulas",
    "precio": "8.90",
    "stock": 0,
    "categoria": 1,
    "categoria_nombre": "Analgésicos"
  },
  {
    "id": 3,
    "nombre": "Alcohol 70%",
    "descripcion": "Frasco de 250 ml",
    "precio": "6.50",
    "stock": 3,
    "categoria": 2,
    "categoria_nombre": "Higiene"
  },
  {
    "id": 4,
    "nombre": "Vitamina C",
    "descripcion": "Tubo de 10 tabletas",
    "precio": "12.00",
    "stock": 12,
    "categoria": 3,
    "categoria_nombre": "Vitaminas"
  },
  {
    "id": 5,
    "nombre": "Mascarillas",
    "descripcion": "Paquete de 5 unidades",
    "precio": "4.90",
    "stock": 2,
    "categoria": 2,
    "categoria_nombre": "Higiene"
  }
]
// FIN PRODUCTOS
const categorias = [
  {
    "id": 1,
    "nombre": "Analgésicos",
    "descripcion": "Alivio del dolor"
  },
  {
    "id": 2,
    "nombre": "Higiene",
    "descripcion": "Cuidado y protección personal"
  },
  {
    "id": 3,
    "nombre": "Vitaminas",
    "descripcion": "Complementos nutricionales"
  }
]
const ventas = [
  {
    "id": 101,
    "cliente": {
      "id": 1,
      "nombre": "Ana Torres",
      "documento": "10000101",
      "telefono": "900000001",
      "correo": "demo@example.com"
    },
    "fecha": "2026-10-17T09:30:00-05:00",
    "total": "27.90",
    "detalles": [
      {
        "id": 1010,
        "producto": {
          "id": 1,
          "nombre": "Paracetamol 500 mg",
          "descripcion": "Caja de 10 tabletas",
          "precio": "5.50",
          "stock": 24,
          "categoria": 1,
          "categoria_nombre": "Analgésicos"
        },
        "cantidad": 2,
        "precio_unitario": "5.50",
        "subtotal": "11.00"
      },
      {
        "id": 1011,
        "producto": {
          "id": 4,
          "nombre": "Vitamina C",
          "descripcion": "Tubo de 10 tabletas",
          "precio": "12.00",
          "stock": 12,
          "categoria": 3,
          "categoria_nombre": "Vitaminas"
        },
        "cantidad": 1,
        "precio_unitario": "12.00",
        "subtotal": "12.00"
      },
      {
        "id": 1012,
        "producto": {
          "id": 5,
          "nombre": "Mascarillas",
          "descripcion": "Paquete de 5 unidades",
          "precio": "4.90",
          "stock": 2,
          "categoria": 2,
          "categoria_nombre": "Higiene"
        },
        "cantidad": 1,
        "precio_unitario": "4.90",
        "subtotal": "4.90"
      }
    ]
  },
  {
    "id": 102,
    "cliente": {
      "id": 2,
      "nombre": "Luis Pérez",
      "documento": "10000102",
      "telefono": "900000001",
      "correo": "demo@example.com"
    },
    "fecha": "2026-10-17T09:30:00-05:00",
    "total": "24.00",
    "detalles": [
      {
        "id": 1020,
        "producto": {
          "id": 4,
          "nombre": "Vitamina C",
          "descripcion": "Tubo de 10 tabletas",
          "precio": "12.00",
          "stock": 12,
          "categoria": 3,
          "categoria_nombre": "Vitaminas"
        },
        "cantidad": 2,
        "precio_unitario": "12.00",
        "subtotal": "24.00"
      }
    ]
  }
]

const moneda = valor => `S/ ${Number(valor).toFixed(2)}`
// Sumar céntimos enteros evita errores de coma flotante en los importes.
const totalVenta = venta => venta.detalles.reduce((s, d) => s + d.cantidad * Math.round(Number(d.precio_unitario) * 100), 0) / 100

export default function App() {
  const nombre = 'FarmaPoint'
  const [busqueda, setBusqueda] = useState('')
  const [categoria, setCategoria] = useState(null)
  const visibles = productos.filter(p => p.nombre.toLowerCase().includes(busqueda.toLowerCase()) && (categoria === null || p.categoria === categoria))
  const unidades = productos.reduce((s, p) => s + p.stock, 0)
  return <div className="app">
    <aside><div className="brand"><b>+</b> FarmaPoint</div><p>GESTIÓN DE FARMACIA</p><nav><a href="#inventario">Inventario</a><a href="#categorias">Categorías</a><a href="#ventas">Ventas</a></nav><small>Datos de demostración<br />Laboratorio 09 · React</small></aside>
    <main><header><div><span className="eyebrow">TU FARMACIA, EN ORDEN</span><h1>{nombre}</h1><p>Consulta tus productos y el detalle de cada venta.</p></div><span className="badge">Vista local</span></header>
      <section className="metrics"><article><span>Productos</span><strong>{productos.length}</strong><small>En el catálogo</small></article><article><span>Unidades disponibles</span><strong>{unidades}</strong><small>Stock acumulado</small></article><article><span>Ventas de ejemplo</span><strong>{moneda(ventas.reduce((s, v) => s + totalVenta(v), 0))}</strong><small>{ventas.length} operaciones registradas</small></article></section>
      <section id="inventario" className="panel"><div className="section-head"><div><span className="eyebrow">01 / CATÁLOGO</span><h2>Inventario de productos</h2></div><span>{visibles.length} resultados</span></div>
        <div className="filters"><label>Buscar producto<input type="search" placeholder="Ej. Paracetamol" value={busqueda} onChange={e => setBusqueda(e.target.value)} /></label><button onClick={() => { setBusqueda(''); setCategoria(null) }}>Limpiar filtros</button></div>
        {/* El ternario elige la lista o el mensaje vacío; map equivale al for de Django. */}
        {visibles.length === 0 ? <p className="empty">No hay registros</p> : visibles.map(p => <article className="product" key={p.id} data-testid="producto"><div><small>{p.categoria_nombre}</small><h3>{p.nombre}</h3><p>{p.descripcion}</p></div><div className="price"><strong>{moneda(p.precio)}</strong><span className={p.stock > 0 ? 'badge available' : 'badge sold'}>{p.stock > 0 ? `Disponible · ${p.stock}` : 'Agotado'}</span>
          {/* && muestra el aviso solo cuando quedan entre 1 y 3 unidades. */}
          {p.stock > 0 && p.stock <= 3 && <small className="warning">¡Últimas unidades!</small>}
        </div></article>)}
      </section>
      <section id="categorias"><div className="section-head"><div><span className="eyebrow">02 / ORGANIZACIÓN</span><h2>Categorías</h2></div><span>Selecciona para filtrar</span></div><div className="categories">{categorias.map(c => <button key={c.id} data-testid="categoria" className={`category ${categoria === c.id ? 'selected' : ''}`} aria-pressed={categoria === c.id} aria-label={`Filtrar por ${c.nombre}`} onClick={() => setCategoria(c.id)}><h3>{c.nombre}</h3><p>{c.descripcion}</p><strong>{productos.filter(p => p.categoria === c.id).length} productos</strong></button>)}</div></section>
      <section id="ventas"><div className="section-head"><div><span className="eyebrow">03 / OPERACIONES</span><h2>Detalle de ventas</h2></div><span>Venta y productos</span></div><div className="sales">
        {/* El map anidado representa Venta 1:N DetalleVenta; cada nivel usa su id. */}
        {ventas.map(v => <article className="panel sale" key={v.id} data-testid="venta"><div className="section-head"><h3>Venta #{v.id}</h3><span className="badge available">Registrada</span></div><p>{v.cliente.nombre} · {new Date(v.fecha).toLocaleDateString('es-PE')}</p><ul>{v.detalles.map(d => <li key={d.id}><span>{d.producto.nombre}<small>{d.cantidad} × {moneda(d.precio_unitario)}</small></span><strong>{moneda(d.cantidad * Number(d.precio_unitario))}</strong></li>)}</ul><div className="total"><span>Total calculado</span><strong data-testid="total-venta">{moneda(totalVenta(v))}</strong></div>
          {/* style recibe un objeto JS con propiedades camelCase. */}
          <div className="track"><div style={{ width: `${Math.min(v.detalles.length / 3 * 100, 100)}%`, backgroundColor: '#14826d', height: '4px' }} /></div><small>{v.detalles.length} líneas de detalle</small>
        </article>)}
      </div></section><footer>FarmaPoint · Dario Maza / Sheila Aguirre / Jose Contreras</footer>
    </main>
  </div>
}
