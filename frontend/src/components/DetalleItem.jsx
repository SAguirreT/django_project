export default function DetalleItem({ nombre, cantidad, precioUnitario }) { // Recibe nombres adaptados desde los campos anidados de la API.
  return <li><span>{nombre}<small>{cantidad} × S/ {Number(precioUnitario).toFixed(2)}</small></span><strong>S/ {(cantidad * Math.round(Number(precioUnitario) * 100) / 100).toFixed(2)}</strong></li> // Muestra el subtotal calculado en céntimos.
} // Finaliza el elemento de la relación anidada.
