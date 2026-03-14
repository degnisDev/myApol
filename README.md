# MyApol

**MyApol** es una plataforma web (E-commerce / Catálogo) diseñada para ofrecer una experiencia visual premium, rápida y dinámica. Implementa una arquitectura Cliente-Servidor (API REST) estructurada con un diseño moderno y un completo panel administrativo.

## Funcionalidades Principales

- **Catálogo Dinámico e Interactivo**: Búsqueda en tiempo real y filtrado de productos por categorías.
- **Detalle de Producto**: Vista expandida de cada dispositivo consumiendo la API por ID de manera reactiva.
- **Sistema de Opiniones**: Los usuarios registrados pueden iniciar sesión y dejar comentarios públicos en tiempo real.
- **Panel Administrativo (CRUD)**: Acceso privado para gestionar (Crear, Leer, Actualizar y Eliminar) completamente el inventario de la tienda.
- **Seguridad Básica**: Autenticación de administrador y clientes basada en roles. Inyección de datos protegida con peticiones paramétricas.

## Tecnologías Utilizadas

- **Frontend**: HTML5, CSS3, JavaScript (Vanilla), Bootstrap 5, Bootstrap Icons.
- **Backend**: Python 3, Flask (RESTful API).
- **Base de Datos**: SQLite (`database.db`).

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

## USUARIOS Y CONTRASEÑAS PRUEBA

- Usuario: admin@myapol.com
- Contraseña: 12345

- Cliente: cliente@myapol.cpm
- Contraseña: 12345

