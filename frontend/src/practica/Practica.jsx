import { useCallback, useState } from 'react';
import productos from './datos.js';
import Catalogo from './Catalogo.jsx';
import Carrito from './Carrito.jsx';
import Buscador from './Buscador.jsx';
import Aviso from './Aviso.jsx';

export default function Practica() {
  const [lineas, setLineas] = useState([]);
  const [busqueda, setBusqueda] = useState('');
  const [mensaje, setMensaje] = useState('');
  const cerrarAviso = useCallback(() => setMensaje(''), []);

  function agregarAlCarrito(producto) {
    console.log(producto.nombre);
    setLineas((actuales) => {
      const existe = actuales.some((linea) => linea.id === producto.id);
      if (existe) {
        return actuales.map((linea) => (linea.id === producto.id ? { ...linea, cantidad: linea.cantidad + 1 } : linea));
      }
      return [...actuales, { id: producto.id, nombre: producto.nombre, precio: producto.precio, cantidad: 1 }];
    });
    setMensaje(producto.nombre);
  }

  function quitarLinea(id) { setLineas((actuales) => actuales.filter((linea) => linea.id !== id)); }
  function vaciarCarrito() { setLineas([]); }

  const filtrados = productos.filter((producto) => producto.nombre.toLocaleLowerCase('es').includes(busqueda.trim().toLocaleLowerCase('es')));

  return (
    <section className="page-wrap">
      <div className="page-heading">
        <div><p className="eyebrow">PRÁCTICA 01 · COMUNICACIÓN PADRE-HIJO</p><h1>Un café a tu manera.</h1><p className="subtitle">Elige algo rico y arma tu pedido. Tu carrito te acompaña.</p></div>
        <div className="heading-art" aria-hidden="true">☕</div>
      </div>
      <div className="practice-layout">
        <div className="catalog-column">
          <div className="section-bar"><div><p className="eyebrow">HECHO PARA DISFRUTAR</p><h2>El menú</h2></div><span className="count-pill">{filtrados.length} opciones</span></div>
          <Buscador valor={busqueda} onCambiar={setBusqueda} />
          <Catalogo productos={filtrados} onAgregar={agregarAlCarrito} />
        </div>
        <Carrito lineas={lineas} onQuitar={quitarLinea} onVaciar={vaciarCarrito} />
      </div>
      {mensaje && <Aviso mensaje={mensaje} onCerrar={cerrarAviso} />}
    </section>
  );
}
