import ProductoCard from './ProductoCard.jsx';

export default function Catalogo({ productos, onAgregar }) {
  if (productos.length === 0) return <div className="empty-search"><span>⌕</span><strong>No hay productos que coincidan</strong><p>Prueba con otra búsqueda.</p></div>;
  return <div className="product-grid">{productos.map((producto) => <ProductoCard key={producto.id} producto={producto} onAgregar={onAgregar} />)}</div>;
}
