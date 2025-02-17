# importando bibliotecas
from csv import DictWriter
from dataclasses import field
from http.client import responses
from os import write

# REQUEST para fazer requisições HTTP à API
import requests
import csv
import time

from pandas.io.common import file_exists
from pandas.io.formats.format import save_to_buffer


# FUNÇÂO para realizar a requisição dos dados do clima
def dados_clima(city:str, api_key: str):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()

    else:
        print(f"Erro ao obter dados:{response.status_code}")
        return None

# FUNÇÂO para salvar os dados em CSV
def salvar_csv(data, filename='Dados_clima.csv'):
    fieldnames = ["Cidade", "Temperatura", "Umidade", "Clima"]
    file_exists = False

    try:
        with open(filename, "r") as f:
            file_exists = True
    except FileNotFoundError:
            file_exists = False

    with open(filename, mode="a", newline="") as file:
        writer = DictWriter(file, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        writer.writerow(data)

# FUNCÃO para coletar os dados
def coletar_clima(city: str, api_key: str, interval=60):
    while True:
        weater_data = dados_clima(city, api_key)
        if weater_data:
            formatted_data = {
                "Cidade": city,
                "Temperatura": weater_data["main"]["temp"],
                "Umidade": weater_data["main"]["humidity"],
                "Clima": weater_data["weather"][0]["description"],
            }
            salvar_csv(formatted_data)
            print(f"dados salvos para {city}:{formatted_data}")
        time.sleep(interval)

# EXECUÇÃO da automação
if __name__ == "__main__":
    CITY = "São Paulo"
    API_KEY = "24d6fa510a2296ee07c022e2c52b257a"
    coletar_clima(CITY, API_KEY, interval=3600)
