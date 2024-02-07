from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
#from weather.myproject.api.views import retornaDados
from requisicao import retornaDados


app = Dash(__name__)

colors = {'background': '#111111', 'text': '#7FDBFF'}
# Altitude (m)
Z = 54
# Latitude (decimos de graus)
fi = -22.45
# Inicialização dos vetores
Patm = Tm = URm = es = ea = DPV = UA = US = Qesp = Rmix = Tpo = Dens = Lamb = Gama = Ses = []

#Coleta de dados
url = 'http://127.0.0.1:8000/evapotranspiracaoservice?query=evapotransp&estacao=1&inicio=12/12/2023&fim=31/12/2023&pagina=1'
#if dados["next"] != None:
        #proximapagina = dados["next"]



dados_json = retornaDados(url)
dados = []
if dados_json != "":
    termo = []
    radi = []
    while dados_json["next"] !=None:
        dados.append(dados_json)
        dados_json = retornaDados(dados_json["next"])
    df = pd.DataFrame(dados)
        
    for dado in dados:
        termodinamica = dado['termodinamica']
        termo.append(termodinamica['Patm'])
        termo.append(termodinamica['Tm'])
        termo.append(termodinamica['URm'])
        termo.append(termodinamica['es'])
        termo.append(termodinamica['ea'])
        termo.append(termodinamica['DPV'])
        termo.append(termodinamica['UA'])
        termo.append(termodinamica['US'])
        termo.append(termodinamica['Qesp'])
        termo.append(termodinamica['Rmix'])
        termo.append(termodinamica['Tpo'])
        termo.append(termodinamica['Dens'])
        termo.append(termodinamica['Lamb'])
        termo.append(termodinamica['Gama'])
        termo.append(termodinamica['Ses'])
        
        radiacao = dado['saldoradiacao']
        radi.append(radiacao['Rn'])
        radi.append(radiacao['Rns'])
        radi.append(radiacao['Rnl'])
        radi.append(radiacao['Ra'])
        
        
    
    resultado_termodinamica = pd.DataFrame(termo,
                                       columns=[
                                         'Patm', 'Tm', 'URm', 'es', 'ea',
                                         'DPV', 'UA', 'US', 'Qesp', 'Rmix',
                                         'Tpo', 'Dens', 'Lamb', 'Gama', 'Ses'
                                       ])
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

    resultado_termodinamica = pd.concat([df['URn'], resultado_termodinamica],
                                        axis=1,
                                        join='inner')
    resultado_termodinamica = pd.concat([df['URx'], resultado_termodinamica],
                                        axis=1,
                                        join='inner')    
    resultado_radiacao = pd.DataFrame(radi, columns=['Rn', 'Rns', 'Rnl', 'Ra'])
    resultado_radiacao = pd.concat([df['dia-mes'], resultado_radiacao],
                               axis=1,
                               join='inner')
    resultado_radiacao = pd.concat([df['Rs'], resultado_radiacao],
                               axis=1,
                               join='inner')



# criando o gráfico 01

a=list()
a.append("Todos os Gráficos")
a.append("Gráfico da Termodinâmica")
a.append("Gráfico da Evapotranspiração")
a.append("Gráfico de Umidade relativa")
#a.append("Gráfico da velocidade do vento")
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


app.layout = html.Div(children=[
  html.H1(children='Relações psicrométricas e termodinâmicas'),
  html.Div(children='A web application framework for your data.',
           style={
             'textAlign': 'center',
           }),
  dcc.Dropdown(a, value='Todos os Gráficos', id='lista_grafico'),
  
  html.Div(id="graph1", children= [
  dcc.Graph(id='grafico_1', figure=fig4),
 ])
  #html.Div(id="graph2", children= [
  #dcc.Graph(id='grafico_2', figure=fig8),
 #]),

  #html.Div(id="graph3", children= [
  #dcc.Graph(id='grafico_3', figure=fig12),
 #]),

  #html.Div(id="graph4", children= [
  #dcc.Graph(id='grafico_4', figure=fig16),
 #]),

  #html.Div(id="graph5", children= [
  #dcc.Graph(id='grafico_5', figure=fig20),
 #]),
    
   
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
            
    