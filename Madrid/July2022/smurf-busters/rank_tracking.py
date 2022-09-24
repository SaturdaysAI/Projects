from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import pandas as pd
from selenium.webdriver import ActionChains
import time
from config import NUMBER_OF_GAMES
from selenium.webdriver.support.ui import Select


def get_info_from_match(summoner_name):
    # Crear una sesión de Firefox
    driver = webdriver.Chrome(r'C:\Program Files (x86)\Google\Chrome\chromedriver.exe')
    driver.implicitly_wait(10)
    driver.maximize_window()

    summoner_name_search = summoner_name.replace(' ', '+')

    driver.get(f"https://www.leagueofgraphs.com/es/summoner/euw/{summoner_name_search}")

    filter = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CLASS_NAME, "recentGamesFilterExpander")))
    ActionChains(driver).click(filter).perform()

    element = driver.find_elements(By.CLASS_NAME, 'recentGamesFilter')
    ActionChains(driver).click(element[1]).perform()

    select = driver.find_elements(By.XPATH, '//*[@id="drop-queueTypes-recentgames"]/ul/li[4]/a')
    ActionChains(driver).click(select[0]).perform()
    flag_ver_mas = 10
    while flag_ver_mas < NUMBER_OF_GAMES:
        try:

            search_field = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CLASS_NAME, "see_more_ajax_button")))
            ActionChains(driver).click(search_field).perform()
            flag_ver_mas += 10
        except:
            flag_ver_mas = 0
    time.sleep(2)
    tabla_partidas = driver.find_element(By.CLASS_NAME, value="data_table.relative.recentGamesTable.inverted_rows_color")
    elems = tabla_partidas.find_elements(By.XPATH, value='//a[contains(@href,"/es/match/euw")]')
    list_href_partidas = []
    for elem in elems:
        list_href_partidas.append(elem.get_attribute("href"))
    list_href_partidas = set(list_href_partidas)
    list_href_partidas = list(list_href_partidas)[:NUMBER_OF_GAMES]
    partidas_jugadores_rango = {'pk_partida': [], 'jugador': [], 'rango': [], 'lps': []}
    for url in list_href_partidas:
        driver.get(url)
        lps = driver.find_elements(By.CLASS_NAME, 'number.solo-number')
        lp_result = ''
        for lp in lps:
            if lp.text:
                lp_result = lp.text
        box = driver.find_element(By.CLASS_NAME, 'data_table.matchTable')
        jugadores = box.find_elements(By.XPATH, '//a[contains(@href,"/es/summoner/euw")]')
        jugadores_rango = {}
        for i in range(1,20,2):
            jugador = jugadores[i]
            nombre = jugador.find_element(By.CLASS_NAME, 'name').text
            clasi = jugador.find_element(By.CLASS_NAME, 'subname').text
            jugadores_rango[nombre] = clasi
        partida_pk = list(jugadores_rango.keys())
        partida_pk.sort()
        partida_pk = '_'.join(partida_pk)
        for jugador, rango in jugadores_rango.items():
            if jugador.lower() != summoner_name.lower():
                continue
            partidas_jugadores_rango['pk_partida'].append(partida_pk)
            partidas_jugadores_rango['jugador'].append(jugador)
            partidas_jugadores_rango['rango'].append(rango)
            partidas_jugadores_rango['lps'].append(lp_result)
    driver.close()
    return pd.DataFrame().from_dict(partidas_jugadores_rango)



