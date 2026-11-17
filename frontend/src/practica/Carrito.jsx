import { useEffect } from 'react';

export default function Carrito({ lineas, onQuitar, onVaciar }) {
  const unidades = lineas.reduce((acumulado, linea) => acumulado + linea.cantidad, 0);
  const total = lineas.reduce((acumulado, linea) => acumulado + Number(linea.precio) * linea.cantidad, 0);

  useEffect(() => { document.title = `Carrito (${unidades}) — Cafetería`; }, [unidades]);

  return (
    <aside className="cart-panel">
      <div className="cart-heading"><div><p className="eyebrow">TU PEDIDO</p><h2>El carrito <span className="cart-count">{unidades}</span></h2></div><span className="cart-icon">♧</span></div>
      {lineas.length === 0 && <div className="cart-empty"><span className="empty-basket">⌑</span><strong>El carrito está vacío</strong><p>Las cosas buenas empiezan con un antojo.</p></div>}
      {lineas.length > 0 && <>
        <div className="cart-lines">{lineas.map((linea) => <div className="cart-line" key={linea.id}><div className="line-thumb">{linea.nombre.includes('Café') || linea.nombre.includes('Capuchino') ? '☕' : '🍰'}</div><div className="line-info"><strong>{linea.nombre}</strong><span>{linea.cantidad} × S/ {Number(linea.precio).toFixed(2)}</span></div><strong className="line-total">S/ {(Number(linea.precio) * linea.cantidad).toFixed(2)}</strong><button className="remove-line" onClick={() => onQuitar(linea.id)} aria-label={`Quitar ${linea.nombre}`}>×</button></div>)}</div>
        <div className="cart-subtotal"><span>Unidades</span><strong>{unidades}</strong></div>
        <div className="cart-total"><span>Total</span><strong>S/ {total.toFixed(2)}</strong></div>
        <button className="clear-button" onClick={onVaciar}>Vaciar carrito</button>
      </>}
      <div className="cart-note"><span>✦</span> Preparado con cariño, pedido a pedido.</div>
    </aside>
  );
}
