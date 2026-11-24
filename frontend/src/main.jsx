import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import './styles.css'
import App from './App.jsx'
import ProductosPage from './pages/ProductosPage.jsx'
import VentasPage from './pages/VentasPage.jsx'

const pathname = window.location.pathname.replace(/\/$/, '')
const venta = pathname.match(/^\/ventas(?:\/(\d+))?$/)
const pantalla = pathname === '/cafeteria/productos'
  ? <ProductosPage />
  : venta
    ? <VentasPage id={venta[1]} />
    : <App />

createRoot(document.getElementById('root')).render(
  <StrictMode>
    {pantalla}
  </StrictMode>,
)
