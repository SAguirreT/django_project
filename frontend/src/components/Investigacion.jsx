import Tarjeta from './Tarjeta.jsx' // Reutiliza el contenedor con children.
import ListaProductos from './ListaProductos.jsx' // Reutiliza la lista con estado propio para la investigación.
import VentaCard from './VentaCard.jsx' // Reutiliza el modelo intermedio anidado.
export default function Investigacion({ productos, categorias, ventas }) { // Recibe las mismas entidades de la investigación documentada en Semana 9.
  return <div id="investigacion"><Tarjeta titulo="Parte 2 · Investigación propia"><p>Categoria, Producto, Proveedor, Cliente y Venta; PerfilCliente (1:1) y DetalleVenta (intermedio M:N). Se reutilizan los datos originales de FarmaPoint.</p><ListaProductos iniciales={productos} categorias={categorias} /></Tarjeta><h2>Modelo intermedio · DetalleVenta</h2><div className="sales">{ventas.map(v => <VentaCard key={v.id} {...v} />)}</div></div> // Presenta una segunda lista independiente y su relación anidada sin inventar entidades.
} // Finaliza la sección de investigación propia.
