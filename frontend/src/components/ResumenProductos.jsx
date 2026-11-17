export default function ResumenProductos({ productos, stockTotal, disponiblesTotal }) {
  const stock = stockTotal ?? productos.reduce((acumulado, producto) => acumulado + Number(producto.stock), 0);
  const disponibles = disponiblesTotal ?? productos.filter((producto) => producto.stock > 0).length;
  return <div className="summary-grid">
    <article className="summary-card"><span className="summary-icon lilac">▦</span><div><small>Productos registrados</small><strong>{productos.length}</strong></div><span className="summary-trend">en catálogo</span></article>
    <article className="summary-card"><span className="summary-icon mint">↗</span><div><small>Unidades en stock</small><strong>{stock.toLocaleString('es')}</strong></div><span className="summary-trend">unidades</span></article>
    <article className="summary-card"><span className="summary-icon peach">✓</span><div><small>Con disponibilidad</small><strong>{disponibles}</strong></div><span className="summary-trend">productos</span></article>
  </div>;
}
