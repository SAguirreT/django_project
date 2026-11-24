import { useEffect, useState } from 'react';
import api from '../practica/cafeteria/api';

export default function ProductosPage() {
  const [resultado, setResultado] = useState(null);
  const [error, setError] = useState(false);

  useEffect(() => {
    const solicitud = new AbortController();
    api.get('productos/', { signal: solicitud.signal })
      .then(({ data }) => setResultado(data))
      .catch(() => { if (!solicitud.signal.aborted) setError(true); });
    return () => solicitud.abort();
  }, []);

  return (
    <main className="lab14-page">
      <a href="/">Volver al panel</a>
      <h1>Catálogo de la cafetería</h1>
      {error && <p role="alert">No se pudo cargar el catálogo.</p>}
      {!error && resultado === null && <p role="status">Cargando productos…</p>}
      {resultado?.length === 0 && <p>El catálogo está vacío.</p>}
      <ul>
        {resultado?.map((producto) => (
          <li key={producto.id}>
            <strong>{producto.nombre}</strong> · {producto.categoria_nombre} · S/ {producto.precio}
            {' '}· {producto.activo ? `${producto.stock} en stock` : 'Inactivo'}
          </li>
        ))}
      </ul>
    </main>
  );
}
