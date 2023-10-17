import geopandas as gpd
import pandas as pd
import numpy as np

pat = gpd.read_file("./data/output/patentes_comerciales.geojson")

translate = {
    'ROL': 'id',
    'TIPO': 'type',
    'ACTIVIDAD': 'name',
}
pat.rename(columns=translate, inplace=True)

pat['Category'] = 'Comercio'
pat['Source'] = 'SII'
pat['Subcategor'] = np.nan

pat_cols = list(translate.values()) + ['Category', 'Subcategor', 'Source', 'geometry']
pat = pat[pat_cols]

pat.to_file('./data/output/pois_patentes_comerciales.geojson', driver='GeoJSON')