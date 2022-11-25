'''
 # @ Create Time: 2022-11-12 11:02:35.100389
'''

from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import pandas as pd
from PIL import Image
image = Image.open("Guadalajara.png")


app = Dash(__name__, title="InfraccionesGDL")

# Declare server for Heroku deployment. Needed for Procfile.
server = app.server

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
db = pd.read_csv("InfraccionesGDL_DB_v1.csv")
db['INFRACCIONES'] = db[['INFRACCION_1.0',
       'INFRACCION_4.0', 'INFRACCION_5.0']].sum(axis = 1)

db = db.loc[db['INFRACCIONES'] > 0]

db['INFRACCION'] = condition_1 = (db['INFRACCION_1.0'] == 1)
db.loc[condition_1, 'INFRACCION'] = 1

condition_4 = (db['INFRACCION_4.0'] == 1)
db.loc[condition_4, 'INFRACCION'] = 4

condition_5 = (db['INFRACCION_5.0'] == 1)
db.loc[condition_5, 'INFRACCION'] = 5

db = db.drop(columns = ["Unnamed: 0"])
db = db[['ESTADO', 'MARCA', 'CALLE', 'CRUCE', 'FECHA', 'ANO', 'MES',
         'HORA', 'HORA_NUM', 'LATITUD', 'LONGITUD', 'INFRACCION']]
db.FECHA = pd.to_datetime(db.FECHA)
db['DIAS'] = db.FECHA.dt.weekday
db = db.sort_values(by = 'INFRACCION')

app.layout = html.Div([
    html.Img(src=image, alt='SaturdaysAI_Logo', style={'height':'15%', 'width':'15%', 'margin-left': '73vh'}),
    html.H1("InfraccionesGDL", style={"textAlign":"center"}),
    html.H2("SaturdaysAI - 4ta Edición - Guadalajara", style={"textAlign":"center", }),
    html.H2("Equipo Morado", style={"textAlign":"center"}),
    html.P(" ", style={"textAlign":"center"}),

    html.H3("La educación vial de los conductores en la ZMG suele ser mala al estacionarse en lugares no permitidos como líneas amarillas, tomas para bomberos, lugares reservados para incapacitados entre otros, causando problemas a peatones y gente que requiera de una rampa para poder usar las banquetas. Y por otro lado, las infracciones tienen un impacto económico, ya que los automovilistas suelen omitir la tarifa de parquímetros en diferentes puntos de la ciudad.", style={"textAlign":"center"}),

    html.Table(className='table',
                children = 
                [
                    html.Tr([html.Th("Tipo de Infracción"), html.Th("Descripción")],style={'textAlign' : 'center'})
                ] +
                [
                    html.Tr([html.Td("Tipo 1"), html.Td("Omitir tarifa de parquímetro")],style={'textAlign' : 'center'}),
                    html.Tr([html.Td("Tipo 4"), html.Td(" Estacionarse en intersección o línea amarilla")],style={'textAlign' : 'center'}),
                    html.Tr([html.Td("Tipo 5"), html.Td("Estacionarse en lugares exclusivos, bomberos, policía, servicios médicos o personas con discapacidad")],style={'textAlign' : 'center'})
                ],  style={'margin-left': '42vh'}
            ),
           
    html.Hr(),
    html.P("Tipo de Infracción:",  style={"textAlign":"center"}),
    html.Div(html.Div([
        dcc.Dropdown(id='animal-type', clearable=False,
                     value=0,
                     options=[{'label': 'Tipo 1, 4 & 5', 'value': 0},
                      {'label': 'Tipo 1', 'value': 1},
                      {'label': 'Tipo 4', 'value': 4},
                      {'label': 'Tipo 5', 'value': 5}]),
    ],className="two columns"),className="row", style={'margin-left': '42vh', 'margin-right': '42vh'}),

    html.Div(id="output-div", children=[]),
])

@app.callback(Output(component_id="output-div", component_property="children"),
              Input(component_id="animal-type", component_property="value"),
)

def make_graphs(infraccion_chosen):
    
    if infraccion_chosen == 0:
        db_graphs = db
        infraccion_chosen_txt = "Todas las infracciones"
    else:
        db_graphs = db.loc[db.INFRACCION == infraccion_chosen]
        infraccion_chosen_txt = "Infracción de Tipo " + str(infraccion_chosen)
    
    # HISTOGRAM
    top10_estados = pd.DataFrame(index = db_graphs.ESTADO.value_counts().index[:10]).reset_index()
    top10_estados.columns = ['Estado']
    top10_estados['Conteo'] = db_graphs.ESTADO.value_counts()[:10].values
    
    fig_pie = px.pie(top10_estados, values = 'Conteo', names = 'Estado',
                 title = 'Top 10 Estados con más infracciones (2021 - 2022)',
                color_discrete_sequence=px.colors.qualitative.Bold,
                width=650, height=500)
    fig_pie.update_layout(title_x=0.5)

    # STRIP CHART
    vehiculos = pd.DataFrame(index = db_graphs.MARCA.value_counts()[:50].index).reset_index()
    vehiculos.columns = ['Marca del vehículo']
    vehiculos['Conteo'] = db_graphs.MARCA.value_counts()[:50].values
    
    fig_bar = px.bar(vehiculos, x = "Marca del vehículo", y = "Conteo",
             title = "Top 50 marcas de vehículos infraccionados (2021 - 2022)",
             color_discrete_sequence=px.colors.qualitative.Bold, text = 'Conteo',
             width=650, height=500)
    fig_bar.update_traces(textposition="inside", texttemplate='%{text:,}')
    fig_bar.update_layout(title_x=0.5)

    
    # INFRACCIONES POR DIA
    horas = pd.DataFrame(index = db_graphs.HORA_NUM.value_counts()[1:].index).reset_index()
    horas.columns = ['Hora']
    horas['Conteo'] = db_graphs.HORA_NUM.value_counts()[1:].values
    
    fig_horas = px.bar(horas, x = "Hora", y = "Conteo",
                 title = "Infracciones por hora del día (2021 - 2022)",
                 color_discrete_sequence=px.colors.qualitative.Prism, text = 'Conteo',
                 width=650, height=500)
    fig_horas.update_layout(xaxis={"dtick":1})
    fig_horas.update_traces(textposition="inside", texttemplate='%{text:,}')
    fig_horas.update_layout(title_x=0.5)

    
    # INFRACCIONES POR DIA
    dias = pd.DataFrame(index = db_graphs.DIAS.value_counts().index).reset_index()
    dias.columns = ['Dia de la semana de la Infracción']
    dias['Conteo'] = db_graphs.DIAS.value_counts().values
    dias = dias.sort_values(by = 'Dia de la semana de la Infracción')
    dias['Dia de la semana'] = ['Domingo', 'Lunes', 'Martes', 'Miercoles', 'Jueves', 
                                                 'Viernes', 'Sabado']
    
    fig_dias = px.line(dias, x = "Dia de la semana", y = "Conteo",
                 title = "Infracciones por día (2021 - 2022)",
                 color_discrete_sequence=px.colors.qualitative.Prism, text = 'Conteo',
                 width=650, height=500)
    fig_dias.update_traces(textposition="top center", texttemplate='%{text:,}')
    fig_dias.update_layout(title_x=0.5)



    # MAP
    fig_map = px.scatter_mapbox(db, lat="LATITUD", lon="LONGITUD",
                       mapbox_style="carto-positron", color = 'INFRACCION',
                       zoom=10, center = {"lat": 20.676820, "lon": -103.3418228},
                       opacity=0.5)
    



    return [

        html.Div(className='row', children=[
            html.Div(children=[
                html.H2(str(infraccion_chosen_txt), style={"textAlign":"center"}),
                dcc.Graph(figure=fig_bar, style={'display': 'inline-block'}),
                dcc.Graph(figure=fig_pie, style={'display': 'inline-block'})
                ]) 
            ]),
        
        html.Div(className='row', children=[
            html.Div(children=[
                dcc.Graph(figure=fig_dias, style={'display': 'inline-block'}),
                dcc.Graph(figure=fig_horas, style={'display': 'inline-block'})
                ]) 
            ]),
        
        
        html.H2("Mapa de Infracciones de la ZMG (2021 - 2022)", style={"textAlign":"center"}),
        html.Hr(),
        html.Div([
            html.Div([dcc.Graph(figure=fig_map)], className="six columns"),
        ], className="row"),
        
        html.P("La ZMG recibe alrededor de 1,000 infracciones al día, de las cuales solo alrededor del 10% son pagadas cada año. Este modelo está enfocado en dos principales metas: Una para el ciudadano conductor, donde a partir del Estado de su placa, Modelo de su carro, mes y hora donde se estacionará, y latitud y longitud del lugar; a partir de esto, se podrá hacer una valoración si entra en perfil estadístico de infracciones en la ciudad y estereotipos de conductores que el modelo aprendió. Por otro lado, beneficiará a la Entidad Pública, ya que a partir de este modelo se puede tener una proyección más certera, basada en el histórico, sobre las infracciones a futuro. A partir de estas predicciones, se pueden crear o proponer políticas públicas o programas sociales que incentiven una mejor cultura vial en la ciudad. A partir del análisis de estos datos podemos determinar cuáles serían las zonas más eficientes dónde agregar cajones de estacionamiento parkimovil o estacionamientos públicos. #LaCalleEsDeTodos",
               style={"textAlign":"right"}), 
    ]


if __name__ == '__main__':
    app.run_server(debug=True)
