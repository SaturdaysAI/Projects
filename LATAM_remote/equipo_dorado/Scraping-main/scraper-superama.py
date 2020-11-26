import pandas as pd
from bs4 import BeautifulSoup, Tag
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import getpass
from datetime import date
from time import sleep

# configuración de selenium
usuario = getpass.getuser()
driver = 'C:/Users/' + usuario + '/Documents/chromedriver_win32/chromedriver.exe' # ruta donde se encuentra el webdriver
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore-ssl-errors')
browser = webdriver.Chrome(driver, chrome_options=options) # inizializando el driver Chrome
browser.maximize_window() # maximizar la ventana de Chrome

# productos a scrapear
productos = ['huevo', 'frijol', 'leche', 'tortilla', 'papel higiénico']


URL = 'https://www.superama.com.mx' # url de superama
fecha = date.today().strftime("%d-%m-%Y") # fecha de hoy
nombre_archivo = 'superama_' + fecha + '.csv' # el nombre que tendra el archivo con los datos
data_general = [] # lista donde se guardaran los datos

browser.get(URL)    # abriendo la url de superama
sleep(2) # esperando 2 segundo a que cargue la pagina

for item in productos: # para cada producto en productos

    # ingresa el nombre del producto en el buscador
    ingresar = browser.find_element_by_xpath("//*[@id='serachTextV3']") 
    ingresar.send_keys(item)
    ingresar.send_keys(Keys.ENTER)
    sleep(7) # espera 6s a que cargue a pagina
    html = browser.page_source  # extrayendo el HTML
    soup = BeautifulSoup(html, 'lxml')
    
    # elimina todas las etiquetas <b></b> del html ya que no necesito este texto
    for tag in soup.find_all('b'):
        tag.replaceWith('')
    
    # eliminar todos los <span></span> del html ya que no necesito este texto
    for tag in soup.find_all('span', class_='upcPromo rollBack'):
        tag.replaceWith('')

    # en la lista "data" se guarda cada resultado de la busqueda
    data = soup.find_all('li', class_='upcWrapper item isotope-item')
    
    # para cada resultado
    for li in data:
        text = " ".join(li.text.strip().replace('Agregar', '').split())
        # en este diccionario guardo el producto, su descripcion y precio
        producto = {'producto': item,
                    'descripcion': text[:text.find('$')],
                    'precio': float(text[text.find('$')+1:])}
        data_general.append(producto) # agrego el diccionario a la lista de productos
    
    sleep(15) # espero 15s para realizar la siguiente busqueda sino la pagina se dará cuenta que la estoy scrapeando xd

browser.close() # cierro el navegador


df = pd.DataFrame(data_general) # hago una dataframe con todos los productos
df['fecha'] = fecha # le agrego una columna de fecha con la fecha de hoy
df['ubicacion'] = "unknown"
df.to_csv(nombre_archivo) # lo exporto como csv