import sqlite3
import os

# Asegurarnos de que estamos creando el archivo en el mismo lugar que el script
db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'database.db')

print(f"Conectando y creando la base de datos en: {db_path}")
conexion = sqlite3.connect(db_path)
cursor = conexion.cursor()

# 1. Tabla ROLES
cursor.execute('''
CREATE TABLE IF NOT EXISTS roles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL
)
''')

# 2. Tabla USUARIOS
cursor.execute('''
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    correo TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    id_rol INTEGER,
    FOREIGN KEY(id_rol) REFERENCES roles(id)
)
''')

# 3. Tabla MARCAS
cursor.execute('''
CREATE TABLE IF NOT EXISTS marcas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL
)
''')

# 4. Tabla CATEGORIAS
cursor.execute('''
CREATE TABLE IF NOT EXISTS categorias (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL
)
''')

# 5. Tabla DISPOSITIVOS
cursor.execute('''
CREATE TABLE IF NOT EXISTS dispositivos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    descripcion TEXT,
    precio REAL NOT NULL,
    url_imagen TEXT,
    id_marca INTEGER,
    id_categoria INTEGER,
    FOREIGN KEY(id_marca) REFERENCES marcas(id),
    FOREIGN KEY(id_categoria) REFERENCES categorias(id)
)
''')

# 6. Tabla COMENTARIOS
cursor.execute('''
CREATE TABLE IF NOT EXISTS comentarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    texto TEXT NOT NULL,
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    id_dispositivo INTEGER,
    id_usuario INTEGER,
    FOREIGN KEY(id_dispositivo) REFERENCES dispositivos(id),
    FOREIGN KEY(id_usuario) REFERENCES usuarios(id)
)
''')

print("Insertando datos de prueba (MyApol)...")
try:
    # ----------------------------------------------------
    # DATOS INICIALES: Roles y Usuario
    # ----------------------------------------------------
    cursor.execute("INSERT INTO roles (nombre) VALUES ('Administrador'), ('Cliente')")
    cursor.execute("INSERT INTO usuarios (nombre, correo, password, id_rol) VALUES ('Super Admin', 'admin@myapol.com', '12345', 1)")
    
    # ----------------------------------------------------
    # MARCA
    # ----------------------------------------------------
    cursor.execute("INSERT INTO marcas (nombre) VALUES ('Apple')")
    
    # ----------------------------------------------------
    # CATEGORÍAS
    # ----------------------------------------------------
    categorias = [
        ('Smartphones',), ('Computers',), ('Tablets',), 
        ('Wearables',), ('Home & Entertainment',), ('Accessories',), ('Merch',)
    ]
    cursor.executemany("INSERT INTO categorias (nombre) VALUES (?)", categorias)

    # ----------------------------------------------------
    # PRODUCTOS (Precios en COP aproximados)
    # id_marca=1 siempre es Apple
    # id_categoria: 1=Smartphones, 2=Computers, 3=Tablets, 4=Wearables, 5=Home, 6=Accessories, 7=Merch
    # ----------------------------------------------------
    productos = [
        # Smartphones (id_categoria=1)
        ('iPhone 15', 'El iPhone 15 con Dynamic Island y cámara de 48 MP.', 3800000, '', 1, 1),
        ('iPhone 15 Pro', 'Diseño de titanio aeroespacial. Chip A17 Pro.', 5200000, '', 1, 1),
        ('iPhone 15 Pro Max', 'El iPhone más potente, titanio, zoom óptico 5x.', 6500000, '', 1, 1),
        
        # Computers (id_categoria=2)
        ('MacBook Air', 'Súper ligera. Súper chip M3.', 4900000, '', 1, 2),
        ('MacBook Pro', 'Portátil profesional con chip M3 Pro/Max.', 9500000, '', 1, 2),
        ('iMac', 'Computadora de escritorio todo en uno con diseño increíble. Chip M3.', 7200000, '', 1, 2),
        
        # Tablets (id_categoria=3)
        ('iPad', 'El iPad clásico para todas tus tareas diarias.', 2400000, '', 1, 3),
        ('iPad Air', 'Ligero, brillante y potente con chip M2.', 3500000, '', 1, 3),
        ('iPad Pro', 'El iPad definitivo con pantalla OLED y chip M4.', 6000000, '', 1, 3),
        
        # Wearables (id_categoria=4)
        ('Apple Watch Series 9', 'Más inteligente, más brillante, más capaz.', 2100000, '', 1, 4),
        ('AirPods Pro', 'Cancelación activa de ruido y audio espacial.', 1300000, '', 1, 4),
        ('Apple Vision Pro', 'La primera computadora espacial de Apple.', 18000000, '', 1, 4),
        
        # Home & Entertainment (id_categoria=5)
        ('Apple TV 4K', 'La experiencia cinematográfica en tu casa.', 750000, '', 1, 5),
        ('HomePod', 'Audio de alta fidelidad asombroso.', 1600000, '', 1, 5),
        ('HomePod mini', 'Sonido envolvente en un diseño compacto.', 550000, '', 1, 5),
        
        # Accessories (id_categoria=6)
        ('AirTag', 'Encuentra tus llaves, mochila y más.', 180000, '', 1, 6),
        ('Apple Pencil', 'Precisión increíble para dibujar y escribir.', 650000, '', 1, 6),
        ('Magic Keyboard', 'El compañero perfecto para iPad y Mac.', 1500000, '', 1, 6),
        
        # Merch (id_categoria=7)
        ('Camisetas Apple', 'Ropa oficial de Apple Store.', 200000, '', 1, 7),
        ('Pines Apple', 'Pines coleccionables de la marca.', 80000, '', 1, 7),
        ('Busos / Hoodies Apple', 'Sudaderas cómodas con logo de Apple.', 350000, '', 1, 7)
    ]
    
    cursor.executemany('''
        INSERT INTO dispositivos (nombre, descripcion, precio, url_imagen, id_marca, id_categoria) 
        VALUES (?, ?, ?, ?, ?, ?)
    ''', productos)

    conexion.commit()
    print("¡Base de datos 'MyApol' creada e inicializada exitosamente con datos!")

except Exception as e:
    print(f"Nota: Los datos ya existen o hubo un error: {e}")

# Cerrar la conexión
conexion.close()
