import pandas as pd
import geopandas as gpd

# Cargar el archivo
gdf = gpd.read_file('./data/output/pois_patentes_comerciales.geojson')
df = gdf[['type', 'name']]

# Definir palabras clave para cada categoría
keywords = {
    "Aprovisionamiento": ["rotiseria", "fruta", "tienda", "supermercado", "mercado", "comestible", "alimento", "abasto", "fruteria", "verduleria"],
    "Entretenimiento": ["pista","deport","discot","club","parque", "esparcimiento", "teatro", "recreo", "juego"],
    "Servicios": ["veter","fotocopia","belleza","limpieza","asesor","gimnasio","reparacion","banco", "peluqueria", "asesoria", "servicio", "consultoria", "peluquera", "cerrajeria"],
    "Comida para servir": ["postre","cafe","rest", "soda", "pizza", "pasteleria", "restaurante", "cocineria", "comida", "cafeteria", "bar", "cocina", "fast food"],
    "Comercio": ["prenda","perfume","comerc","regalo","bebidas","paqueteria", "cerveza","libreria","accesorios","cantina", "licor","alcohol", "comercia", "revista", "confiteria", "provision", "bazar", "repuesto", "venta", "comercio", "tienda", "boutique", "ropa", "zapato"],
    "Cuidados": ["dental","psicolo","quiroprac","pediatr","kine","radiografia","odonto","medico", "dentista", "salud", "hospital", "clinica", "farmacia", "laboratorio"],
    "Educacion": ["colegio", "liceo", "escuela", "universidad", "jardin", "academia", "instituto", "educacion"],
    "drop": ["moto","proyect","seguridad","ahorro","arquitectura","inversion","hostal","inmobiliaria","teleco","vehiculo","auto","capital","profesional","oficina","internet","investigacion","guardia","divisa","seguro","estacionamiento", "asistencia","personal","agencia","elaboracion", "hotel", "otras actividades", "import", "equipos", "maquinas", "administrat", "taller", "construccion"]
}

# Función para categorizar amenidades basándose en palabras clave
def categorize_amenity(name):
    for category, keys in keywords.items():
        for key in keys:
            if key in name.lower():
                return category
    return "No clasificado"

# Aplicar la función para categorizar cada amenidad en el DataFrame
df['category'] = df['name'].apply(categorize_amenity)

# Guardar el DataFrame con las categorías asignadas
df.to_csv('C:\\Users\\CityLab Biobio - DS\\Dev\\ds_ccp\\data\\input\\patentes_comerciales_amenities_labels.csv', index=False)
# print(df[df['category']=="No clasificado"].shape)
# print(df[df['category']!="No clasificado"].shape)
# print(df.shape)
# df[df['category']=="No clasificado"].to_csv('./data/output/no_class.csv', index=False)

