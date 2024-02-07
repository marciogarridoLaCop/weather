import requests

def retornaDados(urljson):
    dados_json = ""
    response = requests.get(urljson)
    if response.status_code == 200:
        dados_json = response.json()
    return dados_json