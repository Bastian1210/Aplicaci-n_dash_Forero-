from dash import Dash, dash_table, dcc, html,Input, Output, callback
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.tools as tls
import plotly.graph_objs as go
from backend.granulometria import granulometria
import numpy as np
#from backend.cartaplasticidad import *

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

layout1 = dbc.Container([
    html.H1("Tabla de granulometria"),
    dash_table.DataTable(
        id='tabla_granulometria',
        columns=[
            {'name':'Malla','id':'Malla','editable':False},
            {'name':'Abertura','id':'Abertura','editable': False},
            {'name':'Retenido','id':'Retenido','editable': True},
            {'name':'Retenido_acum','id':'Retenido_acum','editable':False},
            {'name':'Pasa','id':'Pasa','editable':False},
            {'name':'Por_pasa','id':'Por_Pasa','editable':False},
        ],
        data=granulometria.to_dict('records')

    ),
    dcc.Graph(id='granulometria-plot')
])

# Nuevo diseño a agregar
layout2 = dbc.Container([
    html.H1("Carta de Plasticidad", style={'textAlign': 'center'}),
    dcc.Graph(id='plasticity-chart'),
    html.Label("Limite líquido:"),
    dcc.Input(id='ll-input', type='number', value=60),
    html.Label("Índice de plasticidad:"),
    dcc.Input(id='ip-input', type='number', value=40)
])

# Combinar el diseño original y el nuevo diseño
app.layout = dbc.Tabs([
    dbc.Tab(layout1, label='Tabla de Granulometría'),
    dbc.Tab(layout2, label='Carta de plasticidad'),
])

@callback(
    Output('tabla_granulometria','data'),
    [Input('tabla_granulometria','data')]
)

def update_grabulometria_table(rows):
    granulometria = pd.DataFrame(rows)
    granulometria["Retenido"]=granulometria["Retenido"].astype("int")
    granulometria["Retenido_acum"]=granulometria["Retenido"].cumsum()
    granulometria["Pasa"] = granulometria["Retenido"].sum()-granulometria["Retenido_acum"]
    granulometria["Por_pasa"]= round(granulometria["Pasa"]*100/granulometria["Retenido"].sum(),2)
    granulometria["Por_Pasa"]= round((granulometria["Pasa"] * 100 / granulometria["Retenido"].sum()) if granulometria["Retenido"].sum() != 0 else 0, 2)


    granulometria["Retenido"]=granulometria["Retenido"].astype(str)
    granulometria["Retenido_acum"]=granulometria["Retenido_acum"].astype(str)
    granulometria["Pasa"] = granulometria["Pasa"].astype(str)
    granulometria["Por_pasa"]=granulometria["Por_pasa"].astype(str)

    return granulometria.to_dict('records')


@app.callback(
    Output('granulometria-plot','figure'),
    [Input('tabla_granulometria','data')]
)
def update_chart(rows):
    granulometria = pd.DataFrame(rows)
    
    trace = go.Scatter(
        x=granulometria['Abertura'][0:11],
        y=granulometria['Por_pasa'][0:11],
        mode='lines',
        line=dict(color='black',width=2),
        name='Curva Granulometrica'
    )

    layout = go.Layout(
        title = 'Curva Granulometrica',
        xaxis = dict(
            title = 'Tamiz (mm)',
            type = 'log',
            autorange = True,
        ),
        yaxis = dict(
            title = 'Prcentaje Pasa Acumulado %',
            range = [0,100],
        )
    )

    return{'data':[trace],'layout': layout}



@app.callback(
    Output('plasticity-chart', 'figure'),
    [Input('ll-input', 'value'), Input('ip-input', 'value')]
)
def update_chart(Limite_liquido, Indice_plasticidad):
    x = np.array([0, 100])
    LineaA = 0.73 * (x - 20)
    LineaU = 0.9 * (x - 8)
    data = [
        go.Scatter(x=[Limite_liquido], y=[Indice_plasticidad], mode='markers', 
                   marker=dict(size=10, color='red', line=dict(width=2, color='black')), 
                   name="LL-IP"),
        go.Scatter(x=x, y=LineaA, mode='lines', line=dict(width=2, color='darkblue'), name="Linea A"),
        go.Scatter(x=x, y=LineaU, mode='lines', line=dict(width=2, color='black', dash='dot'), name="Linea U"),
        go.Scatter(x=[50, 50], y=[0, 80], mode='lines', line=dict(width=2, color='black'), name="LL=50"),
        go.Scatter(x=[15.78, 29.59], y=[7, 7], mode='lines', line=dict(width=2, color='red'), name="IP=7"),
        go.Scatter(x=[12.44, 25.48], y=[4, 4], mode='lines', line=dict(width=2, color='red'), name="IP=7")
    ]

    annotation1 = go.layout.Annotation(
    x=30,  
    y=60,  
    text="NO EXISTE",  
    showarrow=True,  
    arrowhead=7, 
    ax=0,  
    ay=0  
    )
    annotation2 = go.layout.Annotation(
    x=80,  
    y=20,  
    text="MH",  
    showarrow=True,  
    arrowhead=7,  
    ax=0,  
    ay=0  
    )
    annotation3 = go.layout.Annotation(
    x=20,  
    y=5.5,  
    text="CL-ML",  
    showarrow=True,  
    arrowhead=7,  
    ax=0,  
    ay=0  
    )
    annotation4 = go.layout.Annotation(
    x=70,  
    y=45,  
    text="CH",  
    showarrow=True,  
    arrowhead=7,  
    ax=0,  
    ay=0  
    )
    annotation5 = go.layout.Annotation(
    x=40,  
    y=25,  
    text="C L",  
    showarrow=True,  
    arrowhead=7, 
    ax=0,  
    ay=0  
    )
    annotation6 = go.layout.Annotation(
    x=40,  
    y=5.5,  
    text="ML",  
    showarrow=True,  
    arrowhead=7,  
    ax=0,  
    ay=0  
)

    layout2 = go.Layout(
        title="Carta de Plasticidad",
        xaxis=dict(title="Limite líquido"),
        yaxis=dict(title="Índice de plasticidad", range = [0,80]),
        legend=dict(orientation='h', x=0.3, y=1.15),
        margin=dict(l=40, r=20, b=40, t=60),
        plot_bgcolor='white',
        paper_bgcolor='lightgray',
        annotations=[annotation1,annotation2,annotation3,annotation4,annotation5,annotation6]
    )
    return {'data': data, 'layout': layout2}
    
if __name__ == "__main__":
    app.run_server(debug=True)
