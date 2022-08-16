from parametros import encuesta
from analisis import optimization
from dash import Dash, html, dcc
from waitress import serve
import plotly.express as px
import dash
import pandas as pd
from dash.dependencies import Input, Output, State
#from analisis import optimization

app = Dash(__name__)

# see https://plotly.com/python/px-arguments/ for more options

app.layout = html.Div([
    html.Div(children=[
        html.Br(),
        html.Label(encuesta['Pregunta 1']['text']),
        dcc.Dropdown(encuesta['Pregunta 1']['opc'],id='p1'),

        html.Br(),
        html.Label(encuesta['Pregunta 2']['text']),
        dcc.Dropdown(encuesta['Pregunta 2']['opc'],id='p2'),

        html.Br(),
        html.Label(encuesta['Pregunta 3']['text']),
        html.Br(),
        dcc.Input(value='Ingrese un valor', type='text',id='p3'),

        html.Br(),
        html.Label(encuesta['Pregunta 4']['text']),
        dcc.Dropdown(encuesta['Pregunta 4']['opc'],id='p4'),

        html.Br(),
        html.Label(encuesta['Pregunta 5']['text']),
        dcc.Dropdown(encuesta['Pregunta 5']['opc'],id='p5'),

        html.Br(),
        html.Label(encuesta['Pregunta 6']['text']),
        dcc.Dropdown(encuesta['Pregunta 6']['opc'],id='p6'),
        
        html.Br(),
        html.Label(encuesta['Pregunta 8']['text']),
        dcc.Dropdown(encuesta['Pregunta 8']['opc'],id='p8'),
        
        html.Br(),
        html.Label(encuesta['Pregunta 14']['text']),
        html.Br(),
        dcc.Input(value='Ingrese un valor', type='text',id='p14')
        

    ], style={'width':550}),

    html.Div(children=[html.Br(),
        html.Label(encuesta['Pregunta 7']['text']),
        dcc.Dropdown(encuesta['Pregunta 7']['opc'],id='p7'),
    

        html.Br(),
        html.Label(encuesta['Pregunta 9']['text']),
        dcc.Dropdown(encuesta['Pregunta 9']['opc'],id='p9'),

        html.Br(),
        html.Label(encuesta['Pregunta 10']['text']),
        dcc.Dropdown(encuesta['Pregunta 10']['opc'],id='p10'),

        html.Br(),
        html.Label(encuesta['Pregunta 11']['text']),
        dcc.Dropdown(encuesta['Pregunta 11']['opc'],id='p11'),

        html.Br(),
        html.Label(encuesta['Pregunta 12']['text']),
        dcc.Dropdown(encuesta['Pregunta 12']['opc'],id='p12'),

        html.Br(),
        html.Label(encuesta['Pregunta 13']['text']),
        dcc.Dropdown(encuesta['Pregunta 13']['opc'],id='p13'),
                       
        html.Button(id='submit-button-state', n_clicks=0, children='Submit'),
                          
        dcc.Graph(figure={}, id='pie_chart')
                       
        
                       


    ], style={'padding': 5, 'width':550, 'margin-left':40})
], style={'display': 'flex', 'flex-direction': 'row', 'marginTop': 40, 'margin-right':40, 'font-size':18, 'font-family':'helvetica'})


@app.callback(
    Output(component_id='pie_chart', component_property='figure'),
    [Input('submit-button-state', 'n_clicks')],
    [State(component_id='p4', component_property='value'),
    State(component_id='p5', component_property='value'),
    State(component_id='p6', component_property='value'),
    State(component_id='p7', component_property='value'),
    State(component_id='p8', component_property='value'), 
    State(component_id='p9', component_property='value'),
    State(component_id='p10', component_property='value'),
    State(component_id='p11', component_property='value'),
    State(component_id='p12', component_property='value'),
    State(component_id='p13', component_property='value')])
    

def analizar(n_clicks,p4,p5,p6,p7,p8,p9,p10,p11,p12,p13):
        if n_clicks > 0:
            x1 = ((encuesta['Pregunta 4']['opc']).index(p4) + 1)*100
            x2 = ((encuesta['Pregunta 5']['opc']).index(p5) + 1)*100
            x3 = ((encuesta['Pregunta 6']['opc']).index(p6) + 1)*100
            x4 = ((encuesta['Pregunta 7']['opc']).index(p7) + 1)*100
            x5 = ((encuesta['Pregunta 8']['opc']).index(p8) + 1)*100
            x6 = ((encuesta['Pregunta 9']['opc']).index(p9) + 1)*100
            x7 = ((encuesta['Pregunta 10']['opc']).index(p10) + 1)*100
            x8 = ((encuesta['Pregunta 11']['opc']).index(p11) + 1)*100
            x9 = ((encuesta['Pregunta 12']['opc']).index(p12) + 1)*100
            x10 = ((encuesta['Pregunta 13']['opc']).index(p13) + 1)*100

            score = (x1 + x2 + x3 + x4 + x5 + x6 + x7 + x8 + x9 + x10)// 4

            if score > 2700:
                score == 400
            elif score > 1800 and score < 2700:
                score == 300
            elif score > 900 and score < 1800:
                score == 200
            else:
                score == 100

            df = optimization(score)

            fig = px.pie(df, values='w', names = 'names',title='Portafolio Sugerido')
            return fig
        else:
            raise dash.exceptions.PreventUpdate


############## Resultado del portafolio

#portafolio = optimization()

if __name__ == '__main__':
    app.run_server(debug=True)
    
    