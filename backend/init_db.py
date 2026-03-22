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

# 7. Tabla IMAGENES_DISPOSITIVO (Galería)
cursor.execute('''
    CREATE TABLE IF NOT EXISTS imagenes_dispositivo (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        id_dispositivo INTEGER NOT NULL,
        url_imagen TEXT NOT NULL,
        FOREIGN KEY(id_dispositivo) REFERENCES dispositivos(id)
    )
''')

print("Insertando datos de prueba (MyApol)...")
try:

    # Limpiar solo productos y galería para poder reinsertar
    cursor.execute('DELETE FROM imagenes_dispositivo')
    cursor.execute('DELETE FROM dispositivos')

    # ----------------------------------------------------
    # DATOS INICIALES: Roles y Usuario
    # ----------------------------------------------------
    cursor.execute("INSERT INTO roles (nombre) VALUES ('Administrador'), ('Cliente')")
    cursor.execute("INSERT INTO usuarios (nombre, correo, password, id_rol) VALUES ('Super Admin', 'admin@myapol.com', '12345', 1)")
    cursor.execute("INSERT INTO usuarios (nombre, correo, password, id_rol) VALUES ('Cliente Prueba', 'cliente@myapol.com', '12345', 2)")
    
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
    # ----------------------------------------------------
    # PRODUCTOS (Precios en COP aproximados)
    # id_marca=1 siempre es Apple
    # id_categoria: 1=Smartphones, 2=Computers, 3=Tablets, 4=Wearables, 5=Home, 6=Accessories, 7=Merch
    # ----------------------------------------------------
    productos = [
        # Smartphones (cat 1)
        ('iPhone 17 Pro Max 256 GB', 'El iPhone 17 Pro Max lleva la fotografía móvil al siguiente nivel con su sistema de triple cámara de 48 MP. El potente chip A19 Pro garantiza un rendimiento inigualable en IA y procesamiento, todo en un cuerpo de titanio ultradelgado.', 5000000, 'img/dispositivos/1 - iphone_17_pro/p1-main.jpg', 1, 1),
        ('iPhone 16 Pro 512 GB', 'El iPhone 16 Pro incorpora el innovador botón de Control de Cámara para capturar fotos y video con precisión profesional. Su chip A18 Pro y pantalla Super Retina XDR de 6.3 pulgadas lo hacen perfecto para creativos y profesionales.', 3500000, 'img/dispositivos/2 - iphone_16_pro/p2-main.jpg', 1, 1),
        ('iPhone 15 Pro Max 256 GB', 'Fabricado en titanio aeroespacial con chip A17 Pro, el iPhone 15 Pro Max introduce el lente periscópico con zoom óptico 5x. El botón de acción personalizable y pantalla ProMotion de 6.7 pulgadas completan esta experiencia premium.', 2500000, 'img/dispositivos/3 - iphone_15_pro/p3-main.jpg', 1, 1),
        # Computers (cat 2)
        ('MacBook Air Chip M2 13.6" Midnight 8GB 256GB', 'La MacBook Air con chip M2 redefine lo que significa ser ligera y potente. Con 18 horas de batería, pantalla Liquid Retina de 13.6 pulgadas y diseño silencioso sin ventilador, es la laptop perfecta para estudiantes y profesionales.', 4500000, 'img/dispositivos/4 - mackBook_Air_m2/p4-main.jpg', 1, 2),
        ('MacBook Pro 14 Chip M4 16GB RAM 512GB SSD', 'El MacBook Pro 14 con chip M4 ofrece rendimiento avanzado en formato compacto. Pantalla Liquid Retina XDR de 14.2 pulgadas con ProMotion y sistema de seis altavoces crean una experiencia audiovisual inmersiva y profesional.', 7000000, 'img/dispositivos/5 - mackbook_14_m4/p5-main.jpg', 1, 2),
        ('iMac 24 M4 16GB 512GB CPU10', 'El iMac con chip M4 combina diseño ultradelgado de 24 pulgadas con pantalla Retina 4.5K deslumbrante. Con 10 núcleos de CPU y GPU integrada de última generación, redefine el espacio de trabajo creativo en casa.', 6000000, 'img/dispositivos/6 - imac_24_m4/p6-main.jpg', 1, 2),
        # Tablets (cat 3)
        ('iPad 2025 A16 Chip 11" 512GB WiFi', 'El iPad 2025 con chip A16 eleva la experiencia del iPad más popular. Pantalla Liquid Retina de 11 pulgadas, Apple Pencil Pro y Magic Keyboard lo convierten en la herramienta versátil ideal para crear, estudiar y entretenerse.', 3000000, 'img/dispositivos/7 - tablet_ipad_a16/p7-main.jpg', 1, 3),
        ('iPad Air 11" M3 128GB', 'El iPad Air con chip M3 ofrece rendimiento extraordinario en diseño elegante y ligero. Pantalla Liquid Retina de 11 pulgadas y compatibilidad con Apple Pencil Pro lo hacen perfecto para artistas y profesionales creativos.', 2500000, 'img/dispositivos/8 - ipad_Air_m3/p8-main.jpg', 1, 3),
        ('Apple iPad Pro 13" 6ta Gen 256GB', 'El iPad Pro 13 con chip M4 es la tableta más delgada y poderosa del mundo. Su pantalla Ultra Retina XDR OLED ofrece colores perfectos y negros puros ideales para profesionales creativos que exigen lo mejor.', 7000000, 'img/dispositivos/9 - ipad_13_pulg/p9-main.jpg', 1, 3),
        # Wearables (cat 4)
        ('Apple Watch Series 9', 'El Apple Watch Series 9 presenta el gesto Double Tap para controlar sin tocar la pantalla. Con Always-On display más brillante, monitorización de salud avanzada y chip S9 SiP, es el compañero definitivo para tu bienestar.', 1000000, 'img/dispositivos/13 - Apple_watch_s9/p13-main.jpg', 1, 4),
        ('Apple Watch Ultra 2 GPS + Cellular 49mm', 'El Apple Watch Ultra 2 es el smartwatch más robusto de Apple para exploradores y atletas de élite. Caja de titanio de 49mm, pantalla de 3000 nits y batería de 60 horas para los entornos más extremos.', 2500000, 'img/dispositivos/14 -  Apple_watch_ultra/p14-main.jpg', 1, 4),
        # Audio (cat 5)
        ('AirPods 3ra Generación In-Ear Bluetooth', 'Los AirPods de 3ra generación con diseño resistente al sudor y agua. Audio Espacial personalizado y estuche MagSafe los convierten en los compañeros perfectos para deporte y vida diaria.', 600000, 'img/dispositivos/10 - ipods_in_Ears/p10-main.jpg', 1, 5),
        ('AirPods Pro 3 Inalámbricos', 'Los AirPods Pro 3 con chip H2 mejorado y Cancelación Activa de Ruido de siguiente nivel. La función de Escucha activa los convierte en audífonos clínicos certificados con Audio Espacial envolvente.', 1500000, 'img/dispositivos/11 - Air_pods_s3/p11-main.jpg', 1, 5),
        ('AirPods Pro 2da Generación', 'Los AirPods Pro 2 con chip H2 y Cancelación Activa de Ruido 2x más potente. Audio Espacial dinámico personalizado y carga USB-C los hacen los audífonos más avanzados de Apple.', 700000, 'img/dispositivos/12 - Air_pods_pro_2/p12-main.jpg', 1, 5),
        # Merch (cat 6)
        ('Apple T-Shirt', 'Camiseta oficial de Apple Store en algodón premium 100% orgánico con logo bordado. Disponible en blanco, negro y azul. Edición limitada para verdaderos fans de la manzana.', 180000, 'img/dispositivos/15 - Apple_Tshirt/p15-main.jpg', 1, 6),
        ('Apple Pin Coleccionable', 'Pines coleccionables oficiales de Apple en metal de alta calidad con acabado brillante. Ideales para mochilas, chaquetas o vitrinas. Cada pin celebra los íconos más queridos del universo Apple.', 80000, 'img/dispositivos/16 - pines/p16-main.jpg.png', 1, 6),
        ('Apple Hoodie Buzo', 'Hoodie oficial de Apple en mezcla de algodón y poliéster reciclado premium con logo Apple bordado. La comodidad y el estilo Apple fusionados para los días más frescos.', 350000, 'img/dispositivos/17 - Apple_Hoodie/p17-main.jpg', 1, 6),
    ]

    cursor.executemany('''
        INSERT INTO dispositivos (nombre, descripcion, precio, url_imagen, id_marca, id_categoria) 
        VALUES (?, ?, ?, ?, ?, ?)
    ''', productos)

        # Galería: fotos adicionales por producto
        # Galería: fotos adicionales por producto
    galeria = [
        (1,  'img/dispositivos/1 - iphone_17_pro/p1-side.jpg'),
        (1,  'img/dispositivos/1 - iphone_17_pro/p1-back.jpg'),
        (2,  'img/dispositivos/2 - iphone_16_pro/p2-side.jpg'),
        (2,  'img/dispositivos/2 - iphone_16_pro/p2-back.jpg'),
        (3,  'img/dispositivos/3 - iphone_15_pro/p3-side.jpg'),
        (3,  'img/dispositivos/3 - iphone_15_pro/p3-back.jpg'),
        (4,  'img/dispositivos/4 - mackBook_Air_m2/p4-side.jpg'),
        (4,  'img/dispositivos/4 - mackBook_Air_m2/p4-back.jpg'),
        (5,  'img/dispositivos/5 - mackbook_14_m4/p5-side.jpg'),
        (5,  'img/dispositivos/5 - mackbook_14_m4/p5-back.jpg'),
        (6,  'img/dispositivos/6 - imac_24_m4/p6-side.jpg'),
        (6,  'img/dispositivos/6 - imac_24_m4/p6-back.jpg'),
        (7,  'img/dispositivos/7 - tablet_ipad_a16/p7-side.jpg'),
        (7,  'img/dispositivos/7 - tablet_ipad_a16/p7-back.jpg'),
        (8,  'img/dispositivos/8 - ipad_Air_m3/p8-side.jpg'),
        (8,  'img/dispositivos/8 - ipad_Air_m3/p8-back.jpg'),
        (9,  'img/dispositivos/9 - ipad_13_pulg/p9-side.jpg'),
        (9,  'img/dispositivos/9 - ipad_13_pulg/p9-back.jpg'),
        (10, 'img/dispositivos/13 - Apple_watch_s9/p13-side.jpg'),    # ID 10 = Watch S9
        (10, 'img/dispositivos/13 - Apple_watch_s9/p13-back.jpg'),
        (11, 'img/dispositivos/14 -  Apple_watch_ultra/p14-side.jpg'), # ID 11 = Watch Ultra
        (12, 'img/dispositivos/10 - ipods_in_Ears/p10-side.jpg'),      # ID 12 = AirPods 3ra
        (12, 'img/dispositivos/10 - ipods_in_Ears/p10-back.jpg'),
        (13, 'img/dispositivos/11 - Air_pods_s3/p11-side.jpg'),        # ID 13 = AirPods Pro 3
        (13, 'img/dispositivos/11 - Air_pods_s3/p11-back.jpg'),
        # ID 14 AirPods Pro 2: solo tiene main
        (15, 'img/dispositivos/15 - Apple_Tshirt/p15-black.jpg'),      # ID 15 = T-Shirt
        (15, 'img/dispositivos/15 - Apple_Tshirt/p15-blue.jpg'),
        # ID 16 Pin: solo tiene main
        (17, 'img/dispositivos/17 - Apple_Hoodie/p17-green.jpg'),      # ID 17 = Hoodie
    ]

    cursor.executemany('INSERT INTO imagenes_dispositivo (id_dispositivo, url_imagen) VALUES (?, ?)', galeria)
    
    conexion.commit()
    print("¡Base de datos 'MyApol' creada e inicializada exitosamente con datos!")

except Exception as e:
    print(f"Nota: Los datos ya existen o hubo un error: {e}")

# Cerrar la conexión
conexion.close()
