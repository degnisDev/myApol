from flask import Flask, jsonify, request
import sqlite3
import os

app = Flask(__name__)

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
    query = '''
        SELECT d.id, d.nombre, d.descripcion, d.precio, d.url_imagen, 
               m.nombre as marca, c.nombre as categoria
        FROM dispositivos d
        JOIN marcas m ON d.id_marca = m.id
        JOIN categorias c ON d.id_categoria = c.id
        WHERE d.id = ?
    '''
    dispositivo = conn.execute(query, (id,)).fetchone()
    conn.close()
    
    if dispositivo:
        return jsonify(dict(dispositivo))
    else:
        return jsonify({"success": False, "mensaje": "Dispositivo no encontrado"}), 404

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
        # Asumimos id_usuario = 2 (el cliente por defecto) para este proyecto académico
        id_usuario = datos.get('id_usuario', 2) 
        
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

if __name__ == '__main__':
    # Ejecuta el servidor en el puerto 5000 con modo debug activado
    app.run(debug=True, port=5000)
