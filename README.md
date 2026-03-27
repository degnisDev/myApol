# MyApol

**MyApol** es una plataforma web (E-commerce / Catálogo) diseñada para ofrecer una experiencia visual premium, rápida y dinámica. Implementa una arquitectura Cliente-Servidor (API REST) estructurada con un diseño moderno y un completo panel administrativo.

## Funcionalidades Principales

- **Catálogo Dinámico e Interactivo**: Búsqueda en tiempo real y filtrado de productos por categorías.
- **Detalle de Producto**: Vista expandida de cada dispositivo consumiendo la API por ID de manera reactiva.
- **Sistema de Opiniones**: Los usuarios registrados pueden iniciar sesión y dejar comentarios públicos en tiempo real.
- **Panel Administrativo (CRUD)**: Acceso privado para gestionar (Crear, Leer, Actualizar y Eliminar) completamente el inventario de la tienda.
- **Seguridad Básica**: Autenticación de administrador y clientes basada en roles. Inyección de datos protegida con peticiones paramétricas.
- **Pasarela de Pagos (Checkout Pro)**: Integración con **Mercado Pago** para procesar transacciones seguras de manera dinámica desde el carrito de compras.

## Tecnologías Utilizadas

- **Frontend**: HTML5, CSS3, JavaScript (Vanilla), Bootstrap 5, Bootstrap Icons.
- **Backend**: Python 3, Flask (RESTful API).
- **Base de Datos**: SQLite (`database.db`).
- **Pasarela de Pagos**: SDK de **Mercado Pago** (Python & JavaScript).

## Estructura del Proyecto

```text
/
├── frontend/
│   ├── index.html         (Página principal / Catálogo público)
│   ├── detalle.html       (Vista individual de producto y comentarios)
│   ├── admin.html         (Panel Privado CRUD para gestionar tienda)
│   ├── login.html         (Página de acceso al Panel Administrativo)
│   ├── login_cliente.html (Página de acceso Público / Clientes)
│   ├── styles.css         (Diseño global premium oscuro y animaciones)
│   └── scripts.js         (Lógica principal de UI y consumo de la API)
│
└── backend/
    ├── app.py               (Servidor Flask Principal / API)
    ├── init_db.py           (Script creador y poblador automático de Base de Datos)
    ├── inyectar_imagenes.py (Script optimizador de Imágenes HD Hotlinking)
    └── database.db          (Base de datos local generada automáticamente)
```

## ¿Cómo ejecutar este proyecto? (Paso a Paso)

Para ejecutar este proyecto exitosamente, sigue los siguientes pasos:

### Paso 1: Requisitos Previos
Asegúrate de tener instalado [Python](https://www.python.org/downloads/) en tu computadora.

### Paso 2: Instalar Dependencias del Servidor Backend
Abre una terminal (símbolo del sistema o PowerShell) en la carpeta principal del proyecto e instala la librería **Flask** con este comando:
```bash
pip install flask
```

### Paso 3: Inicializar la Base de Datos
Para generar la base de datos `database.db` y llenarla con la información inicial de roles, categorías y 18 productos Apple, ejecuta este comando:
```bash
python backend/init_db.py
```
*(Opcionalmente, si deseas obtener imágenes fotorealistas en alta calidad de manera automática directo desde internet en tu base de datos, ejecuta también: `python backend/inyectar_imagenes.py`)*

### Paso 4: Levantar el Servidor Backend (La API)
Inicia la API (el motor de datos del catálogo) con el siguiente comando quedándote en la raíz del proyecto:
```bash
python backend/app.py
```
> Si te aparece un mensaje en la consola como `* Running on http://127.0.0.1:5000`, ¡felicidades, el servidor está vivo y escuchando peticiones! Deja esa pestaña de la terminal abierta ejecutándose en segundo plano.

### Paso 5: Abrir el Frontend (La Página Web)
No necesitas servidores web super extraños para la vista. Simplemente ve a la carpeta `frontend` en tu explorador de archivos convencional y haz doble clic sobre el archivo **`index.html`** para abrirlo en tu navegador favorito (Chrome, Safari, Edge).

### Paso 6: Configurar Pasarela de Pagos (Mercado Pago)
Para que el carrito de compras procese los pagos, necesitamos instalar la librería oficial de Mercado Pago en tu servidor:
```bash
pip install mercadopago
```

### Paso 7: Configuración de Credenciales

Debes vincular tu cuenta de desarrollador para que las transacciones lleguen a tu panel:
1. Ingresa a [Mercado Pago Developers](https://www.mercadopago.com.co/developers/panel).
2. Crea una aplicación llamada **MyApol**.
3. En la sección **Credenciales de Prueba**, obtén tu `Access Token` y tu `Public Key`.
4. Abre el archivo `backend/app.py` y reemplaza los tokens en las líneas correspondientes (asegúrate de que estén entre comillas).
5. Abre el archivo `frontend/index.html` y pega tu `Public Key` en la inicialización del SDK de Mercado Pago.

### Paso 8: ¡A comprar! (Pruebas)
Una vez configurado:
- Abre tu catálogo (`index.html`).
- Agrega productos al carrito.
- Haz clic en **PROCEDER AL PAGO**. 
- Se abrirá la ventana oficial de Mercado Pago donde podrás usar [Tarjetas de Prueba](https://www.mercadopago.com.co/developers/es/docs/checkout-pro/additional-content/test-cards) para simular una compra exitosa sin dinero real.

## Despliegue en Producción (Cloud)

Este proyecto ha sido optimizado para funcionar en la nube, separando el Frontend del Backend para garantizar mayor velocidad y escalabilidad.

### Paso 9: Despliegue del Backend (PythonAnywhere)
El cerebro de la aplicación (la API) se encuentra alojado en **PythonAnywhere**:
1. Sube la carpeta `/backend` a tu cuenta de PythonAnywhere.
2. Crea un **Virtualenv** e instala las librerías necesarias (`flask`, `mercadopago`).
3. En la pestaña **Web**, configura el archivo `WSGI` apuntando a tu `app.py`.
4. Ejecuta un terminal tipo consola en el servidor y corre `python backend/init_db.py` para generar tu base de datos en la nube.
5. Tu API estará viva en una URL similar a: `https://tu-usuario.pythonanywhere.com/api`.

### Paso 10: Despliegue del Frontend (GitHub Pages)
La interfaz visual se encuentra alojada en **GitHub Pages**:
1. Crea un repositorio en GitHub y sube la carpeta `/frontend`.
2. Ve a **Settings > Pages** y selecciona la rama donde subiste los archivos para activar el sitio.
3. Esto te proporcionará una URL pública para acceder a tu catálogo desde cualquier parte del mundo.

### Paso 11: Vinculación Final (`config.js`)
Para que tu página web se comunique correctamente con tu servidor en la nube, asegúrate de que el archivo `frontend/config.js` tenga la URL correcta de tu backend en PythonAnywhere:
```javascript
const CONFIG = {
    API_BASE_URL: 'https://degnisdev.pythonanywhere.com/api'
};
```
> **Nota:** Gracias a la configuración de **CORS** en el `app.py`, GitHub Pages podrá realizar peticiones a PythonAnywhere de manera segura.

## USUARIOS Y CONTRASEÑAS PRUEBA

- Usuario: admin@myapol.com
- Contraseña: 12345

- Cliente: cliente@myapol.cpm
- Contraseña: 12345

