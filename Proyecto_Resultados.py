import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_style("whitegrid")
df = pd.read_csv(r"C:\Users\erick\Downloads\ProyectoMineríaDeDatos\datasetINE_preparado.csv")

RANGO_A_VALOR = {'18': 18, '19': 19, '20-24': 22.5, '25-29': 27.5, '30-34': 32.5,
    '35-39': 37.5, '40-44': 42.5, '45-49': 47.5, '50-54': 52.5,
    '55-59': 57.5, '60-64': 62.5, '65+': 70}

MUNICIPIOS_ZMG = ['guadalajara', 'zapopan', 'tlaquepaque', 'tlajomulco de zúñiga', 
    'tonalá', 'el salto', 'ixtlahuacán de los membrillos', 
    'juanacatlán', 'zapotlanejo', 'acatlán de juárez']

df['nombre_normalizado'] = df['nombre municipio'].str.lower()

df_zmg = df[df['nombre_normalizado'].isin(MUNICIPIOS_ZMG)]
df_gdl = df[df['nombre_normalizado'] == 'guadalajara']

areas = {"Jalisco": df,
    "Zona Metropolitana de Guadalajara": df_zmg,
    "Guadalajara": df_gdl}

for nombre_area, data in areas.items():

    data = data.copy()
    data['edad_valor'] = data['rango_edad'].map(RANGO_A_VALOR)

    df_hombres = data[data['sexo'] == 'hombres']
    df_mujeres = data[data['sexo'] == 'mujeres']
    
    total_hombres = df_hombres['total_padron'].sum()
    total_mujeres = df_mujeres['total_padron'].sum()
    
    plt.figure(figsize=(10, 6))
    ax = plt.gca()
    bars = ax.bar(['Hombres', 'Mujeres'], 
                 [total_hombres, total_mujeres], 
                 color=['dodgerblue', 'lightcoral'],
                 width=0.6)

    for bar in bars:
        height = bar.get_height()
        ax.annotate(f'{height:,.0f}',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3),
                    textcoords="offset points",
                    ha='center', va='bottom',
                    fontsize=11, fontweight='bold')

    ax.set_title(f'Distribución por Sexo: {nombre_area}', 
                fontsize=16, fontweight='bold', pad=20)
    ax.set_ylabel('Total en Padrón Electoral', fontsize=12, labelpad=15)
    ax.set_xlabel('Sexo', fontsize=12, labelpad=10)

    ax.tick_params(axis='both', which='major', labelsize=11)
    ax.grid(axis='y', linestyle='--', alpha=0.7)

    ax.legend(bars, ['Hombres', 'Mujeres'], 
             loc='upper right', fontsize=11)

    plt.tight_layout()
    plt.subplots_adjust(top=0.9)
    plt.show()