import sqlite3
import os

db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'database.db')
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

actualizaciones = [
    (1, "El innovador iPhone 15 presenta el nuevo diseño con Dynamic Island para alertas y Actividades en vivo. Captura cada momento con su cámara principal de 48 MP y disfruta de un rendimiento increíble gracias a la potencia del chip A16 Bionic y su elegante acabado en vidrio con color integrado."),
    (2, "Fabricado en titanio aeroespacial, el iPhone 15 Pro es más resistente y ligero que nunca. Su flamante chip A17 Pro te permite correr los juegos más exigentes de consola ofreciendo una experiencia inmersiva con gráficos impresionantes. Incluye botón de acción programable."),
    (3, "El iPhone 15 Pro Max es el epítome de la potencia y la elegancia. Además de su construcción de titanio premium y el nuevo chip A17 Pro, incorpora el nuevo lente periscópico de zoom óptico 5x, brindando a creativos y profesionales el sistema de cámaras más potente en la historia del iPhone."),
    (4, "Súper ligera. Súper revolucionaria. Con un peso envidiable, la nueva MacBook Air alberga el chip M3, diseñado para potenciar tanto tus rutinas de trabajo como las sesiones de juego gracias a un CPU de 8 núcleos y almacenamiento súper rápido. Totalmente silenciosa y 18h de batería."),
    (5, "Puro rendimiento para los profesionales. Con los procesadores M3 Pro y M3 Max, el límite del MacBook Pro no existe. Pantalla Liquid Retina XDR asombrosa, hasta 128GB de memoria unificada y gran variedad de puertos. La laptop más capaz del mercado hoy en día."),
    (6, "Tu espacio de trabajo en una sola pieza de arte deslumbrante. El nuevo iMac luce un diseño ultradelgado, pantalla Retina 4.5K de 24 pulgadas brillante y todo el poder del procesador M3. Viene acompañado de su teclado Magic Keyboard y Mouse a juego."),
    (7, "El iPad que todos aman. Potenciado por el chip A14 Bionic, su deslumbrante pantalla Liquid Retina de 10.9 pulgadas y compatibilidad con el Apple Pencil de primera generación. La mejor herramienta para estudiantes o disfrutar del entretenimiento de una forma inmersiva y colorida."),
    (8, "Ligero como el viento, potente como una Mac. El iPad Air incorpora ahora el increíble procesador M2, dando un salto astronómico en rendimiento. Es súper versátil y gracias la nueva cámara frontal Ultra Gran Angular, estarás siempre en el centro del encuadre."),
    (9, "El iPad definitivo asombra en todos los sentidos. El más delgado jamás creado que cuenta por primera vez con la asombrosa tecnología Ultra Retina XDR (OLED), dando unos negros y niveles de brillo incomparables. El nuevo e intimidante chip M4 lidera el camino de la IA."),
    (10, "El Apple Watch Series 9 viene más brillante y con nuevas formas mágicas de interactuar gracias al gesto Double Tap (Doble toque), ideal para usar sin manos. Monitoriza tu salud 24/7 y mantente en forma con la pantalla siempre activa."),
    (11, "Vuelve a sumergirte en el sonido. Los AirPods Pro ofrecen Cancelación Activa de Ruido el doble de potente, un modo de Audio Espacial dinámico asombroso, y una experiencia auditiva mágicamente personalizada. La carga USB-C es ahora un estándar en este modelo."),
    (12, "Llegamos a la era de la computación espacial. Las Apple Vision Pro revolucionan el panorama mezclando perfectamente el entorno digital con tu espacio físico con la magia del chip R1. Entra a las películas de forma interactiva y expande tu escritorio al infinito."),
    (13, "Prepárate para la máxima experiencia en el salón de tu hogar. El Apple TV 4K cuenta con resolución brillante hasta en Dolby Vision y audio espacial para películas, junto a acceso a todo el ecosistema de juegos de Apple Arcade desde tu TV principal."),
    (14, "Redefine cómo suena tu salón de estar con sonido inmersivo y audio espacial al instante. El diseño acústico de precisión del HomePod y el procesamiento computacional adaptan al instante su sonido a la ubicación, ideal para ser el centro de una casa inteligente con Siri."),
    (15, "Tan pequeño que casi desaparece en la mesa, pero un sonido de tal calidad y potencia en 360 grados que llena todo el recinto sin perder nitidez. Sirve estupendamente como un Hub central (centro de control) con la nueva App Casa de Apple."),
    (16, "No pierdas nunca tus objetos de valor. Conecta el AirTag en un llavero, bolso o maleta pequeña. Configúralo en un instante en el modo Encontrar (Find My) de iOS. Usa una pila barata intercambiable que te otorga hasta un año de uso continuo e ininterrumpible."),
    (17, "Eleva el nivel de expresión artística en tu iPad con esta herramienta indispensable. Cuenta con latencia nula y reconocimiento asombroso de la presión y la inclinación para hacer distintos grosores de línea o aplicar sombreados espectaculares igual un lápiz físico."),
    (18, "El aliado incondicional para quienes buscan productividad nivel computadora en el uso de iPad. Con un suave panel de apoyo de cantiléver (flotante), y sus teclas ligeras retro iluminadas que esconden debajo de sí un espacioso trackpad multiprestaciones.")
]

for item in actualizaciones:
    cursor.execute("UPDATE dispositivos SET descripcion = ? WHERE id = ?", (item[1], item[0]))

conn.commit()
conn.close()
print("Descripciones de productos actualizadas correctamente.")
