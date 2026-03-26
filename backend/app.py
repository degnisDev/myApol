import mercadopago
from flask import Flask, jsonify, request
import sqlite3
import os

app = Flask(__name__)

# Inicializar mercado pago con Access Token
sdk = mercadopago.SDK("APP_USR-7274769787548043-032511-b3a9e049624e523fca7625cf52ee3161-3292872524")

# Función ayudante para conectarse a la DB
def get_db_connection():
    # Asegura que busque la DB en la misma ruta que este archivo
    db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'database.db')
    conn = sqlite3.connect(db_path)
    # Esto permite que las filas de la DB se manejen como diccionarios
    conn.row_factory = sqlite3.Row
    return conn

# -------------------------------------------------------------
# RUTA DE PRUEBA: Verifica que el servidor está funcionando
# -------------------------------------------------------------
@app.route('/')
def index():
    return jsonify({"mensaje": "¡Bienvenido a la API de MyApol! El servidor está vivo."})

# -------------------------------------------------------------
# RUTA PÚBLICA: Obtener todos los dispositivos (para el index.html)
# -------------------------------------------------------------
@app.route('/api/dispositivos', methods=['GET'])
def get_dispositivos():
    conn = get_db_connection()
    # Hacemos una consulta con los JOINS para traer los nombres de marca y categoría en vez de los IDs
    query = '''
        SELECT d.id, d.nombre, d.descripcion, d.precio, d.url_imagen, 
               m.nombre as marca, c.nombre as categoria
        FROM dispositivos d
        JOIN marcas m ON d.id_marca = m.id
        JOIN categorias c ON d.id_categoria = c.id
    '''
    dispositivos_db = conn.execute(query).fetchall()
    conn.close()

    # Convertimos los resultados en una lista de diccionarios JSON
    dispositivos_lista = [dict(row) for row in dispositivos_db]
    
    return jsonify({
        "total": len(dispositivos_lista),
        "dispositivos": dispositivos_lista
    })

# -------------------------------------------------------------
# RUTA PÚBLICA: Obtener detalle de un solo dispositivo por ID
# -------------------------------------------------------------
@app.route('/api/dispositivos/<int:id>', methods=['GET'])
def get_dispositivo(id):
    conn = get_db_connection()
    equipo = conn.execute('''
            SELECT d.*, m.nombre as marca, c.nombre as categoria
            FROM dispositivos d
            JOIN marcas m ON d.id_marca = m.id
            JOIN categorias c ON d.id_categoria = c.id
            WHERE d.id = ?
        ''', (id,)).fetchone()

    if equipo is None:
        conn.close()
        return jsonify({'success': False, 'mensaje': 'No encontrado'}), 404
    
    # Obtener fotos adicionales de la galería
    rows = conn.execute('SELECT url_imagen FROM imagenes_dispositivo WHERE id_dispositivo = ?', (id,)).fetchall()
    galeria = [r['url_imagen'] for r in rows]
    
    data = dict(equipo)
    data['galeria'] = galeria  # Lista de fotos extra, o [] si no tiene
    
    conn.close()
    return jsonify(data)


# -------------------------------------------------------------
# RUTA PÚBLICA: Obtener y Crear Comentarios de un dispositivo
# -------------------------------------------------------------
@app.route('/api/comentarios/<int:id_dispositivo>', methods=['GET', 'POST'])
def manejar_comentarios(id_dispositivo):
    conn = get_db_connection()
    
    if request.method == 'GET':
        query = '''
            SELECT c.id, c.texto, c.fecha, u.nombre as usuario
            FROM comentarios c
            JOIN usuarios u ON c.id_usuario = u.id
            WHERE c.id_dispositivo = ?
            ORDER BY c.fecha DESC
        '''
        comentarios_db = conn.execute(query, (id_dispositivo,)).fetchall()
        comentarios_lista = [dict(row) for row in comentarios_db]
        conn.close()
        return jsonify(comentarios_lista)
        
    elif request.method == 'POST':
        datos = request.json
        # Extraemos el ID del usuario real enviado desde el Frontend
        id_usuario = datos.get('id_usuario')
        
        if not id_usuario:
            return jsonify({"success": False, "mensaje": "Debe iniciar sesión para comentar"}), 401 
        
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO comentarios (texto, id_dispositivo, id_usuario)
            VALUES (?, ?, ?)
        ''', (datos['texto'], id_dispositivo, id_usuario))
        conn.commit()
        nuevo_id = cursor.lastrowid
        conn.close()
        
        return jsonify({"success": True, "mensaje": "Comentario agregado", "id": nuevo_id}), 201

# -------------------------------------------------------------
# RUTA PRIVADA: Login de Administrador
# -------------------------------------------------------------
@app.route('/api/login', methods=['POST'])
def login():
    datos = request.json
    correo = datos.get('correo')
    password = datos.get('password')
    
    conn = get_db_connection()
    usuario = conn.execute('SELECT * FROM usuarios WHERE correo = ? AND password = ?', (correo, password)).fetchone()
    conn.close()
    
    if usuario:
        # Devuelve un token falso por simplicidad académica
        return jsonify({"success": True, "mensaje": "Login exitoso", "token": "admin_token_123", "id_usuario": usuario['id']})
    else:
        return jsonify({"success": False, "mensaje": "Credenciales inválidas"}), 401

# -------------------------------------------------------------
# RUTA PÚBLICA: Registro de Clientes Nuevos
# -------------------------------------------------------------
@app.route('/api/registro_cliente', methods=['POST'])
def registro_cliente():
    datos = request.json
    nombre = datos.get('nombre')
    correo = datos.get('correo')
    password = datos.get('password')
    
    # Validamos
    if not nombre or not correo or not password:
        return jsonify({"success": False, "mensaje": "Faltan datos requeridos."}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Revisar si el correo ya existe
    existente = cursor.execute('SELECT id FROM usuarios WHERE correo = ?', (correo,)).fetchone()
    if existente:
        conn.close()
        return jsonify({"success": False, "mensaje": "Este correo ya está registrado."}), 409
        
    try:
        # Insertar nuevo usuario como Cliente (id_rol = 2)
        cursor.execute('''
            INSERT INTO usuarios (nombre, correo, password, id_rol)
            VALUES (?, ?, ?, 2)
        ''', (nombre, correo, password))
        conn.commit()
        nuevo_id = cursor.lastrowid
        conn.close()
        return jsonify({"success": True, "mensaje": "Usuario registrado con éxito.", "id_usuario": nuevo_id}), 201
    except Exception as e:
        conn.close()
        return jsonify({"success": False, "mensaje": str(e)}), 500

# -------------------------------------------------------------
# RUTA PÚBLICA: Login de Clientes
# -------------------------------------------------------------
@app.route('/api/login_cliente', methods=['POST'])
def login_cliente():
    datos = request.json
    correo = datos.get('correo')
    password = datos.get('password')
    
    conn = get_db_connection()
    # Nos aseguramos de que el que se loguea tenga rol 2 (Cliente) o verificamos solo credenciales
    usuario = conn.execute('SELECT * FROM usuarios WHERE correo = ? AND password = ? AND id_rol = 2', (correo, password)).fetchone()
    conn.close()
    
    if usuario:
        # Retornamos datos del cliente para su sesión
        return jsonify({
            "success": True, 
            "mensaje": "Bienvenido", 
            "token": "user_token_" + str(usuario['id']), 
            "id_usuario": usuario['id'],
            "nombre": usuario['nombre']
        })
    else:
        return jsonify({"success": False, "mensaje": "Correo o contraseña incorrectos."}), 401

# -------------------------------------------------------------
# RUTA PRIVADA: Crear un nuevo dispositivo
# -------------------------------------------------------------
@app.route('/api/dispositivos', methods=['POST'])
def crear_dispositivo():
    datos = request.json
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO dispositivos (nombre, descripcion, precio, url_imagen, id_marca, id_categoria)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (datos['nombre'], datos['descripcion'], datos['precio'], datos.get('url_imagen', ''), datos['id_marca'], datos['id_categoria']))
    conn.commit()
    nuevo_id = cursor.lastrowid
    conn.close()
    
    return jsonify({"success": True, "mensaje": "Dispositivo creado", "id": nuevo_id}), 201

# -------------------------------------------------------------
# RUTA PRIVADA: Actualizar un dispositivo
# -------------------------------------------------------------
@app.route('/api/dispositivos/<int:id>', methods=['PUT'])
def actualizar_dispositivo(id):
    datos = request.json
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE dispositivos
        SET nombre = ?, descripcion = ?, precio = ?, url_imagen = ?, id_marca = ?, id_categoria = ?
        WHERE id = ?
    ''', (datos['nombre'], datos['descripcion'], datos['precio'], datos.get('url_imagen', ''), datos['id_marca'], datos['id_categoria'], id))
    conn.commit()
    conn.close()
    
    return jsonify({"success": True, "mensaje": "Dispositivo actualizado"}), 200

# -------------------------------------------------------------
# RUTA PRIVADA: Eliminar un dispositivo
# -------------------------------------------------------------
@app.route('/api/dispositivos/<int:id>', methods=['DELETE'])
def eliminar_dispositivo(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM dispositivos WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    
    return jsonify({"success": True, "mensaje": "Dispositivo eliminado"}), 200

# -------------------------------------------------------------
# CORS: Habilitar peticiones desde el Frontend local
# -------------------------------------------------------------
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

# -------------------------------------------------------------
# RUTA MERCADO PAGO: Crear preferencia de pago
# -------------------------------------------------------------
@app.route('/api/create_preference', methods=['POST'])
def create_preference():
    try:
        items_carrito = request.json.get('items')
        
        items_mp = []
        for item in items_carrito:
            items_mp.append({
                "id": str(item['id']),
                "title": item['nombre'],
                "quantity": int(item['quantity']),
                "unit_price": float(item['precio']),
                "currency_id": "COP"
            })

        preference_data = {
            "items": items_mp,
            # "back_urls": {
            #     "success": "http://localhost:5500/frontend/index.html",
            #     "failure": "http://localhost:5500/frontend/index.html",
            #     "pending": "http://localhost:5500/frontend/index.html"
            # },
            # "back_urls": {
            #     "success": "https://degnisdev.com/myapol/index.html",
            #     "failure": "https://degnisdev.com/myapol/index.html",
            #     "pending": "https://degnisdev.com/myapol/index.html"
            # },
            "back_urls": {
                "success": "https://degnisdev.github.io/myApol/frontend/index.html",
                "failure": "https://degnisdev.github.io/myApol/frontend/index.html",
                "pending": "https://degnisdev.github.io/myApol/frontend/index.html"
            },
            
            # "auto_return": "approved",
        }

        # Intentamos crear la preferencia
        preference_response = sdk.preference().create(preference_data)
        
        # --- NUEVA LÓGICA DE DIAGNÓSTICO ---
        status_sdk = preference_response["status"]
        response_sdk = preference_response["response"]

        if status_sdk >= 400:
            print("ERROR DE MERCADO PAGO:", response_sdk) # Esto saldrá en tu terminal negra
            return jsonify({"error": "Error de Mercado Pago", "detalles": response_sdk}), status_sdk

        # Si todo salió bien, devolvemos el ID
        return jsonify({"id": response_sdk["id"]})

    except Exception as e:
        print("EXCEPCIÓN EN EL SERVIDOR:", str(e))
        return jsonify({"error": "Excepción interna", "mensaje": str(e)}), 500



if __name__ == '__main__':
    # Ejecuta el servidor en el puerto 5000 con modo debug activado
    app.run(debug=True, port=5000)
