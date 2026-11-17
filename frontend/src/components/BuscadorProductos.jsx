export default function BuscadorProductos({ valor, onCambiar }) {
  return <label className="search-box inventory-search"><span aria-hidden="true">⌕</span><input value={valor} onChange={(evento) => onCambiar(evento.target.value)} placeholder="Buscar producto..." aria-label="Buscar por nombre de producto" />{valor && <button type="button" onClick={() => onCambiar('')} aria-label="Limpiar búsqueda">×</button>}</label>;
}
