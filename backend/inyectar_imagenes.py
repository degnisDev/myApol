import sqlite3
import os

# Conectar a la BD
db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'database.db')
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# URLs reales de los CDNs oficiales de Apple (Alta calidad, compresión WebP original)
imagenes_apple = [
    # Smartphones
    (1, "https://store.storeimages.cdn-apple.com/4668/as-images.apple.com/is/iphone-15-finish-select-202309-6-1inch-blue?wid=5120&hei=2880&fmt=p-jpg&qlt=80&.v=1692923777972"), # iPhone 15
    (2, "https://store.storeimages.cdn-apple.com/4668/as-images.apple.com/is/iphone-15-pro-finish-select-202309-6-1inch-bluetitanium?wid=5120&hei=2880&fmt=p-jpg&qlt=80&.v=1692846360609"), # iPhone 15 Pro
    (3, "https://store.storeimages.cdn-apple.com/4668/as-images.apple.com/is/iphone-15-pro-finish-select-202309-6-7inch-naturaltitanium?wid=5120&hei=2880&fmt=p-jpg&qlt=80&.v=1692845702708"), # iPhone 15 Pro Max
    
    # Computers
    (4, "https://store.storeimages.cdn-apple.com/4668/as-images.apple.com/is/mba13-midnight-select-202402?wid=904&hei=840&fmt=jpeg&qlt=90&.v=1708367688034"), # MacBook Air (Este ya lo usas en el Hero)
    (5, "https://store.storeimages.cdn-apple.com/4668/as-images.apple.com/is/mba13-midnight-select-202402?wid=904&hei=840&fmt=jpeg&qlt=90&.v=1708367688034"), # MacBook Air (Este ya lo usas en el Hero)
    (6, "https://store.storeimages.cdn-apple.com/4668/as-images.apple.com/is/imac-24-blue-selection-hero-202310?wid=904&hei=840&fmt=jpeg&qlt=90&.v=1697302573216"), # iMac
    
    # Tablets
    (7, "https://store.storeimages.cdn-apple.com/4668/as-images.apple.com/is/ipad-10th-gen-finish-select-202212-blue-wifi_FMT_WHH?wid=1280&hei=720&fmt=p-jpg&qlt=80&.v=1667592817345"), # iPad 10
    (8, "https://store.storeimages.cdn-apple.com/4668/as-images.apple.com/is/ipad-air-finish-select-gallery-202405-11inch-blue-wifi_FMT_WHH?wid=1280&hei=720&fmt=p-jpg&qlt=80&.v=1713304562013"), # iPad Air
    (9, "https://store.storeimages.cdn-apple.com/4668/as-images.apple.com/is/ipad-air-finish-select-gallery-202405-11inch-blue-wifi_FMT_WHH?wid=1280&hei=720&fmt=p-jpg&qlt=80&.v=1713304562013"), # iPad Air
    
    # Wearables & VR
    (10, "https://store.storeimages.cdn-apple.com/4668/as-images.apple.com/is/MQD83?wid=1144&hei=1144&fmt=jpeg&qlt=90&.v=1660803972361"), # Apple Watch (Misma imagen que AirPods por ahora)
    (11, "https://store.storeimages.cdn-apple.com/4668/as-images.apple.com/is/MQD83?wid=1144&hei=1144&fmt=jpeg&qlt=90&.v=1660803972361"), # AirPods Pro
    (12, "https://store.storeimages.cdn-apple.com/4668/as-images.apple.com/is/MQD83?wid=1144&hei=1144&fmt=jpeg&qlt=90&.v=1660803972361"), # Apple Vision Pro (Misma imagen que AirPods por ahora)
    
    # Home
    (13, "https://store.storeimages.cdn-apple.com/4668/as-images.apple.com/is/apple-tv-4k-hero-select-202210_FMT_WHH?wid=1280&hei=720&fmt=p-jpg&qlt=80&.v=1664896361164"), # Apple TV
    (14, "https://store.storeimages.cdn-apple.com/4668/as-images.apple.com/is/homepod-select-midnight-202210?wid=904&hei=840&fmt=jpeg&qlt=90&.v=1670557210097"), # HomePod
    (15, "https://store.storeimages.cdn-apple.com/4668/as-images.apple.com/is/homepod-mini-select-spacegray-202110?wid=904&hei=840&fmt=jpeg&qlt=90&.v=1632925510000"), # HomePod mini
    
    # Accesorios
    (16, "https://store.storeimages.cdn-apple.com/4668/as-images.apple.com/is/airtag-single-select-202104?wid=904&hei=840&fmt=jpeg&qlt=90&.v=1617761669000"), # AirTag
    (17, "https://store.storeimages.cdn-apple.com/4668/as-images.apple.com/is/MU8F2?wid=1144&hei=1144&fmt=jpeg&qlt=90&.v=1540596407165"), # Apple Pencil
    (18, "https://store.storeimages.cdn-apple.com/4668/as-images.apple.com/is/MWR53?wid=1144&hei=1144&fmt=jpeg&qlt=90&.v=1713933090623") # Magic Keyboard
]

for item in imagenes_apple:
    cursor.execute("UPDATE dispositivos SET url_imagen = ? WHERE id = ?", (item[1], item[0]))

conn.commit()
conn.close()

print("¡Imágenes HD de servidores Apple sincronizadas exitosamente en la Base de Datos!")
