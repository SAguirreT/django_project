import { useState } from 'react';

const vacio = { nombre: '', descripcion: '', precio: '', stock: '', categoria: '' };

function valoresIniciales(productoEditar) {
  if (!productoEditar) return vacio;
  return {
    nombre: productoEditar.nombre ?? '',
    descripcion: productoEditar.descripcion ?? '',
    precio: productoEditar.precio ?? '',
    stock: String(productoEditar.stock ?? ''),
    categoria: String(productoEditar.categoria ?? ''),
  };
}

export default function FormularioProducto({ onGuardar, productoEditar, categorias, guardando, errorApi, onCancelar }) {
  const [valores, setValores] = useState(() => valoresIniciales(productoEditar));
  const [error, setError] = useState('');

  function cambiar(evento) { setValores((actuales) => ({ ...actuales, [evento.target.name]: evento.target.value })); }
  async function enviar(evento) {
    evento.preventDefault();
    if (!valores.nombre.trim()) { setError('Escribe el nombre del producto.'); return; }
    if (!valores.precio || !Number.isFinite(Number(valores.precio))) { setError('Ingresa un precio numérico.'); return; }
    if (valores.stock !== '' && (!Number.isInteger(Number(valores.stock)) || Number(valores.stock) < 0)) { setError('El stock debe ser un entero igual o mayor que cero.'); return; }
    if (!valores.categoria) { setError('Selecciona una categoría existente.'); return; }
    const guardado = await onGuardar({ ...valores, nombre: valores.nombre.trim(), precio: Number(valores.precio).toFixed(2), stock: Number(valores.stock || 0), categoria: Number(valores.categoria) });
    if (guardado) { setValores(vacio); setError(''); }
  }

  return <aside className="form-panel"><div className="form-heading"><span className="form-icon">＋</span><div><p className="eyebrow">{productoEditar ? 'EDITAR REGISTRO' : 'NUEVO REGISTRO'}</p><h2>{productoEditar ? 'Editar producto' : 'Agregar producto'}</h2></div></div>
    <p className="form-intro">Completa los datos para {productoEditar ? 'actualizar' : 'sumar'} el inventario.</p>
    <form onSubmit={enviar} noValidate>
      <label className="field-label">Nombre del producto<input name="nombre" value={valores.nombre} onChange={cambiar} placeholder="Ej. Ibuprofeno 400 mg" /></label>
      <label className="field-label">Descripción <span className="optional">OPCIONAL</span><textarea name="descripcion" value={valores.descripcion} onChange={cambiar} rows="2" placeholder="Presentación o detalle breve" /></label>
      <div className="field-pair"><label className="field-label">Precio (S/)<input name="precio" type="number" min="0.01" step="0.01" value={valores.precio} onChange={cambiar} placeholder="0.00" /></label><label className="field-label">Stock<input name="stock" type="number" min="0" step="1" value={valores.stock} onChange={cambiar} placeholder="0" /></label></div>
      <label className="field-label">Categoría<select name="categoria" value={valores.categoria} onChange={cambiar}><option value="">Selecciona una categoría</option>{categorias.map((categoria) => <option key={categoria.id} value={categoria.id}>{categoria.nombre}</option>)}</select></label>
      {error && <p className="form-error" role="alert">{error}</p>}
      {errorApi && <p className="form-error" role="alert">{errorApi}</p>}
      <button className="save-button" type="submit" disabled={guardando}>{guardando ? 'Guardando…' : productoEditar ? 'Guardar cambios' : 'Agregar al inventario'} <span>→</span></button>
      {productoEditar && <button className="cancel-button" type="button" onClick={onCancelar}>Cancelar edición</button>}
    </form>
    <p className="form-footnote"><span>✦</span> Selecciona una categoría existente; la API recibe su ID. Descripción, stock y precio siguen los campos del modelo Producto.</p>
  </aside>;
}
