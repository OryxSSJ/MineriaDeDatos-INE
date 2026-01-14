import pandas as pd
import re

df = pd.read_csv(
    r"C:\Users\erick\Downloads\ProyectoMineríaDeDatos\datasetINE.csv",
    dtype=str,
    low_memory=False
)

def normalizar_nombres_columnas(columnas):
    return (
        columnas.str.replace('\n', ' ')
        .str.strip()
        .str.lower()
        .str.replace(r'\s+', ' ', regex=True)
    )

def encontrar_columna_por_patron(patrones, columnas):
    for patron in patrones:
        regex = re.compile(patron, re.IGNORECASE)
        coincidencias = [col for col in columnas if regex.search(col)]
        if coincidencias:
            return coincidencias[0]
    return None

df.columns = normalizar_nombres_columnas(df.columns)

COLUMNAS_OBJETIVO = {
    'entidad': [r'clave.*entidad'],
    'municipio': [r'clave.*municipio'],
    'nombre_mun': [r'nombre.*municipio', r'municipio.*nombre'],
    'seccion': [r'seccion']
}

columnas_identificadas = {
    key: encontrar_columna_por_patron(patrones, df.columns) 
    for key, patrones in COLUMNAS_OBJETIVO.items()
}

if not columnas_identificadas['nombre_mun']:
    print("Advertencia: Columna de municipio no encontrada. Creando dummy.")
    df['nombre municipio'] = 'Desconocido'
    columnas_identificadas['nombre_mun'] = 'nombre municipio'

jalisco = df[df[columnas_identificadas['entidad']] == '14'].copy()
jalisco = jalisco.rename(columns={
    columnas_identificadas['municipio']: 'clave municipio',
    columnas_identificadas['seccion']: 'seccion',
    columnas_identificadas['nombre_mun']: 'nombre municipio'
})

RANGOS_EDAD = {
    '18': '18',
    '19': '19',
    '20_24': '20-24',
    '25_29': '25-29',
    '30_34': '30-34',
    '35_39': '35-39',
    '40_44': '40-44',
    '45_49': '45-49',
    '50_54': '50-54',
    '55_59': '55-59',
    '60_64': '60-64',
    '65_y_mas': '65+'
}

def procesar_columna_numerica(df, prefijo, sufijos):
    resultados = {}
    for sufijo in sufijos:
        col_name = f'{prefijo}_{sufijo}'
        if col_name in df.columns:
            resultados[sufijo] = (
                df[col_name]
                .fillna('0')
                .str.replace(',', '')
                .astype(int)
            )
        else:
            print(f"Advertencia: {col_name} no encontrada. Usando ceros.")
            resultados[sufijo] = pd.Series(0, index=df.index)
    return resultados

sufijos = [f"{rango}_{sexo}" for rango in RANGOS_EDAD.keys() 
                         for sexo in ['hombres', 'mujeres']]

padrones = procesar_columna_numerica(jalisco, 'padron', sufijos)
listas = procesar_columna_numerica(jalisco, 'lista', sufijos)

data = []
for sufijo in sufijos:
    rango_key, sexo = sufijo.rsplit('_', 1)
    etiqueta_edad = RANGOS_EDAD[rango_key]
    
    df_temp = jalisco[['clave municipio', 'nombre municipio', 'seccion']].copy()
    df_temp['rango_edad'] = etiqueta_edad
    df_temp['sexo'] = sexo
    df_temp['total_padron'] = padrones[sufijo].values
    df_temp['total_lista'] = listas[sufijo].values
    
    data.append(df_temp)

df_final = pd.concat(data, ignore_index=True)

COLUMNAS_FINALES = [
    'clave municipio', 'nombre municipio', 'seccion',
    'rango_edad', 'sexo', 'total_padron', 'total_lista'
]
df_final = df_final[COLUMNAS_FINALES]

df_final.to_csv('datasetINE_preparado.csv', index=False)
print("Datos guardados exitosamente en 'datasetINE_preparado.csv'")