import { useEffect, useState } from 'react';
import api from '../api';

export default function VentasPage({ id }) {
  const [resultado, setResultado] = useState(null);
  const [error, setError] = useState('');

  useEffect(() => {
    const solicitud = new AbortController();
    const ruta = id ? `ventas/${id}/` : 'ventas/';
    api.get(ruta, { signal: solicitud.signal })
      .then(({ data }) => setResultado(data))
      .catch((fallo) => {
        if (solicitud.signal.aborted) return;
        setError(fallo.response?.status === 404 ? 'La venta no existe.' : 'No se pudieron cargar las ventas.');
      });
    return () => solicitud.abort();
  }, [id]);

  return (
    <main className="lab14-page">
      <a href={id ? '/ventas' : '/'}>{id ? 'Volver a ventas' : 'Volver al panel'}</a>
      <h1>{id ? `Detalle de venta #${id}` : 'Ventas de FarmaPoint'}</h1>
      {error && <p role="alert">{error}</p>}
      {!error && resultado === null && <p role="status">Cargando ventas…</p>}
      {resultado && (id ? <DetalleVenta venta={resultado} /> : <ListaVentas ventas={resultado} />)}
    </main>
  );
}

function ListaVentas({ ventas }) {
  if (ventas.length === 0) return <p>No hay ventas registradas.</p>;

  return (
    <ul>
      {ventas.map((venta) => (
        <li key={venta.id}>
          <a href={`/ventas/${venta.id}`}>Venta #{venta.id}</a>
          {' '}· {venta.cliente.nombre} · S/ {venta.total}
        </li>
      ))}
    </ul>
  );
}

function DetalleVenta({ venta }) {
  return (
    <>
      <p>Cliente {venta.cliente.nombre}</p>
      <p>Fecha {new Date(venta.fecha).toLocaleString('es-PE')}</p>
      <ul>
        {venta.detalles.map((linea) => (
          <li key={linea.id}>
            {linea.producto.nombre} · {linea.cantidad} × S/ {linea.precio_unitario}
          </li>
        ))}
      </ul>
      <p><strong>Total S/ {venta.total}</strong></p>
    </>
  );
}
