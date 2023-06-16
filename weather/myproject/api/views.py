import sqlite3
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
#from models import dados
#from weather.termodinamica import Termodinamica
#from radiacao import SaldoRadiacao
#from evapo import Evapo
import math
import pandas as pd
import json

from datetime import datetime

@api_view(['GET'])
def getEvapotranpiracaoDB(request):
    query = request.GET.get('query')
    dataini = request.GET.get('dtini')
    datafim = request.GET.get('dtfim')
    dadosevapotranspiracao = {}
    dadosdb = initdatabase()
    
    print(dataini)
    print(datafim)
    
    select = "SELECT * FROM DADOSEVAPO"
    
    if query == None:
        query = 'todos'
    
    if dataini != None and datafim != None: #http://127.0.0.1:8000/dadosevapotranspiracaodb?query=evapo&dtini=6/16/2018&dtfim=6/18/2018
        select = "SELECT * FROM DADOSEVAPO WHERE DATA >= '" + dataini + "' AND DATA <= '" +  datafim +"'"
        
    dadosdb.execute(select)
    
    resultados = dadosdb.fetchall()
    #Retornando os dados do CSV
    dadosCSVCol = []
    for linha in resultados:
        dados = []
        dados.append(datetime.strptime(linha[0], '%m/%d/%Y'))
        dados.append(linha[1])
        dados.append(linha[2])
        dados.append(linha[3])
        dados.append(linha[4])
        dados.append(linha[5])
        dados.append(linha[6])
        dados.append(linha[7])
        dados.append(linha[8])
        dadosCSVCol.append(dados)
    
    lista_objetos = []    
    for dado in dadosCSVCol:
        termoJson = retornaJsondb('termodinamica', dado, None, None)
        radiacaoJson = retornaJsondb('radiacao', dado, termoJson, None)
        evapoJson = retornaJsondb('evapo', dado, termoJson, radiacaoJson)
        if query == 'evapo': #http://127.0.0.1:8000/dadosevapotranspiracaodb?query=evapo
            lista_objetos.append(termoJson)
        elif query == 'radiacao': #http://127.0.0.1:8000/dadosevapotranspiracaodb?query=radiacao
            lista_objetos.append(radiacaoJson)
        elif query == 'termodinamica': #http://127.0.0.1:8000/dadosevapotranspiracaodb?query=termodinamica
            lista_objetos.append(evapoJson)
        elif query == 'todos':
            dadosjson = {}
            lista_objetos.append(termoJson)
            lista_objetos.append(radiacaoJson)
            lista_objetos.append(evapoJson)  
            dadosjson["termodinamica"] = termoJson
            dadosjson["radiacao"] = radiacaoJson
            dadosjson["evapo"] = evapoJson
            lista_objetos.append(dadosjson)
          
        
    return (Response(lista_objetos))

@api_view(['GET'])
def getEvapotranpiracao(request):
    query = request.GET.get('query')
    dadosevapotranspiracao = {}
    dadosCSVCol = []
    #Retornando os dados do CSV
    df = ler_csv() 
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
    
    dadosCSV = []
    for i in range(0, rows):
        dados = []
        dados.append(Data.iloc[i].values)
        dados.append(Doy.iloc[i].values)
        dados.append(Tx.iloc[i].values)
        dados.append(Tn.iloc[i].values)
        dados.append(Rs.iloc[i].values)
        dados.append(U2.iloc[i].values)
        dados.append(URx.iloc[i].values)
        dados.append(URn.iloc[i].values)
        dados.append(PCP.iloc[i].values)
        dadosCSVCol.append(dados)
    
    lista_objetos = []    
    for dado in dadosCSVCol:
        termoJson = retornaJson('termodinamica', dado, None, None)
        radiacaoJson = retornaJson('radiacao', dado, termoJson, None)
        evapoJson = retornaJson('evapo', dado, termoJson, radiacaoJson)
        if query == 'evapo': #http://127.0.0.1:8000/dadosevapotranspiracao?query=evapo
            lista_objetos.append(termoJson)
            print(termoJson)
        elif query == 'radiacao': #http://127.0.0.1:8000/dadosevapotranspiracao?query=radiacao
            lista_objetos.append(radiacaoJson)
            print(radiacaoJson)
        elif query == 'termodinamica': #http://127.0.0.1:8000/dadosevapotranspiracao?query=termodinamica
            lista_objetos.append(evapoJson)
            print(evapoJson)
        
    return (Response(lista_objetos))
  
@api_view(['GET'])
def getEvapotranpiracaoCSV(request): #http://127.0.0.1:8000/evapotranspiracao
    dadosevapotranspiracao = {}
    dadosCSVCol = []
    #Retornando os dados do CSV
    df = ler_csv() 
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
    
    dadosCSV = []
    for i in range(0, rows):
        dados = []
        dados.append(Data.iloc[i].values)
        dados.append(Doy.iloc[i].values)
        dados.append(Tx.iloc[i].values)
        dados.append(Tn.iloc[i].values)
        dados.append(Rs.iloc[i].values)
        dados.append(U2.iloc[i].values)
        dados.append(URx.iloc[i].values)
        dados.append(URn.iloc[i].values)
        dados.append(PCP.iloc[i].values)
        dadosCSVCol.append(dados)
    
    lista_objetos = []    
    for dado in dadosCSVCol:
        dadosjson = {}
        termoJson = retornaJson('termodinamica', dado, None, None)
        dadosjson["termodinamica"] = termoJson
        radiacaoJson = retornaJson('radiacao', dado, termoJson, None)
        dadosjson["radiacao"] = radiacaoJson
        evapoJson = retornaJson('evapo', dado, termoJson, radiacaoJson)
        dadosjson["evapo"] = evapoJson
        print(dadosjson)
        lista_objetos.append(dadosjson)
    
    return (Response(lista_objetos))
    
def evapostranpiracao():
    dados = {}    
              
def ler_csv():
    #Coleta de dados     
    #folder_path = 'Data/'
    folder_path = 'C:/Users/fernando.albani/Documents/Pessoal/Fernando/Mestrado Fernando/Projeto/Weather/weather/Data/'
    data = pd.read_csv(folder_path + "DadosEvapo.txt",
                 delimiter='\s+',
                 index_col=False)
    return data

def convertojsonOLD2(object, data):
    objecttojson = {}
    if object == 'evapo':
        objecttojson['ETo_HS'] = data[0]
        objecttojson['ETo_PM'] = data[1]
        objecttojson['dia-mes'] = data[2][0]
    elif object == 'radiacao':
        objecttojson['Rn'] = data[0]
        objecttojson['Rns'] = data[1]
        objecttojson['Rnl'] = data[2]
        objecttojson['Ra'] = data[3]
        objecttojson['dia-mes'] = data[4][0]
    elif object == 'termodinamica':
        objecttojson['Patm'] = data[0]
        objecttojson['Tm'] = data[1]
        objecttojson['URm'] = data[2]
        objecttojson['es'] = data[3]
        objecttojson['ea'] = data[4]
        objecttojson['DPV'] = data[5]
        objecttojson['UA'] = data[6]
        objecttojson['US'] = data[7]
        objecttojson['Qesp'] = data[8]
        objecttojson['Rmix'] = data[9]
        objecttojson['Tpo'] = data[10]
        objecttojson['Dens'] = data[11]
        objecttojson['Lamb'] = data[12]
        objecttojson['Gama'] = data[13]
        objecttojson['Ses'] = data[14]
        objecttojson['dia-mes'] = data[15][0]
        
    return objecttojson
    
def retornaJsonOLD2(object, dados, termo, rad):
    json_object = {}
    if object == 'termodinamica':
        retorno = Termodinamica(dados.Tx, dados.Tn, dados.URx, dados.URn, 54)
        retorno.append(dados.Data)
    elif object == 'radiacao':
        #termoObj = json.loads(termo)
        retorno = SaldoRadiacao(dados.Doy, -22.45, 54, dados.Rs, dados.Tx, dados.Tn, termo["ea"])
        retorno.append(dados.Data)
    elif object == 'evapo':
        #termoObj = json.loads(termo)
        #radObj = json.loads(rad)   
        retorno = Evapo(rad['Ra'], rad['Rn'], termo['Tm'], 
        dados.Tx, dados.Tn, termo['es'], termo['ea'], 
        termo['Lamb'],termo['Gama'], termo['Ses'], dados.U2)
        retorno.append(dados.Data)
   
    json_object = convertojson(object,retorno)
    return json_object

def convertojsondb(object, data):
    objecttojson = {}
    if object == 'evapo':
        objecttojson['ETo_HS'] = data[0]
        objecttojson['ETo_PM'] = data[1]
        objecttojson['dia-mes'] = str(data[2].month) + '/' + str(data[2].day) + '/' + str(data[2].year)
    elif object == 'radiacao':
        objecttojson['Rn'] = data[0]
        objecttojson['Rns'] = data[1]
        objecttojson['Rnl'] = data[2]
        objecttojson['Ra'] = data[3]
        objecttojson['dia-mes'] = str(data[4].month) + '/' + str(data[4].day) + '/' + str(data[4].year)
    elif object == 'termodinamica':
        objecttojson['Patm'] = data[0]
        objecttojson['Tm'] = data[1]
        objecttojson['URm'] = data[2]
        objecttojson['es'] = data[3]
        objecttojson['ea'] = data[4]
        objecttojson['DPV'] = data[5]
        objecttojson['UA'] = data[6]
        objecttojson['US'] = data[7]
        objecttojson['Qesp'] = data[8]
        objecttojson['Rmix'] = data[9]
        objecttojson['Tpo'] = data[10]
        objecttojson['Dens'] = data[11]
        objecttojson['Lamb'] = data[12]
        objecttojson['Gama'] = data[13]
        objecttojson['Ses'] = data[14]
        objecttojson['dia-mes'] = str(data[15].month) + '/' + str(data[15].day) + '/' + str(data[15].year)
        
    return objecttojson

def convertojson(object, data):
    objecttojson = {}
    if object == 'evapo':
        objecttojson['ETo_HS'] = data[0]
        objecttojson['ETo_PM'] = data[1]
        objecttojson['dia-mes'] = data[2][0]
    elif object == 'radiacao':
        objecttojson['Rn'] = data[0]
        objecttojson['Rns'] = data[1]
        objecttojson['Rnl'] = data[2]
        objecttojson['Ra'] = data[3]
        objecttojson['dia-mes'] = data[4][0]
    elif object == 'termodinamica':
        objecttojson['Patm'] = data[0]
        objecttojson['Tm'] = data[1]
        objecttojson['URm'] = data[2]
        objecttojson['es'] = data[3]
        objecttojson['ea'] = data[4]
        objecttojson['DPV'] = data[5]
        objecttojson['UA'] = data[6]
        objecttojson['US'] = data[7]
        objecttojson['Qesp'] = data[8]
        objecttojson['Rmix'] = data[9]
        objecttojson['Tpo'] = data[10]
        objecttojson['Dens'] = data[11]
        objecttojson['Lamb'] = data[12]
        objecttojson['Gama'] = data[13]
        objecttojson['Ses'] = data[14]
        objecttojson['dia-mes'] = str(data[15].month) + '/' + str(data[15].day) + '/' + str(data[15].year)
        
    return objecttojson

def retornaJsondb(object, dados, termo, rad):
    json_object = {}
    if object == 'termodinamica':
        retorno = Termodinamica(dados[2], dados[3], dados[6], dados[7], 54)
        retorno.append(dados[0])
    elif object == 'radiacao':
        #termoObj = json.loads(termo)
        retorno = SaldoRadiacao(dados[1], -22.45, 54, dados[4], dados[2], dados[3], termo["ea"])
        retorno.append(dados[0])
    elif object == 'evapo':
        #termoObj = json.loads(termo)
        #radObj = json.loads(rad)   
        retorno = Evapo(rad['Ra'], rad['Rn'], termo['Tm'], 
        dados[2], dados[3], termo['es'], termo['ea'], 
        termo['Lamb'],termo['Gama'], termo['Ses'], dados[5])
        retorno.append(dados[0])
   
    json_object = convertojsondb(object,retorno)
    return json_object
    
def retornaJson(object, dados, termo, rad):
    json_object = {}
    if object == 'termodinamica':
        retorno = Termodinamica(dados[2], dados[3], dados[6], dados[7], 54)
        retorno.append(dados[0])
    elif object == 'radiacao':
        #termoObj = json.loads(termo)
        retorno = SaldoRadiacao(dados[1], -22.45, 54, dados[4], dados[2], dados[3], termo["ea"])
        retorno.append(dados[0])
    elif object == 'evapo':
        #termoObj = json.loads(termo)
        #radObj = json.loads(rad)   
        retorno = Evapo(rad['Ra'], rad['Rn'], termo['Tm'], 
        dados[2], dados[3], termo['es'], termo['ea'], 
        termo['Lamb'],termo['Gama'], termo['Ses'], dados[5])
        retorno.append(dados[0])
   
    json_object = convertojson(object,retorno)
    return json_object

def Evapo(Ra,Rn,Tm,Tx,Tn,es,ea,Lamb,Gama,Ses,U2): 

    #Método de Hargreaves-Samani
    ETo_HS = float(str(0.0023*(1/Lamb)*Ra*(Tm+17.8)*(Tx - Tn)**0.5)[1:-1])      

    # Método de Penman-Monteith
    G = 0
    ETo_PM = float(str(((1/Lamb)*Ses*(Rn-G)+(Gama*900*U2*(es-ea)/(Tm + 273)))/(Ses+Gama*(1+0.34*U2)))[1:-1])      

    return [ETo_HS, ETo_PM]

def SaldoRadiacao(Doy,fi,Z,Rs,Tx,Tn,ea): 

    # Correção distância relativa Terra-Sol
    dr = 1 + 0.033 * math.cos(2*math.pi*Doy/365)         
    
    # Declinação solar
               
    decl = 0.409 * math.sin((2*math.pi*Doy/365)-1.39)

    # Ângulo horário entre o nasceer-pôr do Sol
    
    ws = math.acos(-math.tan(fi*math.pi/180)*math.tan(decl)) # Ângulo horário entre o nasceer-pôr do Sol
 
    Np = (24/math.pi)*ws
    
    Hn = 12 - Np/2     # Hora do Nascer do Sol
    Hp = 12 + Np/2     # Hora do Nascer do Pôr
    
   
    Ra = 37.568*dr*((ws*math.sin(fi*math.pi/180)*math.sin(decl))+(math.cos(fi*math.pi/180)*math.cos(decl)*math.sin(ws)))
    # Balanço de radiação
  
    Rso = (0.75 +2E-5*Z)*Ra        
   
    Rns =float(str(0.77 * Rs)[1:-1])   

    # Ondas longas
    Rnl =float(str(4.903E-9*((((Tx + 273.16)**4)+((Tn + 273.16)**4))/2)*(0.34-0.14*ea**0.5)*(1.35*(Rs/Rso)-0.35))[1:-1])   
  
    Rn = Rns - Rnl

    return [Rn,Rns,Rnl,Ra]

def Termodinamica(Tx,Tn,URx,URn,Z): # Temperatura

    Patm = 101.3*((293-0.0065*Z)/293) ** 5.26 # Pressão atmosférica [kPa]

    Tm = float(str((Tx+Tn)/2)[1:-1])                          # Temperatura do ar média [oC]

    URm = float(str((URx+URn)/2)[1:-1])                      # Umidade do ar média [%]

    es = float(str(((0.6108*math.exp(17.27*Tn/(237.3+Tn)))+(0.6108*math.exp(17.27*Tx/(237.3+Tx))))/2)[1:-1])  # Pressão de saturação do vapor d'água do ar [kPa]

    ea = float(str((0.6108*math.exp(17.27*Tn/(237.3+Tn))*URx+0.6108*math.exp(17.27*Tx/(237.3+Tx))*URn)/200)[1:-1])      # Pressão de real do vapor d'água do ar [kPa]

    DPV = (es -ea)                         # Déficit de pressão de saturação [kPa]

    Ses = 4098*(0.6108*math.exp(17.27*Tm/(Tm+237.3)))/(Tm+237.3) ** 2           # Derivada da curvas de pressão de saturação [kPa]

    UA = 2168*(ea/(Tm+273.15))             # Umidade absoluta [g/m³]

    US = 2168*(es/(Tm+273.15))             # Umidade Absoluta de saturação [g/m³]

    Qesp = 0.622*ea/(Patm-0.378*ea)        # Umidade específica [g/g]

    Rmix = 0.622*ea/(Patm-ea)              # Razão de mistura [g/g]

    Tpo = (237.3*math.log10(ea/0.6108))/(7.5-math.log10(ea/0.6108))  # Temperatura do ponto de orvalho [oC]

    Lamb = 2.501-(0.002361)*Tm                             # Calor latente de evaporação [MJ/kg]

    Gama = (1.013E-3*Patm)/(0.622*Lamb)   # Coeficiente pscrométrico [oC/MJ]

    Dens = 3.484*(Patm/Tm)                # Densidade do ar [g/m³]

    return [Patm,Tm,URm,es,ea,DPV,UA,US,Qesp,Rmix,Tpo,Dens,Lamb,Gama,Ses]

def initdatabase():
    conexao = sqlite3.connect(":memory:")
    dadosCSVCol = []
    #Retornando os dados do CSV
    df = ler_csv() 
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
    
    dadosCSV = []
    cursor = conexao.cursor()
    cursor.execute("CREATE TABLE DADOSEVAPO (data DATE, doy INTEGER, tx FLOAT, tn FLOAT, rs FLOAT, u2 FLOAT, urx FLOAT, urn FLOAT, pcp INTEGER)")
    for i in range(0, rows):
        dados = []
        #strdata = datetime.strptime(Data.iloc[i][0], '%m/%d/%Y')
        strdata = str(Data.iloc[i][0])
        
        print(strdata)
        
        #data = strdata.date()
        dados.append(strdata)
        dados.append(int(Doy.iloc[i].values))
        dados.append(float(Tx.iloc[i].values))
        dados.append(float(Tn.iloc[i].values))
        dados.append(float(Rs.iloc[i].values))
        dados.append(float(U2.iloc[i].values))
        dados.append(float(URx.iloc[i].values))
        dados.append(float(URn.iloc[i].values))
        dados.append(int(PCP.iloc[i].values))
        cursor.execute("INSERT INTO DADOSEVAPO VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", dados)
    
    return cursor