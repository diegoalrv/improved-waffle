import pandas as pd
import sqlite3
from geopy.geocoders import Nominatim
import multiprocessing
import logging
import hashlib
import os
import warnings

# Desactivar todas las advertencias
warnings.filterwarnings("ignore")


def generar_user_agent_hash():
    # Generar una cadena aleatoria de 16 bytes
    cadena_aleatoria = os.urandom(16)
    # Calcular el hash MD5 de la cadena aleatoria y convertirlo a una cadena hexadecimal
    user_agent_hash = hashlib.md5(cadena_aleatoria).hexdigest()
    return user_agent_hash

def geocodificar_direcciones(subconjunto):
    # Inicializar el geolocalizador
    geolocalizador = Nominatim(user_agent=generar_user_agent_hash(), timeout=10)
    
    # Conectar a la base de datos SQLite
    conn = sqlite3.connect('patentes_comerciales.db')

    for _, row in subconjunto.iterrows():
        direccion = row['Direccion_completa']
        try:
            ubicacion = geolocalizador.geocode(direccion)
            if ubicacion:
                latitud = ubicacion.latitude
                longitud = ubicacion.longitude
                # Agregar los resultados al DataFrame
                pd.DataFrame(
                    {'direccion': [direccion], 'latitud': [latitud], 'longitud': [longitud]}
                ).to_sql(
                    'coordenadas', conn, if_exists='append', index=False
                )
                logging.info(f"Registro guardado exitosamente: {direccion}")
            else:
                logging.warning(f"No se encontraron coordenadas para la dirección: {direccion}")
                # Registrar la dirección no encontrada en la tabla correspondiente
                cursor.execute("INSERT INTO direcciones_no_encontradas VALUES (?)", (direccion,))
        except Exception as e:
            logging.error(f"Error al geocodificar la dirección {direccion}: {e}")

    # Guardar los cambios en la base de datos y cerrar la conexión
    conn.commit()
    conn.close()

if __name__ == '__main__':
    # Configuración del registro de actividad
    logging.basicConfig(filename='registro_actividad.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    # Cargar el DataFrame desde el archivo Excel
    df = pd.read_excel('.\data\input\patentes_comerciales.xlsx')

    # Conectar a la base de datos SQLite
    conn = sqlite3.connect('patentes_comerciales.db')
    cursor = conn.cursor()

    # Crear una tabla para almacenar los datos si aún no existe
    cursor.execute('''CREATE TABLE IF NOT EXISTS coordenadas (
                        direccion TEXT,
                        latitud REAL,
                        longitud REAL
                    )''')

    # Crear una tabla para almacenar las direcciones que no se pudieron encontrar
    cursor.execute('''CREATE TABLE IF NOT EXISTS direcciones_no_encontradas (
                        direccion TEXT
                    )''')
    
    # Guardar los cambios en la base de datos y cerrar la conexión
    conn.commit()
    conn.close()

    todos_los_cores = True

    if todos_los_cores:
        # Dividir el DataFrame en subconjuntos para procesamiento paralelo
        num_procesadores = 4
    else:
        # En caso de querer usar todos los cores
        num_procesadores = multiprocessing.cpu_count()

    subconjuntos = [df[i:i + len(df) // num_procesadores] for i in range(0, len(df), len(df) // num_procesadores)]
    # Crear procesos para procesar los subconjuntos en paralelo
    procesos = []

    for subconjunto in subconjuntos:
        proceso = multiprocessing.Process(target=geocodificar_direcciones, args=(subconjunto,))
        procesos.append(proceso)
        proceso.start()

    # Esperar a que todos los procesos terminen
    for proceso in procesos:
        proceso.join()
