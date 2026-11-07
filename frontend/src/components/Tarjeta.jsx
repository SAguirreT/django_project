export default function Tarjeta({ titulo, children }) { // Recibe el título y el contenido anidado mediante props.
  return <section className="panel"><h2>{titulo}</h2>{children}</section> // Envuelve cualquier sección con el mismo estilo.
} // Finaliza el contenedor reutilizable.
