import numpy as np

import requests
import logging
from bs4 import BeautifulSoup
import urllib

from requests.models import Response

FORMAT = '%(asctime)-15s  %(message)s'
URL = "https://www.scjn.gob.mx/igualdad-de-genero/igualdadsentencias?page=0"

logging.basicConfig(format=FORMAT)
logging.getLogger('crawler').setLevel(logging.INFO)
logger = logging.getLogger('crawler')
page = requests.get(URL)
soup = BeautifulSoup(page.content, 'html.parser')
logger.info("Status {}".format(page.status_code))
# logger.info("Content {}".format(page.content))
# logger.info("HTML Content {}".format(soup.prettify()))
sentence_table = soup.find('table')
print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
print(sentence_table)

for row in sentence_table.find_all('tr'):
    tds_sentencia = row.find_all('td')

    if len(tds_sentencia) > 0:
        link = tds_sentencia[1].find('a').get("href")
        print("Perioddo: {} Materia: {} Tema: {} \n Enlace: ".format(tds_sentencia[0].text,
                                                                     tds_sentencia[2].text,
                                                                     tds_sentencia[3].text,
                                                                     link))

logger.info("finalize")
