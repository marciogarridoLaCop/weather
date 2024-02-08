#PGEB - PROGRAMA DE PÓS GRADUAÇÃO EM ENGENHARIA DE BIOSSISTEMAS UFF
import requests
import base64
from rest_framework.response import Response
from rest_framework.decorators import api_view
import math
from urllib.parse import urlencode

from datetime import datetime


@api_view(['GET'])
def getEvapotranspiracaoService(request):
    #http://127.0.0.1:8000/evapotranspiracaoservice
    query = request.GET.get('query')
    inicio = request.GET.get('inicio')
    fim = request.GET.get('fim')
    estacao = request.GET.get('estacao')
    pagina = request.GET.get('pagina')

    endpoint_url = "http://django-env-api.eba-xwzidp6r.us-east-1.elasticbeanstalk.com/sensorespecifico/1/"

    if estacao == None:
        estacao = "1"

    params = {'estacao': estacao}

    if inicio != None:
        params['inicio'] = inicio
        if fim != None:
            params['fim'] = fim

    if pagina != None:
        params['page'] = pagina

    endpoint_url = endpoint_url + "?" + urlencode(params)
    usuario = "ovo-esp-user"
    senha = "M@ster10"
    dados = retornadadosservico(endpoint_url, usuario, senha)
    pagina = ""
    if dados:
        dadosarray = filtraJson(dados)
        pagina = dadosarray[0][10]
        lista_objetos = []
        for dado in dadosarray:
            if query == 'evapo':  #http://127.0.0.1:8000/evapotranspiracaoservice?query=evapo&estacao=
                termoJson = retornaJson('termodinamica', dado, None, None)
                termoJson["id"] = dado[9]
                radiacaoJson = retornaJson('saldoradiacao', dado, termoJson,
                                           None)
                radiacaoJson["id"] = dado[9]
                evapoJson = retornaJson('evapo', dado, termoJson, radiacaoJson)
                evapoJson["id"] = dado[9]
                evapoJson["PCP"] = dado[8]
                evapoJson["next"] = dado[10]
                evapoJson["dia-mes"] = dado[11]
                converter_para_string(evapoJson)
                lista_objetos.append(evapoJson)
            elif query == 'saldoradiacao':  #http://127.0.0.1:8000/evapotranspiracaoservice?query=radiacao&estacao=1
                termoJson = retornaJson('termodinamica', dado, None, None)
                termoJson["id"] = dado[9]
                termoJson["tx"] = dado[2]
                termoJson["tn"] = dado[3]
                radiacaoJson = retornaJson('saldoradiacao', dado, termoJson,
                                           None)
                radiacaoJson["id"] = dado[9]
                radiacaoJson["Rs"] = dado[4]
                radiacaoJson["next"] = dado[10]
                converter_para_string(radiacaoJson)
                lista_objetos.append(radiacaoJson)
            elif query == 'termodinamica':  #http://127.0.0.1:8000/evapotranspiracaoservice?query=termodinamica&estacao=1
                termoJson = retornaJson('termodinamica', dado, None, None)
                termoJson["id"] = dado[9]
                termoJson["Tx"] = dado[2]
                termoJson["Tn"] = dado[3]
                termoJson["URx"] = dado[6]
                termoJson["URn"] = dado[7]
                termoJson["next"] = dado[10]
                termoJson["dia-mes"] = dado[11]
                converter_para_string(termoJson)
                lista_objetos.append(termoJson)
            elif query == 'evapotransp':  #http://127.0.0.1:8000/evapotranspiracaoservice?query=todos&estacao=1
                termoJson = retornaJson('termodinamica', dado, None, None)
                termoJson["id"] = dado[9]
                termoJson["Tx"] = dado[2]
                termoJson["Tn"] = dado[3]
                termoJson["URx"] = dado[6]
                termoJson["URn"] = dado[7]
                radiacaoJson = retornaJson('saldoradiacao', dado, termoJson,
                                           None)
                radiacaoJson["id"] = dado[9]
                radiacaoJson["Rs"] = dado[4]
                evapoJson = retornaJson('evapo', dado, termoJson, radiacaoJson)
                evapoJson["id"] = dado[9]
                evapoJson["PCP"] = dado[8]
                converter_para_string(termoJson)
                converter_para_string(radiacaoJson)
                converter_para_string(evapoJson)
                dadosjson = {}
                dadosjson["termodinamica"] = termoJson
                dadosjson["saldoradiacao"] = radiacaoJson
                dadosjson["evapo"] = evapoJson
                dadosjson["next"] = dado[10]
                dadosjson["dia-mes"] = dado[11]
                dadosjson["data"] = dado[0]
                dadosjson["URx"] = dado[6]
                dadosjson["URn"] = dado[7]
                dadosjson["Tx"] = dado[2]
                dadosjson["Tn"] = dado[3]
                dadosjson["Rs"] = dado[4]
                dadosjson["PCP"] = dado[8]
                lista_objetos.append(dadosjson)
        respostajson = {}
        respostajson["results"] = lista_objetos
        respostajson["next"] = pagina
        return (Response(respostajson))
    else:
        return (Response("Não foi possível obter os dados."))


def filtraJson(dados):
    dadosCSVCol = []
    proximapagina = ""

    if dados["next"] != None:
        proximapagina = dados["next"]

    for resultado in dados['results']:
        dado = []
        dado.append(resultado["data_registro"])
        dado.append(dia_do_ano(resultado["data_registro"]))
        dado.append(
            float(resultado["temp_max"]
                  if resultado["temp_max"] != "nan" else "0.00"))
        dado.append(
            float(resultado["temp_min"]
                  if resultado["temp_min"] != "nan" else "0.00"))
        if "rs" in resultado:
            dado.append(float(resultado["rs"])
                        )  #ALTERAR QUANDO EXISTIR ATRIBUTO NO JSON DO REQUEST
        else:
            dado.append(float(
                17.5))  #ALTERAR QUANDO EXISTIR ATRIBUTO NO JSON DO REQUEST

        dado.append(
            float(10.86))  #ALTERAR QUANDO EXISTIR ATRIBUTO NO JSON DO REQUEST
        dado.append(
            float(resultado["umidade_max"]
                  if resultado["umidade_max"] != "nan" else "0.00"))
        dado.append(
            float(resultado["umidade_min"]
                  if resultado["umidade_min"] != "nan" else "0.00"))
        dado.append(float(resultado["mm_ciclo"]))
        dado.append(resultado["id"])
        dado.append(proximapagina)
        dado.append(dia_mes(resultado["data_registro"]))

        dadosCSVCol.append(dado)
    return dadosCSVCol


def filtraJsonOLDOLD(dados):
    dadosCSVCol = []
    for i in range(len(dados)):
        dado = []
        dado.append(dados[i]["data"])
        dado.append(dia_do_ano(dados[i]["data"]))
        dado.append(
            float(
                dados[i]["temp_max"] if dados[i]["temp_max"] != "nan" else 0))
        dado.append(
            float(
                dados[i]["temp_min"] if dados[i]["temp_min"] != "nan" else 0))
        dado.append(
            float(17.5))  #ALTERAR QUANDO EXISTIR ATRIBUTO NO JSON DO REQUEST
        dado.append(
            float(10.86))  #ALTERAR QUANDO EXISTIR ATRIBUTO NO JSON DO REQUEST
        dado.append(
            float(dados[i]["umidade_max"]
                  if dados[i]["umidade_max"] != "nan" else 0))
        dado.append(
            float(dados[i]["umidade_min"]
                  if dados[i]["umidade_min"] != "nan" else 0))
        dado.append(float(dados[i]["mm_ciclo"]))
        dado.append(dados[i]["id"])
        dadosCSVCol.append(dado)
    return dadosCSVCol


def convertojson(object, data):
    objecttojson = {}
    if object == 'evapo':
        objecttojson['ETo_HS'] = data[0]
        objecttojson['ETo_PM'] = data[1]
        objecttojson['data'] = data[2]
    elif object == 'saldoradiacao':
        objecttojson['Rn'] = data[0]
        objecttojson['Rns'] = data[1]
        objecttojson['Rnl'] = data[2]
        objecttojson['Ra'] = data[3]
        objecttojson['data'] = data[4]
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
        objecttojson['data'] = data[15]

    return objecttojson


def retornaJson(object, dados, termo, rad):
    json_object = {}
    if object == 'termodinamica':
        retorno = Termodinamica(dados[2], dados[3], dados[6], dados[7], 54)
        retorno.append(dados[0])
    elif object == 'saldoradiacao':
        retorno = SaldoRadiacao(dados[1], -22.45, 54, dados[4], dados[2],
                                dados[3], termo["ea"])
        retorno.append(dados[0])
    elif object == 'evapo':
        retorno = Evapo(rad['Ra'], rad['Rn'], termo['Tm'], dados[2], dados[3],
                        termo['es'], termo['ea'], termo['Lamb'], termo['Gama'],
                        termo['Ses'], dados[5])
        retorno.append(dados[0])

    json_object = convertojson(object, retorno)
    return json_object


def Evapo(Ra, Rn, Tm, Tx, Tn, es, ea, Lamb, Gama, Ses, U2):

    #Método de Hargreaves-Samani
    #ETo_HS = float(str(0.0023*(1/Lamb)*Ra*(Tm+17.8)*(Tx - Tn)**0.5)[1:-1])
    #ETo_HS = float(0.0023*(1/Lamb)*Ra*(Tm+17.8)*(Tx - Tn)**0.5)[1:-1]
    ETo_HS = 0.0023 * (1 / Lamb) * Ra * (Tm + 17.8) * (Tx - Tn)**0.5

    # Método de Penman-Monteith
    G = 0
    ETo_PM = float(((1 / Lamb) * Ses * (Rn - G) + (Gama * 900 * U2 *
                                                   (es - ea) / (Tm + 273))) /
                   (Ses + Gama * (1 + 0.34 * U2)))

    return [ETo_HS, ETo_PM]


def SaldoRadiacao(Doy, fi, Z, Rs, Tx, Tn, ea):

    # Correção distância relativa Terra-Sol
    dr = 1 + 0.033 * math.cos(2 * math.pi * Doy / 365)

    # Declinação solar

    decl = 0.409 * math.sin((2 * math.pi * Doy / 365) - 1.39)

    # Ângulo horário entre o nasceer-pôr do Sol

    ws = math.acos(-math.tan(fi * math.pi / 180) *
                   math.tan(decl))  # Ângulo horário entre o nasceer-pôr do Sol

    Ra = 37.568 * dr * (
        (ws * math.sin(fi * math.pi / 180) * math.sin(decl)) +
        (math.cos(fi * math.pi / 180) * math.cos(decl) * math.sin(ws)))
    # Balanço de radiação

    Rso = (0.75 + 2E-5 * Z) * Ra

    Rns = float(str(0.77 * Rs)[1:-1])

    # Ondas longas
    Rnl = float(4.903E-9 * ((((Tx + 273.16)**4) + ((Tn + 273.16)**4)) / 2) *
                (0.34 - 0.14 * ea**0.5) * (1.35 * (Rs / Rso) - 0.35))

    Rn = Rns - Rnl

    return [Rn, Rns, Rnl, Ra]


def Termodinamica(Tx, Tn, URx, URn, Z):  # Temperatura
    Patm = 101.3 * (
        (293 - 0.0065 * Z) / 293)**5.26  # Pressão atmosférica [kPa]

    Tm = float((float(Tx) + float(Tn)) / 2)  # Temperatura do ar média [oC]

    URm = float((float(URx) + float(URn)) / 2)  # Umidade do ar média [%]

    es = float(((0.6108 * math.exp(17.27 * Tn / (237.3 + Tn))) +
                (0.6108 * math.exp(17.27 * Tx / (237.3 + Tx)))) /
               2)  # Pressão de saturação do vapor d'água do ar [kPa]

    ea = float((0.6108 * math.exp(17.27 * Tn / (237.3 + Tn)) * URx +
                0.6108 * math.exp(17.27 * Tx / (237.3 + Tx)) * URn) /
               200)  # Pressão de real do vapor d'água do ar [kPa]

    DPV = (es - ea)  # Déficit de pressão de saturação [kPa]

    Ses = 4098 * (0.6108 * math.exp(17.27 * Tm / (Tm + 237.3))) / (
        Tm + 237.3)**2  # Derivada da curvas de pressão de saturação [kPa]

    UA = 2168 * (ea / (Tm + 273.15))  # Umidade absoluta [g/m³]

    US = 2168 * (es / (Tm + 273.15))  # Umidade Absoluta de saturação [g/m³]

    Qesp = 0.622 * ea / (Patm - 0.378 * ea)  # Umidade específica [g/g]

    Rmix = 0.622 * ea / (Patm - ea)  # Razão de mistura [g/g]

    if ea != 0:
        Tpo = (237.3 * math.log10(ea / 0.6108)) / (7.5 - math.log10(
            ea / 0.6108))  # Temperatura do ponto de orvalho [oC]
    else:
        Tpo = 0

    Lamb = 2.501 - (0.002361) * Tm  # Calor latente de evaporação [MJ/kg]

    Gama = (1.013E-3 * Patm) / (0.622 * Lamb
                                )  # Coeficiente pscrométrico [oC/MJ]
    if Tm != 0:
        Dens = 3.484 * (Patm / Tm)  # Densidade do ar [g/m³]
    else:
        Dens = 0

    return [
        Patm, Tm, URm, es, ea, DPV, UA, US, Qesp, Rmix, Tpo, Dens, Lamb, Gama,
        Ses
    ]


def retornaDados(urljson):
    dados_json = ""
    response = requests.get(urljson)
    if response.status_code == 200:
        dados_json = response.json()
    return dados_json


def retornadadosservico(url, usuario, senha):
    try:
        # Codifica as credenciais em base64
        credenciais = f"{usuario}:{senha}"
        credenciais_base64 = base64.b64encode(credenciais.encode()).decode()

        # Define o cabeçalho de autorização
        headers = {"Authorization": f"Basic {credenciais_base64}"}

        # Faz a solicitação GET com a autenticação básica
        response = requests.get(url, headers=headers)

        # Verifica se a solicitação foi bem-sucedida (código de status 200)
        if response.status_code == 200:
            dados = response.json()
            return dados
        else:
            print(f"Erro: {response.status_code} - {response.text}")
            return None
    except requests.RequestException as req_exc:
        # Captura exceções relacionadas a solicitações HTTP
        print("Erro na solicitação HTTP:")
        print(str(req_exc))
        return None
    except Exception as e:
        # Capture exceções e imprima detalhes do erro
        print(f"Ocorreu um erro: {str(e)}")
        return None


def dia_do_ano(data):
    dia = int(data[8:10])
    mes = int(data[5:7])
    ano = int(data[:4])

    data_objeto = datetime(ano, mes, dia)
    dia_ano = data_objeto.timetuple().tm_yday
    return dia_ano


def dia_mes(data):
    dia = data[8:10]
    mes = data[5:7]
    hora = data[11:13]
    minuto = data[14:16]
    segundo = data[17:19]
    diames = dia + "/" + mes + " " + hora + ":" + minuto + ":" + segundo
    return diames


def converter_para_string(dicionario):
    for chave, valor in dicionario.items():
        dicionario[chave] = str(valor)
