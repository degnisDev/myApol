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
    # ----------------------------------------------------
    # PRODUCTOS (Precios en COP aproximados)
    # id_marca=1 siempre es Apple
    # id_categoria: 1=Smartphones, 2=Computers, 3=Tablets, 4=Wearables, 5=Home, 6=Accessories, 7=Merch
    # ----------------------------------------------------
    productos = [
        # Smartphones (id_categoria=1)
        ('iPhone 15', 'El innovador iPhone 15 presenta el nuevo diseño con Dynamic Island para alertas y Actividades en vivo. Captura cada momento con su cámara principal de 48 MP y disfruta de un rendimiento increíble gracias a la potencia del chip A16 Bionic y su elegante acabado en vidrio con color integrado.', 3800000, '', 1, 1),
        ('iPhone 15 Pro', 'Fabricado en titanio aeroespacial, el iPhone 15 Pro es más resistente y ligero que nunca. Su flamante chip A17 Pro te permite correr los juegos más exigentes de consola ofreciendo una experiencia inmersiva con gráficos impresionantes. Incluye botón de acción programable.', 5200000, '', 1, 1),
        ('iPhone 15 Pro Max', 'El iPhone 15 Pro Max es el epítome de la potencia y la elegancia. Además de su construcción de titanio premium y el nuevo chip A17 Pro, incorpora el nuevo lente periscópico de zoom óptico 5x, brindando a creativos y profesionales el sistema de cámaras más potente en la historia del iPhone.', 6500000, '', 1, 1),
        
        # Computers (id_categoria=2)
        ('MacBook Air', 'Súper ligera. Súper revolucionaria. Con un peso envidiable, la nueva MacBook Air alberga el chip M3, diseñado para potenciar tanto tus rutinas de trabajo como las sesiones de juego gracias a un CPU de 8 núcleos y almacenamiento súper rápido. Totalmente silenciosa y 18h de batería.', 4900000, '', 1, 2),
        ('MacBook Pro', 'Puro rendimiento para los profesionales. Con los procesadores M3 Pro y M3 Max, el límite del MacBook Pro no existe. Pantalla Liquid Retina XDR asombrosa, hasta 128GB de memoria unificada y gran variedad de puertos. La laptop más capaz del mercado hoy en día.', 9500000, '', 1, 2),
        ('iMac', 'Tu espacio de trabajo en una sola pieza de arte deslumbrante. El nuevo iMac luce un diseño ultradelgado, pantalla Retina 4.5K de 24 pulgadas brillante y todo el poder del procesador M3. Viene acompañado de su teclado Magic Keyboard y Mouse a juego.', 7200000, '', 1, 2),
        
        # Tablets (id_categoria=3)
        ('iPad', 'El iPad que todos aman. Potenciado por el chip A14 Bionic, su deslumbrante pantalla Liquid Retina de 10.9 pulgadas y compatibilidad con el Apple Pencil de primera generación. La mejor herramienta para estudiantes o disfrutar del entretenimiento de una forma inmersiva y colorida.', 2400000, '', 1, 3),
        ('iPad Air', 'Ligero como el viento, potente como una Mac. El iPad Air incorpora ahora el increíble procesador M2, dando un salto astronómico en rendimiento. Es súper versátil y gracias la nueva cámara frontal Ultra Gran Angular, estarás siempre en el centro del encuadre.', 3500000, '', 1, 3),
        ('iPad Pro', 'El iPad definitivo asombra en todos los sentidos. El más delgado jamás creado que cuenta por primera vez con la asombrosa tecnología Ultra Retina XDR (OLED), dando unos negros y niveles de brillo incomparables. El nuevo e intimidante chip M4 lidera el camino de la IA.', 6000000, '', 1, 3),
        
        # Wearables (id_categoria=4)
        ('Apple Watch Series 9', 'El Apple Watch Series 9 viene más brillante y con nuevas formas mágicas de interactuar gracias al gesto Double Tap (Doble toque), ideal para usar sin manos. Monitoriza tu salud 24/7 y mantente en forma con la pantalla siempre activa.', 2100000, '', 1, 4),
        ('AirPods Pro', 'Vuelve a sumergirte en el sonido. Los AirPods Pro ofrecen Cancelación Activa de Ruido el doble de potente, un modo de Audio Espacial dinámico asombroso, y una experiencia auditiva mágicamente personalizada. La carga USB-C es ahora un estándar en este modelo.', 1300000, '', 1, 4),
        ('Apple Vision Pro', 'Llegamos a la era de la computación espacial. Las Apple Vision Pro revolucionan el panorama mezclando perfectamente el entorno digital con tu espacio físico con la magia del chip R1. Entra a las películas de forma interactiva y expande tu escritorio al infinito.', 18000000, '', 1, 4),
        
        # Home & Entertainment (id_categoria=5)
        ('Apple TV 4K', 'Prepárate para la máxima experiencia en el salón de tu hogar. El Apple TV 4K cuenta con resolución brillante hasta en Dolby Vision y audio espacial para películas, junto a acceso a todo el ecosistema de juegos de Apple Arcade desde tu TV principal.', 750000, '', 1, 5),
        ('HomePod', 'Redefine cómo suena tu salón de estar con sonido inmersivo y audio espacial al instante. El diseño acústico de precisión del HomePod y el procesamiento computacional adaptan al instante su sonido a la ubicación, ideal para ser el centro de una casa inteligente con Siri.', 1600000, '', 1, 5),
        ('HomePod mini', 'Tan pequeño que casi desaparece en la mesa, pero un sonido de tal calidad y potencia en 360 grados que llena todo el recinto sin perder nitidez. Sirve estupendamente como un Hub central (centro de control) con la nueva App Casa de Apple.', 550000, '', 1, 5),
        
        # Accessories (id_categoria=6)
        ('AirTag', 'No pierdas nunca tus objetos de valor. Conecta el AirTag en un llavero, bolso o maleta pequeña. Configúralo en un instante en el modo Encontrar (Find My) de iOS. Usa una pila barata intercambiable que te otorga hasta un año de uso continuo e ininterrumpible.', 180000, '', 1, 6),
        ('Apple Pencil', 'Eleva el nivel de expresión artística en tu iPad con esta herramienta indispensable. Cuenta con latencia nula y reconocimiento asombroso de la presión y la inclinación para hacer distintos grosores de línea o aplicar sombreados espectaculares igual un lápiz físico.', 650000, '', 1, 6),
        ('Magic Keyboard', 'El aliado incondicional para quienes buscan productividad nivel computadora en el uso de iPad. Con un suave panel de apoyo de cantiléver (flotante), y sus teclas ligeras retro iluminadas que esconden debajo de sí un espacioso trackpad multiprestaciones.', 1500000, '', 1, 6),
        
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
