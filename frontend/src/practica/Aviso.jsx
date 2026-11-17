import { useEffect } from 'react';

export default function Aviso({ mensaje, onCerrar }) {
  useEffect(() => {
    const temporizador = setTimeout(onCerrar, 3000);
    return () => clearTimeout(temporizador);
  }, [mensaje, onCerrar]);

  return <div className="toast" role="status"><span className="toast-check">✓</span><span><strong>Agregado al carrito</strong><small>{mensaje}</small></span><button onClick={onCerrar} aria-label="Cerrar aviso">×</button></div>;
}
