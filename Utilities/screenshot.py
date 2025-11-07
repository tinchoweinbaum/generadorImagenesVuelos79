import os
import requests
from playwright.sync_api import sync_playwright
from PIL import Image

#RECORTAR Y RESIZEAR CORRECTAMENTE EL SCREENSHOT, LLEVARLO A 1920x1080 Y HACER Q LAS COSAS Q SOBRAN EN EL SCREENSHOT QUEDEN AFUERA DEL MISMO


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
    #selector = rf".{claseDiv}"

    dirFoto = os.path.join(dir,"vuelosArribos.png")

    if(not paginaActiva(url)):
       print("La página no se encuentra activa, no existe, o tardó demasiado en responder.")
       exit()

    with sync_playwright() as p:
        navegador = p.chromium.launch(headless=True)#Abre una instancia de chromium en headless y abre una página en este navegador
        tab = navegador.new_page()

        tab.goto(url, wait_until="load") #Va a la url y espera a que cargue
        tab.wait_for_load_state("networkidle")

        verMas = tab.query_selector(r".flex.flex-row.items-center.justify-center.lg\:gap-2.gap-1")

        #Se clickea el botón de ver más antes de sacar la foto
        if (verMas):
            verMas.click()
            #algo x la rama del else?

        elemento = tab.query_selector(claseDiv) #Selecciona el elemento

        if elemento: 
            elemento.screenshot(path = dirFoto) #Si existe le saca screenshot, si no, tira error.
            print(f"Se guardo el screenshot de aeropuertosargentina.com en: {dirFoto}")
        else:
            print(f"No se encontro la clase {claseDiv} dentro de la URL especificada. Probablemente hubo cambios la pagina de aeropuertosargentina.com")

        navegador.close()

claseHtml = r".flex.flex-col.space-5.mb-6.xl\:mb-8.w-full" #actualmente esto se hardcodea hasta que se rompa XD

dir, url = leeTxt()

sacaScreen(url,claseHtml,dir) #Genera el screenshot de la pagina de vuelos

pathScreenshot = os.path.join(dir,"vuelosArribos.png")