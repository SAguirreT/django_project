import { useState } from 'react';
import Lab10App from './Lab10App.jsx';
import Practica from './practica/Practica.jsx';
import PanelProductos from './components/PanelProductos.jsx';

export default function App() {
  const [vista, setVista] = useState('productos');

  return (
    <div className="app-shell">
      <header className="topbar">
        <a className="brand" href="#inicio" aria-label="FarmaPoint inicio"><span className="brand-mark">✳</span> FarmaPoint</a>
        <nav className="nav-tabs" aria-label="Laboratorios">
          <button className={vista === 'productos' ? 'nav-tab active' : 'nav-tab'} onClick={() => setVista('productos')}>Productos · API</button>
          <button className={vista === 'practica' ? 'nav-tab active' : 'nav-tab'} onClick={() => setVista('practica')}>Catálogo · Lab 11</button>
          <button className={vista === 'lab10' ? 'nav-tab active' : 'nav-tab'} onClick={() => setVista('lab10')}>Inventario · Lab 10</button>
        </nav>
        <span className="local-badge"><i /> FarmaPoint</span>
      </header>
      {vista === 'productos' ? <PanelProductos /> : vista === 'practica' ? <Practica /> : <Lab10App />}
      {vista !== 'lab10' && <footer className="footer">FarmaPoint <span>·</span> Comunicación entre componentes y API</footer>}
    </div>
  );
}
