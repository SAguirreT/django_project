export default function BuscadorProductos({ valor, onCambiar }) {
  //Cuando el usuario escribe, BuscadorProductos.jsx, 
  // línea 2 llama esa función para actualizar la búsqueda.


  //Hijo → padre (callback). Cuando escribes, BuscadorProductos 
  // llama a onCambiar con el texto nuevo. 
  // Esa función es setBusqueda, que actualiza la búsqueda en el padre.
  return <label className="search-box inventory-search"><span aria-hidden="true">⌕</span><input value={valor} onChange={(evento) => onCambiar(evento.target.value)} placeholder="Buscar producto..." aria-label="Buscar por nombre de producto" />{valor && <button type="button" onClick={() => onCambiar('')} aria-label="Limpiar búsqueda">×</button>}</label>;
}
