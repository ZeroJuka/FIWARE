import requests
import matplotlib.pyplot as plt
from time import sleep
import json

def obter_dados_luminosidade():
    url = "http://10.5.10.34:1026/v2/entities/urn:ngsi-ld:Lamp:031/attrs/luminosity"

    payload = {}

    headers = {
      'Accept': 'application/json',
      'fiware-service': 'smart',
      'fiware-servicepath': '/'
    }

    response = requests.get(url, headers=headers, data=payload)

    if response.status_code == 200:
        data = response.json()
        luminosity_data = data.get("value")
        return luminosity_data
    else:
        print(f"Erro ao obter dados: {response.status_code}")
        return []
def obter_dados_temperatura():
    url = "http://10.5.10.34:1026/v2/entities/urn:ngsi-ld:Lamp:031/attrs/temperature"

    payload = {}
    
    headers = {
      'Accept': 'application/json',
      'fiware-service': 'smart',
      'fiware-servicepath': '/'
    }

    response = requests.get(url, headers=headers, data=payload)

    if response.status_code == 200:
        data = response.json()
        luminosity_data = data.get("value")
        return luminosity_data
    else:
        print(f"Erro ao obter dados: {response.status_code}")
        return []
def obter_dados_umidade():
    url = "http://10.5.10.34:1026/v2/entities/urn:ngsi-ld:Lamp:031/attrs/humidity"

    payload = {}
    
    headers = {
      'Accept': 'application/json',
      'fiware-service': 'smart',
      'fiware-servicepath': '/'
    }

    response = requests.get(url, headers=headers, data=payload)

    if response.status_code == 200:
        data = response.json()
        luminosity_data = data.get("value")
        return luminosity_data
    else:
        print(f"Erro ao obter dados: {response.status_code}")
        return []

def plotar_grafico(data):
    if not data:
        print("Nenhum dado disponível para plotar.")
        return

    luminosidade = [entry['attrValue'] for entry in data]
    tempos = [entry['recvTime'] for entry in data]

    plt.figure(figsize=(12, 6))
    plt.plot(tempos, luminosidade, marker='o', linestyle='-', color='r')
    plt.title('Gráfico de Luminosidade em Função do Tempo')
    plt.xlabel('Tempo')
    plt.ylabel('Luminosidade')
    plt.xticks(rotation=45)
    plt.grid(True)

    plt.tight_layout()
    plt.show()

def pisca():
    url = "http://10.5.10.34:1026/v2/entities/urn:ngsi-ld:Lamp:031/attrs"

    payload = json.dumps({
      "on": {
        "type": "command",
        "value": ""
      }
    })
    headers = {
      'Content-Type': 'application/json',
      'fiware-service': 'smart',
      'fiware-servicepath': '/'
    }

    response = requests.request("PATCH", url, headers=headers, data=payload)
    return
def desligar_luz():
    url = "http://10.5.10.34:1026/v2/entities/urn:ngsi-ld:Lamp:031/attrs"

    payload = json.dumps({
      "off": {
        "type": "command",
        "value": ""
      }
    })
    headers = {
      'Content-Type': 'application/json',
      'fiware-service': 'smart',
      'fiware-servicepath': '/'
    }

    response = requests.request("PATCH", url, headers=headers, data=payload)
    return


desligar_luz()
while True:
    luminosity_data = obter_dados_luminosidade()
    temperature_data = obter_dados_temperatura()
    humidity_data = obter_dados_umidade()

    i = 0
    if(luminosity_data < 1 or luminosity_data > 30 ):
        pisca()
    elif(humidity_data < 29 or humidity_data > 70 ):
        pisca()
    elif(temperature_data < 14 or temperature_data > 26 ):
        pisca()
    else:
        desligar_luz()

    print('luminosidade: ' + str(luminosity_data))
    print('temperatura: ' + str(temperature_data))
    print('umidade: ' + str(humidity_data))
    sleep(2)
