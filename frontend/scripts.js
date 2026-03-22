/* Archivo de Scripts Principal para MyApol */

// Variables globales
let todosLosDispositivos = [];
let idDispositivo = null;

// Formateador de moneda
const formatearCOP = (numero) => new Intl.NumberFormat('es-CO', { style: 'currency', currency: 'COP', maximumFractionDigits: 0 }).format(numero);

// Imagen Genérica si no hay foto real
const imgPlaceholder = "https://placehold.co/600x400/1a1f24/ffffff?text=Dispositivo+Apple";

document.addEventListener('DOMContentLoaded', () => {

    // --- LÓGICA PARA INDEX.HTML (Catálogo) ---
    const contenedorDispositivos = document.getElementById('contenedor-dispositivos');
    if (contenedorDispositivos) {
        fetch('http://localhost:5000/api/dispositivos')
            .then(respuesta => respuesta.json())
            .then(datos => {
                todosLosDispositivos = datos.dispositivos;
                pintarDispositivos(todosLosDispositivos);
            })
            .catch(error => {
                console.error("Error conectando al backend:", error);
                contenedorDispositivos.innerHTML =
                    '<div class="alert alert-danger">Error al cargar los datos. Verifica que el servidor Backend (app.py) esté corriendo.</div>';
            });

        // Buscador
        const buscador = document.getElementById('buscador');
        if (buscador) {
            buscador.addEventListener('input', (e) => {
                const texto = e.target.value.toLowerCase().trim();
                const filtrados = todosLosDispositivos.filter(item =>
                    item.nombre.toLowerCase().includes(texto)
                );
                pintarDispositivos(filtrados);
            });
        }

        // Filtros
        const botonesFiltro = document.querySelectorAll('.btn-filtro');
        botonesFiltro.forEach(boton => {
            boton.addEventListener('click', (e) => {
                botonesFiltro.forEach(b => { b.classList.remove('btn-accent'); b.classList.add('btn-outline-light'); });
                e.target.classList.remove('btn-outline-light'); e.target.classList.add('btn-accent');

                const categoriaBuscada = e.target.getAttribute('data-categoria');
                if (categoriaBuscada === 'Todas') {
                    pintarDispositivos(todosLosDispositivos);
                } else {
                    const filtrados = todosLosDispositivos.filter(item => item.categoria === categoriaBuscada);
                    pintarDispositivos(filtrados);
                }
            });
        });
    }

    // --- LÓGICA PARA DETALLE.HTML (Vista Individual) ---
    const zonaDetalle = document.getElementById('zona-detalle');
    if (zonaDetalle) {
        const parametros = new URLSearchParams(window.location.search);
        idDispositivo = parametros.get('id');

        if (!idDispositivo) {
            zonaDetalle.innerHTML = '<div class="alert alert-danger">No se especificó un dispositivo.</div>';
            return;
        }

        fetch(`http://localhost:5000/api/dispositivos/${idDispositivo}`)
            .then(res => res.json())
            .then(datos => {
                if (datos.success === false) {
                    zonaDetalle.innerHTML = '<div class="alert alert-warning">Dispositivo no encontrado.</div>';
                    return;
                }

                const imgSrc = datos.url_imagen ? datos.url_imagen : imgPlaceholder;

                // Guardamos el producto en memoria para el botón de carrito
                window._currentProduct = datos;

                // Construir miniaturas de galería si existen
                let galeriaHTML = '';
                if (datos.galeria && datos.galeria.length > 0) {
                    const todasLasFotos = [datos.url_imagen, ...datos.galeria];
                    galeriaHTML = `
                        <div class="d-flex gap-2 justify-content-center mt-3 flex-wrap">
                            ${todasLasFotos.map((foto, i) => `
                                <img src="${foto}" alt="Vista ${i + 1}"
                                     onclick="cambiarFotoPrincipal('${foto}')"
                                     class="thumbnail-galeria ${i === 0 ? 'thumbnail-activa' : ''}"
                                     style="width:70px; height:70px; object-fit:contain; cursor:pointer; border-radius:10px; padding:4px; background:rgba(255,255,255,0.05);">
                            `).join('')}
                        </div>`;
                }

                zonaDetalle.innerHTML = `
                    <div class="col-md-5 text-center">
                        <div class="p-4" style="background: linear-gradient(0deg, rgba(25,28,33,1) 0%, rgba(40,44,52,1) 100%); border-radius: 20px; box-shadow: 0 20px 40px rgba(0,0,0,0.5);">
                            <img id="foto-principal" src="${imgSrc}" class="img-fluid object-fit-contain" style="max-height: 380px; filter: drop-shadow(0px 10px 15px rgba(0,0,0,0.5)); transition: opacity 0.3s ease;" alt="${datos.nombre}">
                        </div>
                        ${galeriaHTML}
                    </div>
                    <div class="col-md-7 mt-5 mt-md-0 ps-md-5">
                        <span class="badge bg-primary mb-2 px-3 py-2 rounded-pill">${datos.marca}</span>
                        <span class="badge bg-secondary mb-2 px-3 py-2 rounded-pill">${datos.categoria}</span>
                        <h1 class="fw-bold display-4 mb-3 text-gradient">${datos.nombre}</h1>
                        <p class="fs-5 text-light opacity-75 mb-4 lh-lg">${datos.descripcion}</p>
                        <h2 class="fw-bold text-white mb-4 display-6">${formatearCOP(datos.precio)}</h2>
                        <button class="btn btn-cta btn-lg px-5 shadow" onclick="cart.add(window._currentProduct)">
                            <i class="bi bi-cart me-2"></i> Añadir al Carrito
                        </button>
                    </div>
                `;


                cargarComentarios();
            })
            .catch(e => console.error(e));
    }
});

// FUNCIÓN: Pintar tarjetas en index.html
function pintarDispositivos(lista) {
    const contenedor = document.getElementById('contenedor-dispositivos');
    contenedor.innerHTML = '';

    if (lista.length === 0) {
        contenedor.innerHTML = '<div class="col-12"><p class="text-center text-muted">No se encontraron dispositivos.</p></div>';
        return;
    }

    lista.forEach(item => {
        const precioFormateado = formatearCOP(item.precio);
        const imagenCard = item.url_imagen ? item.url_imagen : imgPlaceholder;

        const htmlCard = `
            <div class="col-md-4 col-sm-6">
                <div class="card card-hoverable h-100">
                    <div class="p-3 text-center" style="height: 200px; overflow: hidden; border-radius: 16px 16px 0 0; background: linear-gradient(0deg, rgba(25,28,33,1) 0%, rgba(40,44,52,1) 100%);">
                        <img src="${imagenCard}" class="img-fluid h-100 object-fit-contain" alt="${item.nombre}">
                    </div>
                    <div class="card-body">
                        <span class="badge bg-primary mb-2">${item.categoria}</span>
                        <h5 class="card-title fw-bold text-white">${item.nombre}</h5>
                        <h6 class="card-subtitle mb-2 text-secondary">${item.marca}</h6>
                        <p class="card-text small text-white-50 text-truncate">${item.descripcion}</p>
                    </div>
                    <div class="card-footer d-flex justify-content-between align-items-center pb-3 px-3">
                        <span class="fw-bold fs-5 text-white">${precioFormateado}</span>
                        <div class="d-flex gap-2">
                            <button class="btn btn-primary btn-sm rounded-circle shadow-sm" onclick="agregarAlCarritoDesdeCatalogo(${item.id})" title="Añadir al carrito">
                                <i class="bi bi-cart-plus"></i>
                            </button>
                            <a href="detalle.html?id=${item.id}" class="btn btn-outline-light btn-sm rounded-pill px-3">Detalle</a>
                        </div>
                    </div>
                </div>
            </div>
        `;
        contenedor.innerHTML += htmlCard;
    });
}

// FUNCIÓN: Lógica de Autenticación para Comentarios en detalle.html
document.addEventListener('DOMContentLoaded', () => {
    const idUrl = new URLSearchParams(window.location.search).get('id');
    if (idUrl) {
        idDispositivo = idUrl;

        const zonaUsuarioDetalle = document.getElementById('zona-usuario-detalle');
        const token = localStorage.getItem('cliente_token');
        const nombre = localStorage.getItem('cliente_nombre');

        if (token && nombre && zonaUsuarioDetalle) {
            zonaUsuarioDetalle.innerHTML = `
                <span class="text-white-50 small me-2">Hola, <strong class="text-white">${nombre}</strong></span>
                <button class="btn btn-outline-danger btn-sm rounded-pill px-3" onclick="cerrarSesionCliente()">Salir</button>
            `;

            const cajaFormulario = document.getElementById('caja-hacer-comentario');
            if (cajaFormulario) {
                cajaFormulario.innerHTML = `
                    <div class="card card-dark mb-4 shadow-sm border-secondary">
                        <div class="card-body">
                            <textarea id="texto-comentario" class="form-control form-control-dark mb-3" rows="3"
                                placeholder="¿Qué opinas de este dispositivo? Escribe como ${nombre}..."></textarea>
                            <button id="btn-comentar" class="btn btn-accent btn-sm" onclick="enviarComentario()">
                                <i class="bi bi-send me-1"></i> Publicar Opinión
                            </button>
                        </div>
                    </div>
                `;
            }
        }

        cargarComentarios();
    }
});

// FUNCIÓN: Cargar comentarios
function cargarComentarios() {
    fetch(`http://localhost:5000/api/comentarios/${idDispositivo}`)
        .then(res => res.json())
        .then(comentarios => {
            const lista = document.getElementById('lista-comentarios');
            lista.innerHTML = '';

            if (comentarios.length === 0) {
                lista.innerHTML = '<p class="text-muted mb-0">Sé el primero en opinar sobre este producto.</p>';
                return;
            }

            comentarios.forEach(c => {
                lista.innerHTML += `
                    <div class="comment-item mb-3 pt-3 pb-2 bg-transparent">
                        <div class="d-flex justify-content-between mb-2">
                            <strong class="text-white"><i class="bi bi-person-circle text-primary me-2"></i> ${c.usuario}</strong>
                            <small class="text-white-50">${new Date(c.fecha).toLocaleDateString()}</small>
                        </div>
                        <p class="text-light opacity-75 ms-4">${c.texto}</p>
                    </div>
                `;
            });
        })
        .catch(err => {
            console.error("Error al cargar comentarios:", err);
            const lista = document.getElementById('lista-comentarios');
            lista.innerHTML = '<p class="text-danger mb-0">Error de conexión al cargar las opiniones.</p>';
        });
}

// FUNCIÓN: Enviar un comentario
function enviarComentario() {
    const texto = document.getElementById('texto-comentario').value;
    if (texto.trim() === '') return alert('Escribe algo primero.');

    const idReal = localStorage.getItem('cliente_id');
    if (!idReal) {
        return alert("Error fatal: No se detectó tu sesión de usuario.");
    }

    const datos = {
        texto: texto,
        id_usuario: parseInt(idReal)
    };

    fetch(`http://localhost:5000/api/comentarios/${idDispositivo}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' },
        body: JSON.stringify(datos)
    })
        .then(res => res.json())
        .then(respuesta => {
            if (respuesta.success) {
                document.getElementById('texto-comentario').value = '';
                cargarComentarios();
            } else {
                alert("Hubo un error al guardar el comentario: " + (respuesta.mensaje || "Desconocido"));
            }
        })
        .catch(err => {
            console.error("Fetch POST Error:", err);
            alert("No se pudo conectar al servidor para guardar tu opinión.");
        });
}

// FUNCIÓN: Cerrar sesión cliente
function cerrarSesionCliente() {
    localStorage.removeItem('cliente_token');
    localStorage.removeItem('cliente_id');
    localStorage.removeItem('cliente_nombre');
    // Limpiar el carrito al salir de sesión
    localStorage.removeItem('myapol_cart');
    window.location.reload();
}

function cambiarFotoPrincipal(src) {
    const foto = document.getElementById('foto-principal');
    if (foto) {
        foto.style.opacity = '0';
        setTimeout(() => { foto.src = src; foto.style.opacity = '1'; }, 200);
    }
    document.querySelectorAll('.thumbnail-galeria').forEach(t => t.classList.remove('thumbnail-activa'));
    event.target.classList.add('thumbnail-activa');
}


