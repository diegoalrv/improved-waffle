import pandas as pd
import geopandas as gpd
import sqlite3

# Paso 1: Parametrizar los nombres de los archivos de entrada
excel_input = "./data/input/patentes_comerciales.xlsx"
sqlite_input = "./data/input/patentes_comerciales.db"

# Paso 2: Leer los archivos como DataFrames de Pandas
df_excel = pd.read_excel(excel_input)
conn = sqlite3.connect(sqlite_input)
query = "SELECT * FROM coordenadas"
df_sqlite = pd.read_sql(query, conn)
conn.close()

# Paso 3: Hacer el merge usando la columna "Direccion_completa" y "direccion"
merged_df = df_excel.merge(df_sqlite, left_on="Direccion_completa", right_on="direccion", how="inner")

# Paso 4: Generar un GeoDataFrame a partir de las columnas de latitud y longitud
from shapely import Point
points = [Point(row['longitud'], row['latitud']) for _, row in merged_df.iterrows()]
gdf = gpd.GeoDataFrame(merged_df, geometry=points)
gdf.drop_duplicates(subset=['rol'], inplace=True)

# Paso 5: Guardar el GeoDataFrame como GeoJSON
gdf.to_file("patentes_comerciales.geojson", driver='GeoJSON')