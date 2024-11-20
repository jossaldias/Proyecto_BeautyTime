import django
import os

# EJECUTAR CON: python manage.py shell < populate_db.py

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'BT.settings')
django.setup()

from core.models import Categoria, Producto, Servicio

# Crear categorías
categorias = [
    {"id": 1, "nombre": "Peluqueria"},
    {"id": 2, "nombre": "Corporal"},
    {"id": 3, "nombre": "Uñas"},
    {"id": 4, "nombre": "Shampoo & Acondicionadores"},
    {"id": 5, "nombre": "Tratamientos"},
    {"id": 6, "nombre": "Maquillaje para eventos"}
]

# Insertar categorías en la base de datos
for categoria in categorias:
    Categoria.objects.create(id=categoria["id"], nombre=categoria["nombre"])

print("Categorías cargadas exitosamente!")

# Crear productos
productos_data = [
    {
        "nombre": "Deep Conditioner (New) 200GR",
        "descripcion": "INGREDIENTES\r\nJUVEXIN Una mezcla de proteínas antienvejecimiento de queratina que restaura el\r\ncabello de adentro hacia afuera y lo devuelve a su estado más juvenil. Protege el cabello\r\ndel daño futuro y los efectos del medio ambiente creando un escudo protector en cada\r\nhebra del cabello.\r\nAGENTES ANTIESTÁTICOS Cubren el cabello con una capa hidrante.\r\nEXTRACTOS NATURALES DE GRANOS Estas proteínas naturales protegen cada hebra\r\ndel cabello contra el daño.\r\nACEITES NATURAL DE SEMILLAS DE JOJOBA Hidratan\r\nal cabello para dejarlo más nutrido y acondicionado.\r\n\r\nCARACTERÍSTICAS\r\n• Reconstruye el daño\r\n• Penetra la corteza capilar para fortalecer y reparar\r\nde adentro hacia afuera\r\n• Nutre y fortalece el cabello con Juvexin\r\n\r\nBENEFICIOS\r\n• Fortalece el cabello debilitado por tratamientos químicos,\r\npeinados con calor o contaminación ambiental\r\n• Suaviza la superficie del cabello sellando las cutículas\r\n\r\nMODO DE USO\r\nLavar el cabello con el pH+ Shampoo de GKhair. Si el cliente ha recibido el tratamiento alisador GK Hair Hair Taming, debe utilizar cualquier champú de GK Hair que no sea el +pH Shampo. Aplicar GK Hair Deep Conditioner sobre el cabello húmedo, cubrir de manera uniforme y dejar actuar durante 20 minutos (con el cabello tapado) bajo el secador de casco.  Enjuagar bien y peinar como desee para sentir los resultados de la transformación.",
        "categoria_id": 4,
        "costo": 43333,
        "costo2": 36833,
        "cantidad": 199,
        "picture": "media/items/Captura_de_pantalla_2024-10-30_a_las_10.12.38a.m._rSQIfsk.png",
        "descuento": 15.00,
        "tipo": "producto",
    },
    {
        "nombre": "Moisturizing Shampoo Color Protection 300ml",
        "descripcion": "JUVEXIN Una mezcla de proteínas antienvejecimiento de queratina que restaura el cabello de adentro hacia afuera y lo devuelve a su estado más juvenil. Protege el cabello del daño futuro y los efectos del medio ambiente creando un escudo protector en cada hebra del cabello.\r\nACEITE NATURAL DE SEMILLAS Aceptados al 100% por el cabello. Hidratan el cabello para dejarlo acondicionado y nutrido.\r\nEXTRACTO DE PLANTAS Calma y equilibra el cabello de tipo normal a seco. Proporciona\r\nuna suave y natural hidratación mientras restaura los niveles de pH.\r\nEXTRACTOS DE GRANOS NATURALES Estas proteínas naturales fortalecen el cabello para proteger cada hebra del daño.",
        "categoria_id": 5,
        "costo": 28000,
        "costo2": 28000,
        "cantidad": 149,
        "picture": "media/items/moisturizing-Shampoo-300ML-BLyho6Tjk_1_1024x10242x.webp",
        "descuento": 0.09,
        "tipo": "producto",
    },
    {
        "nombre": "Balancing Conditioner 300ml",
        "descripcion": "Después de usar GKhair Balancing Shampoo, Balancee y acondicione tipos de cabello de normal a graso con GKhair Balancing Conditioner. El cabello se nutre con extractos de plantas. Libre de SLS ,SLES y fórmula Sodium Chloride que preserva y protege GKhair Oil Hair Color y GKhair light tame, Light Wave, Medium Tame-Curly y formulas Full Tame-Resistant .",
        "categoria_id": 4,
        "costo": 27000,
        "costo2": 27000,
        "cantidad": 200,
        "picture": "media/items/Balancing_Conditioner_300ml.png",
        "descuento": 0.00,
        "tipo": "producto",
    },
    {
        "nombre": "Silver Bombshell Shampoo 280ML",
        "descripcion": "JUVEXIN Una mezcla de proteínas antienvejecimiento de queratina que restaura el cabello de adentro hacia afuera y lo devuelve a su estado más juvenil. Protege el cabello del daño futuro y los efectos del medio ambiente creando un escudo protector en cada hebra del cabello.\r\nACEITE NATURAL DE SEMILLAS Aceptado al 100% por el cabello, hidrata y deja el cabello acondicionado y nutrido.\r\nEXTRACTOS NATURALES DE PLANTAS Calma y humecta el cabello de normal a seco. Proporciona una humectación natural.\r\nEXTRACTOS DE GRANOS NATURALES Estas proteínas naturales fortalecen el cabello para proteger cada hebra del daño.",
        "categoria_id": 4,
        "costo": 28000,
        "costo2": 26600,
        "cantidad": 100,
        "picture": "media/items/Silver_Bombshell_Shampoo_280ML.png",
        "descuento": 5.00,
        "tipo": "producto",
    },
    {
        "nombre": "PH+ Clarifying Shampoo 100ML",
        "descripcion": "Diseñado para funcionar como un pre-tratamiento para Hair Taming System Light Tame, Light Wave, Curly o Resistant formula. Este champú clarificante abre las cutículas del cabello para eliminar el exceso de productos y las impurezas acumuladas. Este esencial paso permite que Hair Taming System Light Tame, Light Wave, Curly o Resistant formula se apliquen apropiadamente.",
        "categoria_id": 4,
        "costo": 9900,
        "costo2": 9900,
        "cantidad": 100,
        "picture": "media/items/ph_Shampoo-100ml_1024x10242x.webp",
        "descuento": 0.00,
        "tipo": "producto",
    },
    {
        "nombre": "Dry Shampoo Spray 219ML",
        "descripcion": "El Shampoo seco GKhair absorbe el exceso de aceite y separa los mechones de cabello al tiempo que agrega volumen a las raíces y crea un aspecto recién lavado. Con almidón Natural Plants & Grain, este champú seco para cabello graso evita la acumulación de caspa y la descamación para dejar el cabello sin frizz y nutrido.",
        "categoria_id": 4,
        "costo": 15990,
        "costo2": 11992,
        "cantidad": 60,
        "picture": "media/items/Dry_Shampoo_Spray_219ML.png",
        "descuento": 25.00,
        "tipo": "producto",
    },
    {
        "nombre": "Moisturizing Shampoo Color Protection 100",
        "descripcion": "GKhair Moisturizing Shampoo está compuesto por ACEITES DE SEMILLAS NATURALES, EXTRACTOS DE GRANOS DE PLANTA Y AMB; limpia suavemente el cabello seco y dañado y fortalece cada hebra con proteínas naturales mientras hidrata y suaviza el cabello. Con una función adicional de protección del color enriquecida con Juvexin, una combinación de proteínas antiedad que restaura el cabello de adentro hacia afuera, devolviéndolo a un estado más juvenil. Compre ahora GKhair Moisturizing Shampoo para cabello seco para hidratar el cabello y proteger el color.",
        "categoria_id": 4,
        "costo": 9900,
        "costo2": 9900,
        "cantidad": 49,
        "picture": "media/items/moisturizing_Shampoo_100ml_1024x10242x.webp",
        "descuento": 0.00,
        "tipo": "producto",
    }
]

# Insertar productos en la base de datos
for producto in productos_data:
    categoria = Categoria.objects.get(id=producto["categoria_id"])
    Producto.objects.create(
        nombre=producto["nombre"],
        descripcion=producto["descripcion"],
        categoria=categoria,
        costo=producto["costo"],
        costo2=producto["costo2"],
        cantidad=producto["cantidad"],
        picture=producto["picture"],
        descuento=producto["descuento"],
        tipo=producto["tipo"]
    )

print("Productos cargados exitosamente!")

# Crear servicios
servicios_data = [
    # Peluquería
    {
        "nombre": "Corte de Cabello",
        "descripcion": "Transforma tu estilo con un corte de cabello personalizado. Nuestros expertos estilistas se asegurarán de realzar tu imagen con técnicas modernas y adaptadas a tu tipo de rostro y preferencias.",
        "categoria_id": 1,
        "costo": 25000,
        "costo2": 23000,
        "duracion": 60,
        "descuento": 0.00,
        "picture": "media/items/corte_pelo.png",
        "tipo": "servicio",
    },
    {
        "nombre": "Baño de Color",
        "descripcion": "Dale vida y brillo a tu cabello con nuestro baño de color. Ideal para quienes buscan un cambio sutil o reforzar su tono natural, dejándolo brillante y revitalizado.",
        "categoria_id": 1,
        "costo": 30000,
        "costo2": 28000,
        "duracion": 60,
        "descuento": 0.00,
        "picture": "media/items/baño_color.png",
        "tipo": "servicio",
    },
    {
        "nombre": "Tinturado",
        "descripcion": "Exprésate con un nuevo color vibrante. Nuestro servicio de tinturado incluye tonos clásicos y modernos para lograr el look que deseas, cuidando la salud de tu cabello.",
        "categoria_id": 1,
        "costo": 40000,
        "costo2": 36000,
        "duracion": 60,
        "descuento": 0.00,
        "picture": "media/items/Coloracion3.png",
        "tipo": "servicio",
    },
    {
        "nombre": "Balayage",
        "descripcion": "Consigue un look natural y sofisticado con nuestra técnica de balayage. Diseñado para iluminar tu cabello de manera gradual, aportando brillo y frescura a tu estilo.",
        "categoria_id": 1,
        "costo": 50000,
        "costo2": 45000,
        "duracion": 60,
        "descuento": 0.00,
        "picture": "media/items/balayage.jpg",
        "tipo": "servicio",
    },
    {
        "nombre": "Highlights",
        "descripcion": "Añade dimensión y luminosidad a tu cabello con mechas perfectamente colocadas. Este servicio destaca tus rasgos faciales y realza tu color natural.",
        "categoria_id": 1,
        "costo": 45000,
        "costo2": 41000,
        "duracion": 60,
        "descuento": 0.00,
        "picture": "media/items/highlights.png",
        "tipo": "servicio",
    },
    {
        "nombre": "Brushing",
        "descripcion": "Luce un peinado impecable y profesional. Desde alisados hasta ondas suaves, nuestro servicio de brushing es perfecto para cualquier ocasión especial o para sentirte increíble en tu día a día.",
        "categoria_id": 1,
        "costo": 20000,
        "costo2": 18000,
        "duracion": 60,
        "descuento": 0.00,
        "picture": "media/items/brushing.jpg",
        "tipo": "servicio",
    },
    {
        "nombre": "Maquillaje",
        "descripcion": "Resalta tu belleza con un maquillaje profesional diseñado para cualquier evento. Desde looks naturales hasta glamurosos, nuestros expertos te ayudarán a lucir espectacular.",
        "categoria_id": 1,
        "costo": 25000,
        "costo2": 23000,
        "duracion": 60,
        "descuento": 0.00,
        "picture": "media/items/Maquillaje3.png",
        "tipo": "servicio",
    },
    # Corporal
    {
        "nombre": "Masajes relajantes",
        "descripcion": "Alivia el estrés y renueva tu energía con un masaje relajante. Este servicio está diseñado para desconectar tu mente y relajar profundamente tu cuerpo.",
        "categoria_id": 2,
        "costo": 30000,
        "costo2": 28000,
        "duracion": 60,
        "descuento": 0.00,
        "picture": "media/items/masaje_relajante.jpg",
        "tipo": "servicio",
    },
    {
        "nombre": "Masajes descontracturantes",
        "descripcion": "Libera tensiones acumuladas con un masaje descontracturante. Ideal para quienes sufren molestias musculares debido a posturas incorrectas o esfuerzo físico.",
        "categoria_id": 2,
        "costo": 35000,
        "costo2": 32000,
        "duracion": 60,
        "descuento": 0.00,
        "picture": "media/items/masajes_descontracturantes.jpg",
        "tipo": "servicio",
    },
    {
        "nombre": "Masajes reductivos",
        "descripcion": "Define tu figura y reduce medidas con nuestro masaje reductivo. Ayuda a estimular la circulación y eliminar la acumulación de líquidos en áreas específicas.",
        "categoria_id": 2,
        "costo": 40000,
        "costo2": 37000,
        "duracion": 60,
        "descuento": 0.00,
        "picture": "media/items/masajes_reductivos.png",
        "tipo": "servicio",
    },
    {
        "nombre": "Masajes deportivos",
        "descripcion": "Recupera y prepara tu cuerpo con un masaje deportivo. Perfecto para deportistas, alivia la tensión muscular y mejora el rendimiento físico.",
        "categoria_id": 2,
        "costo": 45000,
        "costo2": 42000,
        "duracion": 60,
        "descuento": 0.00,
        "picture": "media/items/masajes_deportivos.jpg",
        "tipo": "servicio",
    },
    {
        "nombre": "Limpiezas faciales",
        "descripcion": "Cuida tu piel con una limpieza facial profunda. Este tratamiento elimina impurezas, hidrata y deja tu rostro radiante y saludable.",
        "categoria_id": 2,
        "costo": 25000,
        "costo2": 23000,
        "duracion": 60,
        "descuento": 0.00,
        "picture": "media/items/limpiezas_faciales.jpg",
        "tipo": "servicio",
    },
    {
        "nombre": "Depilación tradicional (cera)",
        "descripcion": "Disfruta de una piel suave y libre de vello con nuestra depilación tradicional con cera. Este método es rápido, efectivo y adecuado para todo tipo de piel.",
        "categoria_id": 2,
        "costo": 15000,
        "costo2": 14000,
        "duracion": 60,
        "descuento": 0.00,
        "picture": "media/items/depilacion_tradicional.jpg",
        "tipo": "servicio",
    },
    # Uñas
    {
        "nombre": "Servicios de esmaltados",
        "descripcion": "Dale color a tus uñas con nuestros servicios de esmaltado. Ofrecemos una amplia gama de colores y acabados para que siempre luzcas impecable.",
        "categoria_id": 3,
        "costo": 10000,
        "costo2": 9000,
        "duracion": 60,
        "descuento": 0.00,
        "picture": "media/items/esmaltados.jpg",
        "tipo": "servicio",
    },
    {
        "nombre": "Soft gel",
        "descripcion": "Realza tus uñas con nuestro servicio de soft gel. Este tratamiento ofrece una apariencia natural y resistente, ideal para quienes buscan un look sofisticado.",
        "categoria_id": 3,
        "costo": 20000,
        "costo2": 18000,
        "duracion": 60,
        "descuento": 0.00,
        "picture": "media/items/soft_gel.jpg",
        "tipo": "servicio",
    },
    {
        "nombre": "Manicura",
        "descripcion": "Cuida tus manos con nuestra manicura completa. Incluye limpieza, hidratación y esmaltado para que tus uñas luzcan elegantes y saludables.",
        "categoria_id": 3,
        "costo": 15000,
        "costo2": 14000,
        "duracion": 60,
        "descuento": 0.00,
        "picture": "media/items/manicura.jpg",
        "tipo": "servicio",
    }
]

# Insertar servicios en la base de datos
for servicio in servicios_data:
    categoria = Categoria.objects.get(id=servicio["categoria_id"])
    Servicio.objects.create(
        nombre=servicio["nombre"],
        descripcion=servicio["descripcion"],
        categoria=categoria,
        costo=servicio["costo"],
        costo2=servicio["costo2"],
        duracion=servicio["duracion"],
        descuento=servicio["descuento"],
        picture=servicio["picture"],
        tipo=servicio["tipo"]
    )

print("Servicios cargados exitosamente!")

