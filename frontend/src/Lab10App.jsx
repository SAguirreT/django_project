import './App.css' // Conserva la presentación adaptable del proyecto original.
import { productos, categorias, ventas } from './datos.js' // Recupera los mismos datos locales de la Semana 9.
import Tarjeta from './components/Tarjeta.jsx' // Importa el contenedor con children.
import ListaProductos from './components/ListaProductos.jsx' // Importa la lista, el buscador y el formulario.
import VentaCard from './components/VentaCard.jsx' // Importa la relación Venta y sus detalles.
import Investigacion from './components/Investigacion.jsx' // Importa la segunda parte con estado independiente.
export default function App() { // Declara la raíz con nombre en mayúscula.
  return <div className="app"><aside><div className="brand"><b>+</b> FarmaPoint</div><p>GESTIÓN DE FARMACIA</p><nav><a href="#inventario">Inventario</a><a href="#ventas">Ventas</a><a href="#investigacion">Investigación</a></nav><small>Datos locales · Laboratorio 10</small></aside><main><header><div><span className="eyebrow">COMPONENTES, ESTADO Y EVENTOS</span><h1>FarmaPoint</h1><p>Productos, reservas y ventas de tu farmacia.</p></div><span className="badge">Vista local</span></header><div id="inventario"><Tarjeta titulo="Parte 1 · Inventario de productos"><ListaProductos iniciales={productos} categorias={categorias} /></Tarjeta></div><section id="ventas"><h2>Detalle de ventas</h2><div className="sales">{ventas.map(v => <VentaCard key={v.id} {...v} />)}</div></section><Investigacion productos={productos} categorias={categorias} ventas={ventas} /><footer>FarmaPoint · Laboratorio 10 · SAguirreT</footer></main></div> // Organiza las dos partes con props de datos y claves estables, sin pasar callbacks.
} // Finaliza la aplicación.
