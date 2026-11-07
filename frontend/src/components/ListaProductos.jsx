import { useState } from 'react' // Importa estado para el formulario, el catálogo y el filtro.
import ProductoCard from './ProductoCard.jsx' // Importa la tarjeta reutilizable de cada registro.
export default function ListaProductos({ iniciales, categorias }) { // Recibe los arreglos originales mediante props desestructuradas.
  const [productos, setProductos] = useState(iniciales) // Guarda una lista independiente para cada parte del laboratorio.
  const [busqueda, setBusqueda] = useState('') // Controla el texto de búsqueda.
  const [categoria, setCategoria] = useState('') // Controla el filtro por categoría.
  const [nombre, setNombre] = useState('') // Controla el nombre del nuevo producto.
  const [precio, setPrecio] = useState('') // Conserva el precio escrito hasta validarlo.
  const [stock, setStock] = useState('') // Controla las unidades del nuevo producto.
  const [error, setError] = useState('') // Guarda el mensaje de validación.
  const [aviso, setAviso] = useState('') // Confirma el envío correcto de forma accesible.
  const visibles = productos.filter(p => p.nombre.toLowerCase().includes(busqueda.toLowerCase()) && (!categoria || p.categoria === Number(categoria))) // Filtra sin distinguir mayúsculas y conserva el filtro anterior de categorías.
  function agregar(evento) { // Maneja el evento dentro del componente dueño de la lista.
    evento.preventDefault() // Evita que el navegador recargue la página.
    setAviso('') // Limpia la confirmación anterior antes de validar.
    if (!nombre.trim() || nombre.trim().length > 120) { setError('El nombre es obligatorio y admite hasta 120 caracteres.'); return } // Respeta el nombre requerido y su longitud en el modelo.
    if (!Number.isFinite(Number(precio)) || Number(precio) <= 0) { setError('El precio debe ser mayor que cero.'); return } // Reproduce ProductoSerializer.validate_precio de la Semana 8.
    if (!/^\d+(\.\d{1,2})?$/.test(precio) || Number(precio) > 99999999.99) { setError('El precio admite hasta 8 enteros y 2 decimales.'); return } // Respeta DecimalField de Django.
    if (!/^\d+$/.test(stock) || !Number.isSafeInteger(Number(stock)) || Number(stock) > 2147483647) { setError('El stock debe ser un entero no negativo válido.'); return } // Respeta PositiveIntegerField sin aceptar valores vacíos.
    const nuevo = { id: Math.max(0, ...productos.map(p => p.id)) + 1, nombre: nombre.trim(), precio: Number(precio).toFixed(2), stock: Number(stock), descripcion: 'Registro local', categoria: categorias[0].id, categoria_nombre: categorias[0].nombre } // Crea un identificador estable y conserva los campos del serializer.
    setProductos(actuales => [...actuales, nuevo]) // Agrega mediante un arreglo nuevo, sin push ni mutaciones.
    setNombre(''); setPrecio(''); setStock(''); setError(''); setBusqueda(''); setCategoria('') // Limpia campos y filtros para mostrar el registro agregado.
    setAviso(`Producto ${nuevo.nombre} agregado a la lista local.`) // Confirma que el cambio vive solo en React.
  } // Finaliza el manejador local sin pasar funciones entre componentes.
  return <div><div className="filters"><label>Buscar producto<input type="search" value={busqueda} onChange={e => setBusqueda(e.target.value)} /></label><label>Categoría<select value={categoria} onChange={e => setCategoria(e.target.value)}><option value="">Todas</option>{categorias.map(c => <option key={c.id} value={c.id}>{c.nombre}</option>)}</select></label><button type="button" onClick={() => { setBusqueda(''); setCategoria('') }}>Limpiar filtros</button></div><p>{visibles.length} resultados · {productos.reduce((s, p) => s + p.stock, 0)} unidades</p>{visibles.length === 0 ? <p className="empty">No hay registros</p> : visibles.map(p => <ProductoCard key={p.id} {...p} />)}<form noValidate onSubmit={agregar}><h3>Nuevo producto</h3><div className="form-grid"><label>Nombre<input value={nombre} onChange={e => setNombre(e.target.value)} /></label><label>Precio<input type="number" step="0.01" value={precio} onChange={e => setPrecio(e.target.value)} /></label><label>Stock<input type="number" step="1" value={stock} onChange={e => setStock(e.target.value)} /></label></div><p>Se asigna a {categorias[0].nombre}. Los datos se conservan hasta recargar la página.</p>{error && <p role="alert">{error}</p>}{aviso && <p role="status">{aviso}</p>}<button type="submit">Agregar producto</button></form></div> // Renderiza listas con key, campos controlados y el formulario con validación visible.
} // Finaliza la lista interactiva.
