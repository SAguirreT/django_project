import DetalleItem from './DetalleItem.jsx' // Compone cada venta con elementos de detalle reutilizables.
export default function VentaCard({ id, cliente, fecha, detalles }) { // Desestructura las props de VentaReadSerializer.
  const total = detalles.reduce((suma, d) => suma + d.cantidad * Math.round(Number(d.precio_unitario) * 100), 0) / 100 // Suma céntimos para evitar errores de coma flotante.
  return <article className="panel sale" data-testid="venta"><h3>Venta #{id}</h3><p>{cliente.nombre} · {new Date(fecha).toLocaleDateString('es-PE')}</p><ul>{detalles.map(d => <DetalleItem key={d.id} nombre={d.producto.nombre} cantidad={d.cantidad} precioUnitario={d.precio_unitario} />)}</ul><div className="total"><span>Total calculado</span><strong>S/ {total.toFixed(2)}</strong></div></article> // Adapta precio_unitario a precioUnitario y representa Venta 1:N DetalleVenta.
} // Finaliza la venta sin alterar el objeto recibido.
