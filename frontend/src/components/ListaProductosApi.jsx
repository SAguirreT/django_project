import ProductoFila from './ProductoFila.jsx';

export default function ListaProductos({ productos, onEliminar, onEditar }) {
  if (productos.length === 0) return <div className="empty-search inventory-empty"><span>⌕</span><strong>No hay productos que coincidan</strong><p>Prueba con otro nombre o agrega un producto nuevo.</p></div>;
  return <div className="table-wrap"><table className="product-table"><thead><tr><th>PRODUCTO</th><th>CATEGORÍA</th><th>PRECIO</th><th>STOCK</th><th>ACCIONES</th></tr></thead><tbody>{productos.map((producto) => <ProductoFila key={producto.id} producto={producto} onEliminar={onEliminar} onEditar={onEditar} />)}</tbody></table></div>;
}
