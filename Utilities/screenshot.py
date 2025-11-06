import os
import requests
from playwright.sync_api import sync_playwright



def leeTxt():

    "Esta funcion se encarga de leer el .txt y ver que parámetro fue el que se específicó."
    "si no se especifica alguno de los dos (o los 2), defaultea a lo que está escrito en el readme.txt."
    try:
        with open("datosvuelos.txt", "r", encoding="utf-8") as arch:
            lineasArch = [linea.strip() for linea in arch.readlines()]

            if len(lineasArch) == 2:
                # [0] = dir ; [1] = url
                return lineasArch[0], lineasArch[1]

            elif len(lineasArch) == 1:
                if lineasArch[0].lower() == 'h':  # ignora mayúsculas/minúsculas
                    return r"D:\Placas\MDQ", lineasArch[0]
                else:
                    return lineasArch[0], "https://www.aeropuertosargentina.com/es/vuelos?movtp=partidas&idarpt=Mar%20del%20Plata%2C%20MDQ"

            else:
                return r"D:\Placas\MDQ", "https://www.aeropuertosargentina.com/es/vuelos?movtp=partidas&idarpt=Mar%20del%20Plata%2C%20MDQ"
    except FileNotFoundError:
        print("No existe datosvuelos.txt")

    

def paginaActiva(url,timeout = 15):
    try:
        resp = requests.get(url,timeout = timeout)
        return resp.status_code == 200
    except requests.RequestException:
        return False

def sacaScreen(url, claseDiv, archivo="screenshot.png"):  #La función pide 3 parámetros: url, nombre de la clase a capturar, y nombre del archivo a crear.
    selector = rf".{claseDiv}"

    dirFoto = os.path.join(dir,"vuelosArribos.png")

    if(not paginaActiva(url)):
       print("La página no se encuentra activa, no existe, o tardó demasiado en responder.")
       exit()

    with sync_playwright() as p:
        navegador = p.chromium.launch(headless=True)#Abre una instancia de chromium en headless y abre una página en este navegador
        tab = navegador.new_page()

        tab.goto(url, wait_until="load") #Va a la url y espera a que cargue
        tab.wait_for_load_state("networkidle")

        elemento = tab.query_selector(selector) #Selecciona el elemento

        if elemento: 
            elemento.screenshot(path = dirFoto) #Si existe le saca screenshot, si no, tira error.
            print(f"Se guardó el archivo en: {dirFoto}")
        else:
            print(f"No se encontró la clase {selector} dentro de la URL especificada. Probablemente se cambio la pagina de aeropuertosargentina.com")

        navegador.close()



claseHtml = r"flex.flex-col.tablet\:w-\[41\.5rem\].tablet\:mx-auto.xl\:w-full.mt-6.xl\:mt-8" #actualmente esto se hardcodea hasta que se rompa XD

dir, url = leeTxt()

sacaScreen(url,claseHtml,dir)