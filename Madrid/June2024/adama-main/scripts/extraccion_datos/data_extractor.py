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

def download_monthly_zips(base_url, save_directory, start_year, start_month, end_year):
    if not os.path.exists(save_directory):
        os.makedirs(save_directory)

    response = requests.get(base_url)
    soup = BeautifulSoup(response.text, "html.parser")

    yearly_containers = soup.find_all("li", class_="asociada-item")
    for year_container in yearly_containers:
        year_element = year_container.find("p", class_="info-title")
        if not year_element:
            continue
        
        # Ensure the year element contains a valid year
        year_text = year_element.text.strip()
        if not year_text.isdigit():
            continue
        
        year = int(year_text)
        if year < end_year or year > start_year:
            continue

        month_containers = year_container.find_all("li", class_="asociada-item")
        for month_container in month_containers:
            month_element = month_container.find("p", class_="info-title")
            if not month_element:
                continue
            
            month = month_element.text.strip()
            normalized_month = int(normalize_month(month.lower()))  # Normalize the month name

            if year == start_year and normalized_month > start_month:
                continue

            zip_link = month_container.find("a", class_="asociada-link ico-zip")
            if zip_link:
                zip_url = f"https://datos.madrid.es{zip_link['href']}"
                file_name = f"{normalized_month:02d}-{year}.zip"
                save_path = os.path.join(save_directory, file_name)
                print(f"Downloading {normalized_month:02d}-{year}.zip...")
                download_file(zip_url, save_path)
                print(f"{normalized_month:02d}-{year}.zip downloaded successfully!")

if __name__ == "__main__":
    base_url = "https://datos.madrid.es/portal/site/egob/menuitem.c05c1f754a33a9fbe4b2e4b284f1a5a0/?vgnextoid=33cb30c367e78410VgnVCM1000000b205a0aRCRD&vgnextchannel=374512b9ace9f310VgnVCM100000171f5a0aRCRD&vgnextfmt=default"
    save_directory = r"C:\Users\ezxt99454\Desktop\crisa\Personal\SaturdaysAI\clases\proyecto_final\data\densidad_trafico"
    
    start_year = 2024  # Año de inicio
    start_month = 2   # Mes de inicio (noviembre)
    end_year = 2019    # Año de fin

    download_monthly_zips(base_url, save_directory, start_year, start_month, end_year)