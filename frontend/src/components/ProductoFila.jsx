export default function ProductoFila({ producto, onEliminar, onEditar }) {
  return <tr>
    <td><div className="product-name-cell"><span className="product-avatar">{producto.nombre.charAt(0).toUpperCase()}</span><span><strong>{producto.nombre}</strong><small>{producto.descripcion || 'Sin descripción'}</small></span></div></td>
    <td><span className="category-chip">{producto.categoria}</span></td>
    <td className="table-price">S/ {Number(producto.precio).toFixed(2)}</td>
    <td><span className={producto.stock > 0 ? 'availability in-stock' : 'availability out-stock'}><i />{producto.stock > 0 ? `${producto.stock} unidades` : 'Agotado'}</span></td>
    <td><div className="row-actions"><button className="status-action" onClick={() => onEditar(producto)}>Editar</button><button className="delete-action" onClick={() => onEliminar(producto.id, producto.nombre)} aria-label={`Eliminar ${producto.nombre}`}>×</button></div></td>
  </tr>;
}
