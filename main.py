from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from weather.termodinamica import Termodinamica
from weather.radiacao import SaldoRadiacao
from weather.evapo import Evapo

app = Dash(__name__)

colors = {'background': '#111111', 'text': '#7FDBFF'}
# Altitude (m)
Z = 54
# Latitude (decimos de graus)
fi = -22.45
# Inicialização dos vetores
Patm = Tm = URm = es = ea = DPV = UA = US = Qesp = Rmix = Tpo = Dens = Lamb = Gama = Ses = []

#Coleta de dados
#folder_path = 'Data/'
folder_path = 'C:/Users/fernando.albani/Documents/Pessoal/Fernando/Mestrado Fernando/Projeto/Weather/weather/Data/'
df = pd.read_csv(folder_path + "DadosEvapo.txt",
                 delimiter='\s+',
                 index_col=False)
#Coleta de dados

rows = len(df)

Data = df.iloc[0:rows, 0:1]  # Data em valor numérico
Doy = df.iloc[0:rows, 1:2]  # Dia de ordem do ano/dia Juliano
Tx = df.iloc[0:rows, 2:3]  # Temperatura do ar máxima absoluta [oC]
Tn = df.iloc[0:rows, 3:4]  # Temperatura do ar mínima absoluta [oC]
Rs = df.iloc[0:rows, 4:5]  # Radiação solar global [MJ / m² d]
U2 = df.iloc[0:rows, 5:6]  # Velocidade do vento - 2m [m/s]
URx = df.iloc[0:rows, 6:7]  # Umidade relativa do ar máxima absoluta [%]
URn = df.iloc[0:rows, 7:8]  # Umidade relativa do ar mínima absoluta [%]
PCP = df.iloc[0:rows, 8:9]  # Precipitação total [mm]

termo = []
for i in range(0, rows):
  termo.append(
    Termodinamica(Tx.iloc[i].values, Tn.iloc[i].values, URx.iloc[i].values,
                  URn.iloc[i].values, Z))
resultado_termodinamica = pd.DataFrame(termo,
                                       columns=[
                                         'Patm', 'Tm', 'URm', 'es', 'ea',
                                         'DPV', 'UA', 'US', 'Qesp', 'Rmix',
                                         'Tpo', 'Dens', 'Lamb', 'Gama', 'Ses'
                                       ])

campo_data = pd.to_datetime(Data['Data'], format='%m/%d/%Y')
df['dia-mes'] = pd.to_datetime(Data['Data']).dt.strftime('%d/%m')

resultado_termodinamica = pd.concat([df['dia-mes'], resultado_termodinamica],
                                    axis=1,
                                    join='inner')
resultado_termodinamica = pd.concat([df['Tx'], resultado_termodinamica],
                                    axis=1,
                                    join='inner')
resultado_termodinamica = pd.concat([df['Tn'], resultado_termodinamica],
                                    axis=1,
                                    join='inner')
resultado_termodinamica.insert(0, 'dia-mes',
                               resultado_termodinamica.pop('dia-mes'))

resultado_termodinamica = pd.concat([URn['URn'], resultado_termodinamica],
                                    axis=1,
                                    join='inner')
resultado_termodinamica = pd.concat([URx['URx'], resultado_termodinamica],
                                    axis=1,
                                    join='inner')

# loop de cálculo Função radiação solar e terrestre e transformação em um DataFrame
radi = []
for i in range(0, rows):
  radi.append(
    SaldoRadiacao(Doy.iloc[i].values, fi, Z, Rs.iloc[i].values,
                  Tx.iloc[i].values, Tn.iloc[i].values,
                  resultado_termodinamica['ea'].iloc[i]))
resultado_radiacao = pd.DataFrame(radi, columns=['Rn', 'Rns', 'Rnl', 'Ra'])
resultado_radiacao = pd.concat([df['dia-mes'], resultado_radiacao],
                               axis=1,
                               join='inner')
resultado_radiacao = pd.concat([df['Rs'], resultado_radiacao],
                               axis=1,
                               join='inner')

# loop de cálculo Função Evapotranspiração e transformação em um DataFrame
evapo = []
for i in range(0, rows):
  evapo.append(
    Evapo(resultado_radiacao['Ra'].iloc[i], resultado_radiacao['Rn'].iloc[i],
          resultado_termodinamica['Tm'].iloc[i], Tx.iloc[i].values,
          Tn.iloc[i].values, resultado_termodinamica['es'].iloc[i],
          resultado_termodinamica['ea'].iloc[i],
          resultado_termodinamica['Lamb'].iloc[i],
          resultado_termodinamica['Gama'].iloc[i],
          resultado_termodinamica['Ses'].iloc[i], U2.iloc[i].values))
resultado_evapostranpiracao = pd.DataFrame(evapo, columns=['ETo_HS', 'ETo_PM'])
resultado_evapostranpiracao = pd.concat(
  [df['dia-mes'], resultado_evapostranpiracao], axis=1, join='inner')
resultado_evapostranpiracao = pd.concat(
  [PCP['P'], resultado_evapostranpiracao], axis=1, join='inner')
resultado_evapostranpiracao.insert(0, 'dia-mes',
                                   resultado_evapostranpiracao.pop('dia-mes'))

# criando o gráfico 01

a=list()
a.append("Todos os Gráficos")
a.append("Gráfico da Termodinâmica")
a.append("Gráfico da Evapotranspiração")
a.append("Gráfico de Umidade relativa")
a.append("Gráfico da velocidade do vento")
a.append("Gráfico do Balanço de Radiação")

fig1 = px.line(resultado_termodinamica, x="dia-mes", y="Tn")
fig1.update_traces(line=dict(color='rgba(2, 46, 250, 0.66)'))

fig2 = px.line(resultado_termodinamica, x="dia-mes", y="Tx")
fig2.update_traces(line=dict(color='rgba(255, 33, 40, 1)'))

fig3 = px.line(resultado_termodinamica, x="dia-mes", y="Tm")
fig3.update_traces(line=dict(color='rgba(0, 24, 255, 0.88)'))
fig3.update_layout(xaxis_title='Data', yaxis_title='Tar (oC)')

fig4 = go.Figure(data=fig1.data + fig2.data + fig3.data)
fig4['data'][0]['showlegend'] = True
fig4['data'][0]['name'] = 'Tn'
fig4['data'][1]['showlegend'] = True
fig4['data'][1]['name'] = 'Tx'
fig4['data'][2]['showlegend'] = True
fig4['data'][2]['name'] = 'Tm'
fig4.update_layout(xaxis_title='Data', yaxis_title='Tar (oC)',title_text="Gráfico da Termodinâmica",title_xanchor="center",title_x=0.5)
opcoes = list(df['dia-mes'].unique())
opcoes.append("Todos dias")

# criando o gráfico 02
fig5 = px.bar(resultado_evapostranpiracao, x="dia-mes", y="P")
fig5.update_traces(base=dict(color='rgba(2, 46, 250, 0.66)'))

fig6 = px.line(resultado_evapostranpiracao, x="dia-mes", y="ETo_HS")
fig6.update_traces(line=dict(color='rgba(2, 250, 15, 0.66)'))

fig7 = px.line(resultado_evapostranpiracao, x="dia-mes", y="ETo_PM")
fig7.update_traces(line=dict(color='rgba(255, 33, 40, 1)'))

fig8 = go.Figure(data=fig5.data + fig6.data + fig7.data)
fig8['data'][0]['showlegend'] = True
fig8['data'][0]['name'] = 'PCP'
fig8['data'][1]['showlegend'] = True
fig8['data'][1]['name'] = 'ETo_HS'
fig8['data'][2]['showlegend'] = True
fig8['data'][2]['name'] = 'ETo_PM'
fig8.update_layout(xaxis_title='Data', yaxis_title='ETo e Chuva (mm)',title_text="Gráfico da Evapotranspiração",title_xanchor="center",title_x=0.5)

#

# criando o gráfico 03
fig9 = px.line(resultado_termodinamica, x="dia-mes", y="URn")
fig9.update_traces(line=dict(color='rgba(2, 46, 250, 0.66)'))

fig10 = px.line(resultado_termodinamica, x="dia-mes", y="URm")
fig10.update_traces(line=dict(color='rgba(2, 250, 15, 0.66)'))

fig11 = px.line(resultado_termodinamica, x="dia-mes", y="URx")
fig11.update_traces(line=dict(color='rgba(255, 33, 40, 1)'))

fig12 = go.Figure(data=fig9.data + fig10.data + fig11.data)
fig12['data'][0]['showlegend'] = True
fig12['data'][0]['name'] = 'URn'
fig12['data'][1]['showlegend'] = True
fig12['data'][1]['name'] = 'URm'
fig12['data'][2]['showlegend'] = True
fig12['data'][2]['name'] = 'URx'
fig12.update_layout(xaxis_title='Data', yaxis_title='UR (%)',title_text="Gráfico de Umidade relativa",title_xanchor="center",title_x=0.5)

#

# criando o gráfico 04
fig13 = px.line(df, x="dia-mes", y="U2")
fig13.update_traces(line=dict(color='rgba(17, 4, 248, 0.78)'))

fig16 = go.Figure(data=fig13.data)
fig16['data'][0]['showlegend'] = True
fig16['data'][0]['name'] = 'U2'
fig16.update_layout(xaxis_title='Data', yaxis_title='U2 (m/s)',title_text="Gráfico da velocidade do vento",title_xanchor="center",title_x=0.5)
#
# criando o gráfico 05
fig17 = px.line(resultado_radiacao, x="dia-mes", y="Ra")
fig17.update_traces(line=dict(color='rgba(255, 33, 40, 1)'))

fig18 = px.line(resultado_radiacao, x="dia-mes", y="Rs")
fig18.update_traces(line=dict(color='rgba(17, 4, 248, 0.78)'))

fig19 = px.line(resultado_radiacao, x="dia-mes", y="Rn")
fig19.update_traces(line=dict(color='rgba(248, 4, 204, 0.78)'))

fig20 = go.Figure(data=fig17.data + fig18.data + fig19.data)
fig20['data'][0]['showlegend'] = True
fig20['data'][0]['name'] = 'Ra'
fig20['data'][1]['showlegend'] = True
fig20['data'][1]['name'] = 'Rs'
fig20['data'][2]['showlegend'] = True
fig20['data'][2]['name'] = 'Rn'
fig20.update_layout(xaxis_title='Data', yaxis_title='Radiação (M/m² d)',title_text="Gráfico do Balanço de Radiação",title_xanchor="center",title_x=0.5)


app.layout = html.Div(children=[
  html.H1(children='Relações psicrométricas e termodinâmicas'),
  html.Div(children='A web application framework for your data.',
           style={
             'textAlign': 'center',
           }),
  dcc.Dropdown(a, value='Todos os Gráficos', id='lista_grafico'),
  
  html.Div(id="graph1", children= [
  dcc.Graph(id='grafico_1', figure=fig4),
 ]),
  html.Div(id="graph2", children= [
  dcc.Graph(id='grafico_2', figure=fig8),
 ]),

  html.Div(id="graph3", children= [
  dcc.Graph(id='grafico_3', figure=fig12),
 ]),

  html.Div(id="graph4", children= [
  dcc.Graph(id='grafico_4', figure=fig16),
 ]),

  html.Div(id="graph5", children= [
  dcc.Graph(id='grafico_5', figure=fig20),
 ]),
    
   
])


@app.callback(Output('graph1', 'style'),
             
              [Input('lista_grafico','value')])
def hide_graph(value):
    if (value == "Todos os Gráficos") or (value == "Gráfico da Termodinâmica"):
      return {'display':'block'}
    else:
      return {'display':'none'}


@app.callback(Output('graph2', 'style'),
             
              [Input('lista_grafico','value')])
def hide_graph2(value):
    if (value == "Todos os Gráficos") or (value == "Gráfico da Evapotranspiração"):
      return {'display':'block'}
    else:
      return {'display':'none'}

@app.callback(Output('graph3', 'style'),
             [Input('lista_grafico','value')])
def hide_graph3(value):
    if (value == "Todos os Gráficos") or (value == "Gráfico de Umidade relativa"):
      return {'display':'block'}
    else:
      return {'display':'none'}
      
@app.callback(Output('graph4', 'style'),
             [Input('lista_grafico','value')])
def hide_graph4(value):
    if (value == "Todos os Gráficos") or (value == "Gráfico da velocidade do vento"):
      return {'display':'block'}
    else:
      return {'display':'none'}

@app.callback(Output('graph5', 'style'),
             [Input('lista_grafico','value')])
def hide_graph5(value):
    if (value == "Todos os Gráficos") or (value == "Gráfico do Balanço de Radiação"):
      return {'display':'block'}
    else:
      return {'display':'none'}

if __name__ == '__main__':
  app.run_server(host='0.0.0.0')

