import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import re

# ----------------------------------------------------------
# Función para cargar y procesar el CSV con nombres de archivo
# ----------------------------------------------------------
def load_data(file_path):
    """
    Carga datos desde CSV y extrae metadatos de la columna FileName:
    - Estructura: MON o DIM
    - Software: AF, RF, SM o MD
    - Proteína: NCChumano o NCCAnguila
    - Modelo base: dos dígitos
    - Nivel de relajación: Base o RelaxedX
    """
    df = pd.read_csv(file_path)
    print(f"Cargando: {file_path}")

    # Extraemos con expresiones regulares
    df['Structure'] = df['FileName'].str.extract(r'^(MON|DIM)')
    df['Software']  = df['FileName'].str.extract(r'-(AF|RF|SM|MD)')
    df['Protein']   = df['FileName'].str.extract(r'-(NCChumano|NCCAnguila)')
    df['ModelBase'] = df['FileName'].str.extract(r'-(\d{2})')
    df['Relaxed']   = df['FileName'].str.extract(r'-(Relaxed\d?)')
    df['Relaxed']   = df['Relaxed'].fillna('Base')  # Asigna 'Base' cuando no hay etiqueta Relaxed
    return df

# ----------------------------------------------------------
# Función para filtrar el DataFrame según inputs de usuario
# ----------------------------------------------------------
def filter_data(df, relaxed, structures, software, top_n, protein, models,
                relaxation_levels, all_models, models_per_software):
    """
    Aplica filtros seleccionados en la UI y ordena por Ramachandran.
    - Si all_models=False, agrupa por software y limita por models_per_software.
    """
    # Filtrado por nivel de relajación
    if relaxed:
        df = df[df['Relaxed'].isin(relaxation_levels)]
    # Estructura MON/DIM
    if structures:
        df = df[df['Structure'].isin(structures)]
    # Software
    if software:
        df = df[df['Software'].isin(software)]
    # Proteína
    if protein:
        df = df[df['Protein'].isin(protein)]
    # Modelos base
    if models:
        df = df[df['ModelBase'].isin(models)]

    # Si NO mostrar todos, ordena y agrupa por software
    if not all_models:
        df = df.sort_values(
            by=['Ramachandran Favored (>98%)',
                'Ramachandran Outliers (<0.05%)',
                'Ramachandran Z-Score (abs(ZScore)<2)'],
            ascending=[False, True, True]
        )
        df = df.groupby('Software').head(models_per_software)
    return df

# ----------------------------------------------------------
# Estadísticas: promedio y desviación estándar por software
# ----------------------------------------------------------
def calculate_statistics(df):
    stats = df.groupby('Software')['Ramachandran Favored (>98%)']\
              .agg(['mean', 'std']).reset_index()
    return stats

# ----------------------------------------------------------
# Carga inicial de datos
# ----------------------------------------------------------
file_path = 'RawData.csv'
df = load_data(file_path)

# ----------------------------------------------------------
# Inicialización de la aplicación Dash
# ----------------------------------------------------------
app = dash.Dash(__name__)
app.layout = html.Div([
    html.H1("Visualización de Ramachandran Favored"),
    # Filtros en UI: relaxed, estructura, software, proteína, modelo, relajación
    dcc.Checklist(id='relaxed-filter', options=[{'label': 'Incluir Relaxed', 'value': True}], value=[]),
    dcc.Dropdown(id='structure-filter', options=[{'label': s, 'value': s} for s in ['MON','DIM']], multi=True),
    dcc.Dropdown(id='software-filter', options=[{'label': s,'value': s} for s in ['AF','RF','SM','MD']], multi=True),
    dcc.Dropdown(id='protein-filter', options=[{'label': p,'value': p} for p in ['NCChumano','NCCAnguila']], multi=True),
    dcc.Dropdown(id='model-filter', options=[{'label': f"Modelo {m}",'value': m} for m in ['01','02','03','04','05']], multi=True),
    dcc.Dropdown(id='relaxation-filter', options=[
        {'label': lvl,'value': lvl} for lvl in ['Base','Relaxed1','Relaxed2','Relaxed3']
    ], multi=True),
    dcc.Checklist(id='all-models-filter', options=[{'label':'Mostrar todos','value': True}], value=[]),
    # Selección de colores por software
    html.Label("Selecciona colores por software:"),
    dcc.Input(id='color-af', type='text', placeholder='AF', value='blue'),
    dcc.Input(id='color-rf', type='text', placeholder='RF', value='green'),
    dcc.Input(id='color-sm', type='text', placeholder='SM', value='red'),
    dcc.Input(id='color-md', type='text', placeholder='MD', value='purple'),
    # Sliders para top_n y modelos por software
    dcc.Slider(id='top-n-filter', min=1, max=120, step=1, value=10,
               marks={i:str(i) for i in range(10,121,10)}),
    dcc.Slider(id='models-per-software-filter', min=1, max=20, step=1, value=5,
               marks={i:str(i) for i in range(1,11)}),
    # Gráficas
    dcc.Graph(id='bar-plot'),
    html.H2("Promedio y Desviación Estándar por Software"),
    dcc.Graph(id='box-plot')
])

# ----------------------------------------------------------
# Callback para actualizar gráficas según filtros
# ----------------------------------------------------------
@app.callback(
    [Output('bar-plot','figure'), Output('box-plot','figure')],
    [Input('relaxed-filter','value'), Input('structure-filter','value'),
     Input('software-filter','value'), Input('protein-filter','value'),
     Input('model-filter','value'), Input('relaxation-filter','value'),
     Input('all-models-filter','value'), Input('top-n-filter','value'),
     Input('models-per-software-filter','value'),
     Input('color-af','value'), Input('color-rf','value'),
     Input('color-sm','value'), Input('color-md','value')]
)
def update_graphs(relaxed, structures, software, protein, models,
                  relaxation_levels, all_models, top_n,
                  models_per_software, color_af, color_rf,
                  color_sm, color_md):
    # Convertimos a booleanos
    relaxed = bool(relaxed)
    all_models = bool(all_models)
    # Aplicamos filtro
    filtered_df = filter_data(df, relaxed, structures, software,
                              top_n, protein, models,
                              relaxation_levels, all_models,
                              models_per_software)

    # Mapa de colores dinámico
    color_map = {'AF': color_af, 'RF': color_rf,
                 'SM': color_sm, 'MD': color_md}

    # Gráfico de barras con líneas de referencia
    bar_fig = px.bar(filtered_df, x='FileName', y='Ramachandran Favored (>98%)',
                     color='Software', color_discrete_map=color_map,
                     pattern_shape='Protein',
                     range_y=[90, 100], title='Comparación de Ramachandran Favored')
    bar_fig.add_hline(y=98, line_dash='dash', line_color='red')

    # Estadísticas y box-plot
    stats_df = calculate_statistics(filtered_df)
    box_fig = px.box(filtered_df, x='Software', y='Ramachandran Favored (>98%)',
                     title='Distribución por Software')

    return bar_fig, box_fig

# ----------------------------------------------------------
# Ejecución de la app
# ----------------------------------------------------------
if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
