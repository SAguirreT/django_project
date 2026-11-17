export default function ProductoCard({ producto, onAgregar }) {
  return (
    <article className="menu-card">
      <div className={`food-art food-${producto.id}`} aria-hidden="true"><span>{['☕', '☕', '🍰', '🍊', '🍞'][producto.id - 1]}</span></div>
      <div className="menu-card-body">
        <div className="card-title-row"><h3>{producto.nombre}</h3><span className="price">S/ {Number(producto.precio).toFixed(2)}</span></div>
        <div className="stock-row"><span className={producto.stock === 0 ? 'stock-dot sold' : 'stock-dot'} />{producto.stock === 0 ? 'Agotado' : `${producto.stock} disponibles`}</div>
        <button className="add-button" disabled={producto.stock === 0} onClick={() => onAgregar(producto)}><span>＋</span> Agregar</button>
      </div>
    </article>
  );
}
