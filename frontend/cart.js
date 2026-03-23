// ==========================================
// LÓGICA DEL CARRITO DE COMPRAS
// ==========================================
const cart = {
    items: [],

    // 1. Añadir producto
    add(product) {
        // SEGURIDAD: Solo usuarios logueados pueden agregar al carrito
        const token = localStorage.getItem('cliente_token');
        if (!token) {
            alert("⚠️ Debes iniciar sesión para agregar productos al carrito.");
            window.location.href = 'login_cliente.html';
            return;
        }

        const existing = this.items.find(i => i.id === product.id);
        if (existing) {
            existing.quantity++;
        } else {
            this.items.push({ ...product, quantity: 1 });
        }
        this.save();
        this.updateUI();
        const offcanvas = new bootstrap.Offcanvas(document.getElementById('offcanvasCart'));
        offcanvas.show();
    },


    // 2. Eliminar producto
    remove(id) {
        this.items = this.items.filter(i => i.id !== id);
        this.save();
        this.updateUI();
    },

    // 3. Vaciar carrito
    clear() {
        if (confirm("¿Seguro que quieres vaciar el carrito?")) {
            this.items = [];
            this.save();
            this.updateUI();
        }
    },

    // 4. Guardar en el navegador (LocalStorage)
    save() {
        localStorage.setItem('myapol_cart', JSON.stringify(this.items));
    },

    // 5. Cargar desde el navegador al abrir la web
    load() {
        const saved = localStorage.getItem('myapol_cart');
        if (saved) this.items = JSON.parse(saved);
        this.updateUI();
    },

    // 6. Actualizar la interfaz (el dibujo del carrito)
    updateUI() {
        const count = this.items.reduce((acc, item) => acc + item.quantity, 0);
        document.getElementById('cart-count').innerText = count;

        const container = document.getElementById('cart-items-container');
        const totalPriceEl = document.getElementById('cart-total-price');
        const btnCheckout = document.getElementById('btn-checkout');

        if (this.items.length === 0) {
            container.innerHTML = '<p class="text-center text-white-50 mt-5">Tu carrito está vacío.</p>';
            totalPriceEl.innerText = '$0';
            btnCheckout.classList.add('disabled');
        } else {
            btnCheckout.classList.remove('disabled');
            let total = 0;
            container.innerHTML = this.items.map(item => {
                total += item.precio * item.quantity;
                return `
                    <div class="cart-item">
                        <img src="${item.url_imagen || imgPlaceholder}" alt="${item.nombre}">
                        <div class="cart-item-info">
                            <div class="cart-item-title">${item.nombre}</div>
                            <div class="cart-item-precio">${item.quantity} x ${formatearCOP(item.precio)}</div>
                        </div>
                        <button class="btn btn-sm btn-outline-danger border-0" onclick="cart.remove(${item.id})">
                            <i class="bi bi-trash"></i>
                        </button>
                    </div>
                `;
            }).join('');
            totalPriceEl.innerText = formatearCOP(total);
        }
    },

    async checkout() {
        const btnCheckout = document.getElementById('btn-checkout');
        btnCheckout.innerText = "Procesando...";
        btnCheckout.classList.add('disabled');

        try {
            // 1. Enviamos el carrito al backend para crear la preferencia
            const response = await fetch('http://localhost:5000/api/create_preference', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ items: this.items })
            });
            const data = await response.json();

            if (data.id) {
                // 2. Inicializamos Mercado Pago con tu PUBLIC_KEY
                const mp = new MercadoPago('TU_PUBLIC_KEY', { locale: 'es-CO' });

                // 3. Abrimos el Checkout Pro
                mp.checkout({
                    preference: { id: data.id },
                    autoOpen: true
                });
            }
        } catch (error) {
            console.error("Error en el pago:", error);
            alert("Hubo un error al iniciar el pago.");
        } finally {
            btnCheckout.innerText = "Finalizar Compra";
            btnCheckout.classList.remove('disabled');
        }
    }


};

// Función puente para el catálogo
function agregarAlCarritoDesdeCatalogo(id) {
    const p = todosLosDispositivos.find(d => d.id === id);
    if (p) cart.add(p);
}

// Inicializar el carrito al cargar
document.addEventListener('DOMContentLoaded', () => cart.load());
