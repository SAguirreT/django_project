export default function Buscador({ valor, onCambiar }) {
  return <label className="search-box"><span aria-hidden="true">⌕</span><input value={valor} onChange={(evento) => onCambiar(evento.target.value)} placeholder="Busca en el menú..." aria-label="Buscar productos" />{valor && <button type="button" onClick={() => onCambiar('')} aria-label="Limpiar búsqueda">×</button>}</label>;
}
