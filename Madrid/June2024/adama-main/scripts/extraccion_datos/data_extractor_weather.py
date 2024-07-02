"""
Autor: Alejandro Alvarez Tenedor
Fecha: 31 de mayo de 2024
Funcionalidad: Este script descarga archivos ZIP mensuales que contienen datos de densidad de tráfico desde la página web del Ayuntamiento de Madrid. 
Utiliza requests y BeautifulSoup para realizar scraping web y guardar los archivos en el directorio especificado.
"""

import requests
from bs4 import BeautifulSoup
import os
from datetime import datetime 

def download_file(url, save_path):
    with requests.get(url, stream=True) as response:
        response.raise_for_status()
        with open(save_path, "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)

def normalize_month(month):
    months_es = ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre']
    months_en = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
    if month == 'diciiembre':
        month = 'diciembre'
    return months_en[months_es.index(month.lower())]

def download_monthly_zips(base_url, save_directory):
    if not os.path.exists(save_directory):
        os.makedirs(save_directory)

    response = requests.get(base_url)
    soup = BeautifulSoup(response.text, "html.parser")

    yearly_containers = soup.find_all("li", class_="asociada-item")
    for year_container in yearly_containers:
        year_element = year_container.find("p", class_="info-title")
        if not year_element:
            continue
        year = year_element.text.strip()
        month_containers = year_container.find_all("li", class_="asociada-item")
        for month_container in month_containers:
            month_element = month_container.find("p", class_="info-title")
            if not month_element:
                continue
            month = month_element.text.strip()
            normalized_month = normalize_month(month.lower())  # Normalize the month name
            csv_link = month_container.find("a", class_="asociada-link ico-csv")
            if csv_link:
                csv_url = f"https://datos.madrid.es{csv_link['href']}"
                file_name = f"{normalized_month}-{year}.csv"
                save_path = os.path.join(save_directory, file_name)
                print(f"Downloading {normalized_month}-{year}.zip...")
                download_file(csv_url, save_path)
                print(f"{normalized_month}-{year}.zip downloaded successfully!")

if __name__ == "__main__":
    base_url = "https://datos.madrid.es/sites/v/index.jsp?vgnextoid=fa8357cec5efa610VgnVCM1000001d4a900aRCRD&vgnextchannel=374512b9ace9f310VgnVCM100000171f5a0aRCRD"
    save_directory = r"C:\Users\Usuario\Desktop\Proyecto Saturdays\data\datos_meteorologicos" 

    download_monthly_zips(base_url, save_directory)
