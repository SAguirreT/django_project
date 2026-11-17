import { useEffect, useMemo, useState } from 'react';
import api from '../api.js';
import BuscadorProductos from './BuscadorProductos.jsx';
import FormularioProducto from './FormularioProducto.jsx';
import ListaProductos from './ListaProductosApi.jsx';
import ResumenProductos from './ResumenProductos.jsx';

function mensajeDeError(error) {
  const data = error.response?.data;
  if (error.response?.status === 404) return 'El producto ya no existe o fue eliminado.';
  if (data && typeof data === 'object') {
    const mensajes = Object.entries(data).flatMap(([campo, valor]) =>
      (Array.isArray(valor) ? valor : [valor]).map((detalle) => `${campo}: ${detalle}`),
    );
    if (mensajes.length) return mensajes.join(' ');
  }
  return error.message || 'Ocurrió un error al comunicarse con la API.';
}

export default function PanelProductos() {
  const [productos, setProductos] = useState([]);
  const [categorias, setCategorias] = useState([]);
  const [busqueda, setBusqueda] = useState('');
  const [disponible, setDisponible] = useState('');
  const [cargando, setCargando] = useState(true);
  const [guardando, setGuardando] = useState(false);
  const [error, setError] = useState('');
  const [errorCategorias, setErrorCategorias] = useState('');
  const [errorFormulario, setErrorFormulario] = useState('');
  const [productoEditar, setProductoEditar] = useState(null);

  useEffect(() => {
    let cancelado = false;
    api.get('/categorias/').then((respuesta) => {
      if (!cancelado) setCategorias(respuesta.data);
    }).catch((fallo) => {
      if (!cancelado) {
        console.error('No se pudieron cargar las categorías:', fallo);
        setErrorCategorias('No se pudieron cargar las categorías. Comprueba que Django esté activo.');
      }
    });
    return () => { cancelado = true; };
  }, []);

  useEffect(() => {
    const controlador = new AbortController();
    async function cargarProductos() {
      setCargando(true);
      setError('');
      try {
        const params = {};
        if (busqueda.trim()) params.search = busqueda.trim();
        if (disponible) params.disponible = disponible;
        const respuesta = await api.get('/productos/', { params, signal: controlador.signal });
        setProductos(respuesta.data);
      } catch (fallo) {
        if (!controlador.signal.aborted) {
          console.error('No se pudo cargar la lista de productos:', fallo);
          setError('No se pudo cargar la lista.');
        }
      } finally {
        if (!controlador.signal.aborted) setCargando(false);
      }
    }
    cargarProductos();
    return () => controlador.abort();
  }, [busqueda, disponible]);

  useEffect(() => {
    document.title = `Productos (${productos.length}) — FarmaPoint`;
  }, [productos.length]);

  const stockTotal = useMemo(() => productos.reduce((total, producto) => total + Number(producto.stock), 0), [productos]);
  const disponiblesTotal = productos.filter((producto) => Number(producto.stock) > 0).length;

  async function guardar(productoNuevo) {
    setGuardando(true);
    setErrorFormulario('');
    try {
      if (productoEditar) {
        const respuesta = await api.patch(`/productos/${productoEditar.id}/`, productoNuevo);
        setProductos((actuales) => actuales.map((producto) => producto.id === productoEditar.id ? respuesta.data : producto));
      } else {
        const respuesta = await api.post('/productos/', productoNuevo);
        setProductos((actuales) => [...actuales, respuesta.data]);
      }
      setProductoEditar(null);
      return true;
    } catch (fallo) {
      console.error('No se pudo guardar el producto:', fallo.response?.data ?? fallo);
      setErrorFormulario(mensajeDeError(fallo));
      return false;
    } finally {
      setGuardando(false);
    }
  }

  async function eliminar(id, nombre) {
    if (!window.confirm(`¿Eliminar el producto “${nombre}”?`)) return;
    setError('');
    try {
      await api.delete(`/productos/${id}/`);
      setProductos((actuales) => actuales.filter((producto) => producto.id !== id));
    } catch (fallo) {
      console.error('No se pudo eliminar el producto:', fallo.response?.data ?? fallo);
      setError(mensajeDeError(fallo));
    }
  }

  return (
    <section className="page-wrap">
      <div className="page-heading panel-hero">
        <div><p className="eyebrow">FARMAPOINT · INVENTARIO</p><h1>Productos bajo control.</h1><p className="subtitle">Una vista clara de tu inventario, para que todo esté en su lugar.</p></div>
        <div className="heading-art pharmacy-art" aria-hidden="true">＋</div>
      </div>
      <ResumenProductos productos={productos} stockTotal={stockTotal} disponiblesTotal={disponiblesTotal} />
      <div className="management-layout">
        <section className="inventory-panel">
          <div className="section-bar inventory-title"><div><p className="eyebrow">CATÁLOGO FARMACÉUTICO</p><h2>Inventario <span className="count-pill">{productos.length}</span></h2></div>
            <div className="filters"><BuscadorProductos valor={busqueda} onCambiar={setBusqueda} /><select aria-label="Filtrar disponibilidad" value={disponible} onChange={(evento) => setDisponible(evento.target.value)}><option value="">Todas las existencias</option><option value="true">Con stock</option><option value="false">Agotados</option></select></div>
          </div>
          {error && <div className="api-message error-message" role="alert">{error}</div>}
          {cargando ? <p className="api-message loading-message">Cargando...</p> : !error && <ListaProductos productos={productos} onEliminar={eliminar} onEditar={(producto) => { setProductoEditar(producto); setErrorFormulario(''); }} />}
        </section>
        <FormularioProducto key={productoEditar?.id ?? 'nuevo'} onGuardar={guardar} productoEditar={productoEditar} categorias={categorias} guardando={guardando} errorApi={errorFormulario || errorCategorias} onCancelar={() => { setProductoEditar(null); setErrorFormulario(''); }} />
      </div>
    </section>
  );
}
