// Conserva exactamente los datos locales de la Semana 9, sin consumir la API.
export const productos = [ // Conserva el campo o la estructura del registro original.
  { // Conserva el campo o la estructura del registro original.
    "id": 1, // Conserva el campo o la estructura del registro original.
    "nombre": "Paracetamol 500 mg", // Conserva el campo o la estructura del registro original.
    "descripcion": "Caja de 10 tabletas", // Conserva el campo o la estructura del registro original.
    "precio": "5.50", // Conserva el campo o la estructura del registro original.
    "stock": 24, // Conserva el campo o la estructura del registro original.
    "categoria": 1, // Conserva el campo o la estructura del registro original.
    "categoria_nombre": "Analgésicos" // Conserva el campo o la estructura del registro original.
  }, // Conserva el campo o la estructura del registro original.
  { // Conserva el campo o la estructura del registro original.
    "id": 2, // Conserva el campo o la estructura del registro original.
    "nombre": "Ibuprofeno 400 mg", // Conserva el campo o la estructura del registro original.
    "descripcion": "Caja de 10 cápsulas", // Conserva el campo o la estructura del registro original.
    "precio": "8.90", // Conserva el campo o la estructura del registro original.
    "stock": 0, // Conserva el campo o la estructura del registro original.
    "categoria": 1, // Conserva el campo o la estructura del registro original.
    "categoria_nombre": "Analgésicos" // Conserva el campo o la estructura del registro original.
  }, // Conserva el campo o la estructura del registro original.
  { // Conserva el campo o la estructura del registro original.
    "id": 3, // Conserva el campo o la estructura del registro original.
    "nombre": "Alcohol 70%", // Conserva el campo o la estructura del registro original.
    "descripcion": "Frasco de 250 ml", // Conserva el campo o la estructura del registro original.
    "precio": "6.50", // Conserva el campo o la estructura del registro original.
    "stock": 3, // Conserva el campo o la estructura del registro original.
    "categoria": 2, // Conserva el campo o la estructura del registro original.
    "categoria_nombre": "Higiene" // Conserva el campo o la estructura del registro original.
  }, // Conserva el campo o la estructura del registro original.
  { // Conserva el campo o la estructura del registro original.
    "id": 4, // Conserva el campo o la estructura del registro original.
    "nombre": "Vitamina C", // Conserva el campo o la estructura del registro original.
    "descripcion": "Tubo de 10 tabletas", // Conserva el campo o la estructura del registro original.
    "precio": "12.00", // Conserva el campo o la estructura del registro original.
    "stock": 12, // Conserva el campo o la estructura del registro original.
    "categoria": 3, // Conserva el campo o la estructura del registro original.
    "categoria_nombre": "Vitaminas" // Conserva el campo o la estructura del registro original.
  }, // Conserva el campo o la estructura del registro original.
  { // Conserva el campo o la estructura del registro original.
    "id": 5, // Conserva el campo o la estructura del registro original.
    "nombre": "Mascarillas", // Conserva el campo o la estructura del registro original.
    "descripcion": "Paquete de 5 unidades", // Conserva el campo o la estructura del registro original.
    "precio": "4.90", // Conserva el campo o la estructura del registro original.
    "stock": 2, // Conserva el campo o la estructura del registro original.
    "categoria": 2, // Conserva el campo o la estructura del registro original.
    "categoria_nombre": "Higiene" // Conserva el campo o la estructura del registro original.
  } // Conserva el campo o la estructura del registro original.
] // Conserva el campo o la estructura del registro original.
export const categorias = [ // Conserva el campo o la estructura del registro original.
  { // Conserva el campo o la estructura del registro original.
    "id": 1, // Conserva el campo o la estructura del registro original.
    "nombre": "Analgésicos", // Conserva el campo o la estructura del registro original.
    "descripcion": "Alivio del dolor" // Conserva el campo o la estructura del registro original.
  }, // Conserva el campo o la estructura del registro original.
  { // Conserva el campo o la estructura del registro original.
    "id": 2, // Conserva el campo o la estructura del registro original.
    "nombre": "Higiene", // Conserva el campo o la estructura del registro original.
    "descripcion": "Cuidado y protección personal" // Conserva el campo o la estructura del registro original.
  }, // Conserva el campo o la estructura del registro original.
  { // Conserva el campo o la estructura del registro original.
    "id": 3, // Conserva el campo o la estructura del registro original.
    "nombre": "Vitaminas", // Conserva el campo o la estructura del registro original.
    "descripcion": "Complementos nutricionales" // Conserva el campo o la estructura del registro original.
  } // Conserva el campo o la estructura del registro original.
] // Conserva el campo o la estructura del registro original.
export const ventas = [ // Conserva el campo o la estructura del registro original.
  { // Conserva el campo o la estructura del registro original.
    "id": 101, // Conserva el campo o la estructura del registro original.
    "cliente": { // Conserva el campo o la estructura del registro original.
      "id": 1, // Conserva el campo o la estructura del registro original.
      "nombre": "Ana Torres", // Conserva el campo o la estructura del registro original.
      "documento": "10000101", // Conserva el campo o la estructura del registro original.
      "telefono": "900000001", // Conserva el campo o la estructura del registro original.
      "correo": "demo@example.com" // Conserva el campo o la estructura del registro original.
    }, // Conserva el campo o la estructura del registro original.
    "fecha": "2026-10-17T09:30:00-05:00", // Conserva el campo o la estructura del registro original.
    "total": "27.90", // Conserva el campo o la estructura del registro original.
    "detalles": [ // Conserva el campo o la estructura del registro original.
      { // Conserva el campo o la estructura del registro original.
        "id": 1010, // Conserva el campo o la estructura del registro original.
        "producto": { // Conserva el campo o la estructura del registro original.
          "id": 1, // Conserva el campo o la estructura del registro original.
          "nombre": "Paracetamol 500 mg", // Conserva el campo o la estructura del registro original.
          "descripcion": "Caja de 10 tabletas", // Conserva el campo o la estructura del registro original.
          "precio": "5.50", // Conserva el campo o la estructura del registro original.
          "stock": 24, // Conserva el campo o la estructura del registro original.
          "categoria": 1, // Conserva el campo o la estructura del registro original.
          "categoria_nombre": "Analgésicos" // Conserva el campo o la estructura del registro original.
        }, // Conserva el campo o la estructura del registro original.
        "cantidad": 2, // Conserva el campo o la estructura del registro original.
        "precio_unitario": "5.50", // Conserva el campo o la estructura del registro original.
        "subtotal": "11.00" // Conserva el campo o la estructura del registro original.
      }, // Conserva el campo o la estructura del registro original.
      { // Conserva el campo o la estructura del registro original.
        "id": 1011, // Conserva el campo o la estructura del registro original.
        "producto": { // Conserva el campo o la estructura del registro original.
          "id": 4, // Conserva el campo o la estructura del registro original.
          "nombre": "Vitamina C", // Conserva el campo o la estructura del registro original.
          "descripcion": "Tubo de 10 tabletas", // Conserva el campo o la estructura del registro original.
          "precio": "12.00", // Conserva el campo o la estructura del registro original.
          "stock": 12, // Conserva el campo o la estructura del registro original.
          "categoria": 3, // Conserva el campo o la estructura del registro original.
          "categoria_nombre": "Vitaminas" // Conserva el campo o la estructura del registro original.
        }, // Conserva el campo o la estructura del registro original.
        "cantidad": 1, // Conserva el campo o la estructura del registro original.
        "precio_unitario": "12.00", // Conserva el campo o la estructura del registro original.
        "subtotal": "12.00" // Conserva el campo o la estructura del registro original.
      }, // Conserva el campo o la estructura del registro original.
      { // Conserva el campo o la estructura del registro original.
        "id": 1012, // Conserva el campo o la estructura del registro original.
        "producto": { // Conserva el campo o la estructura del registro original.
          "id": 5, // Conserva el campo o la estructura del registro original.
          "nombre": "Mascarillas", // Conserva el campo o la estructura del registro original.
          "descripcion": "Paquete de 5 unidades", // Conserva el campo o la estructura del registro original.
          "precio": "4.90", // Conserva el campo o la estructura del registro original.
          "stock": 2, // Conserva el campo o la estructura del registro original.
          "categoria": 2, // Conserva el campo o la estructura del registro original.
          "categoria_nombre": "Higiene" // Conserva el campo o la estructura del registro original.
        }, // Conserva el campo o la estructura del registro original.
        "cantidad": 1, // Conserva el campo o la estructura del registro original.
        "precio_unitario": "4.90", // Conserva el campo o la estructura del registro original.
        "subtotal": "4.90" // Conserva el campo o la estructura del registro original.
      } // Conserva el campo o la estructura del registro original.
    ] // Conserva el campo o la estructura del registro original.
  }, // Conserva el campo o la estructura del registro original.
  { // Conserva el campo o la estructura del registro original.
    "id": 102, // Conserva el campo o la estructura del registro original.
    "cliente": { // Conserva el campo o la estructura del registro original.
      "id": 2, // Conserva el campo o la estructura del registro original.
      "nombre": "Luis Pérez", // Conserva el campo o la estructura del registro original.
      "documento": "10000102", // Conserva el campo o la estructura del registro original.
      "telefono": "900000001", // Conserva el campo o la estructura del registro original.
      "correo": "demo@example.com" // Conserva el campo o la estructura del registro original.
    }, // Conserva el campo o la estructura del registro original.
    "fecha": "2026-10-17T09:30:00-05:00", // Conserva el campo o la estructura del registro original.
    "total": "24.00", // Conserva el campo o la estructura del registro original.
    "detalles": [ // Conserva el campo o la estructura del registro original.
      { // Conserva el campo o la estructura del registro original.
        "id": 1020, // Conserva el campo o la estructura del registro original.
        "producto": { // Conserva el campo o la estructura del registro original.
          "id": 4, // Conserva el campo o la estructura del registro original.
          "nombre": "Vitamina C", // Conserva el campo o la estructura del registro original.
          "descripcion": "Tubo de 10 tabletas", // Conserva el campo o la estructura del registro original.
          "precio": "12.00", // Conserva el campo o la estructura del registro original.
          "stock": 12, // Conserva el campo o la estructura del registro original.
          "categoria": 3, // Conserva el campo o la estructura del registro original.
          "categoria_nombre": "Vitaminas" // Conserva el campo o la estructura del registro original.
        }, // Conserva el campo o la estructura del registro original.
        "cantidad": 2, // Conserva el campo o la estructura del registro original.
        "precio_unitario": "12.00", // Conserva el campo o la estructura del registro original.
        "subtotal": "24.00" // Conserva el campo o la estructura del registro original.
      } // Conserva el campo o la estructura del registro original.
    ] // Conserva el campo o la estructura del registro original.
  } // Conserva el campo o la estructura del registro original.
] // Conserva el campo o la estructura del registro original.
