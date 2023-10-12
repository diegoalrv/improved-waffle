import pandas as pd
import sqlite3

# Conectar a la base de datos SQLite
conn = sqlite3.connect('patentes_comerciales.db')

# Consulta SQL para seleccionar todos los registros de la tabla "coordenadas"
consulta = "SELECT * FROM coordenadas"

# Leer los datos de la tabla "coordenadas" en un DataFrame
df_coordenadas = pd.read_sql_query(consulta, conn)

print(df_coordenadas)

# Cerrar la conexión a la base de datos
conn.close()