import os
import time
import requests
import sys
from playwright.sync_api import sync_playwright
from PIL import Image

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def paginaActiva(url,timeout = 15):
    try:
        resp = requests.get(url,timeout = timeout)
        return resp.status_code == 200
    except requests.RequestException:
        return False


def sacaScreenPartidas(url, claseDiv):

    dirFoto = os.path.join(BASE_DIR, "..", "screenshots", "vuelosPartidas.png")

    if(not paginaActiva(url)):
       print("La pagina no se encuentra activa, no existe, o tardo demasiado en responder.")
       exit()

    with sync_playwright() as p:
        navegador = p.chromium.launch(headless=True) #Abre una instancia de chromium en headless y abre una página en este navegador
        tab = navegador.new_page()

        tab.goto(url, wait_until="load") #Va a la url y espera a que cargue
        tab.wait_for_load_state("networkidle")

        claseCerrar = ".fill-none.stroke-white"
       
        elemCerrar = tab.query_selector(f"{claseCerrar}")
        if claseCerrar:
            elemCerrar.click()

        elemento = tab.query_selector(claseDiv) #Selecciona el elemento

        if elemento: 
            elemento.screenshot(path = dirFoto) #Si existe le saca screenshot, si no, tira error.
            screenshot = Image.open(dirFoto)
            screenshot = screenshot.resize((int(screenshot.width * 1.5),int(screenshot.height*1.5)), Image.LANCZOS) #Lo agranda 150% para que quede mejor en la placa
            screenshot.save(dirFoto)
            #print(f"Se guardo el screenshot de partidas de aeropuertosargentina.com en: {dirFoto}")
        else:
            print(f"No se encontro la clase {claseDiv} dentro de la URL especificada. Probablemente hubo cambios la pagina de aeropuertosargentina.com")

        navegador.close()

def sacaScreenArribos(url, claseDiv):

    dirFoto = os.path.join(BASE_DIR, "..", "screenshots", "vuelosArribos.png")

    if(not paginaActiva(url)):
       print("La pagina no se encuentra activa, no existe, o tardo demasiado en responder.")
       sys.exit(1)

    with sync_playwright() as p:

        navegador = p.chromium.launch(headless=True) #Abre una instancia de chromium en headless y abre una página en este navegador
        tab = navegador.new_page()

        tab.goto(url, wait_until="load") #Va a la url y espera a que cargue
        tab.wait_for_load_state("networkidle")

        claseCerrar = ".fill-none.stroke-white"
       
        elemCerrar = tab.query_selector(f"{claseCerrar}")
        if claseCerrar:
            elemCerrar.click()


        claseBoton = ".group.inline-flex.items-center.border-b-2.py-2.xl\\:py-2.px-3.lg\\:px-4.font-open.text-sm.font-semibold.leading-4.space-3.cursor-pointer.border-transparent.text-gray-500"

        elemArribos = tab.query_selector(f"{claseBoton}") #Hace click en arribos

        if elemArribos:
            elemArribos.click()
                
        tab.wait_for_load_state("networkidle")
        time.sleep(1)

        elemento = tab.query_selector(claseDiv) #Selecciona el elemento

        time.sleep(1)

        if elemento: 
            elemento.screenshot(path = dirFoto) #Si existe le saca screenshot, si no, tira error.
            screenshot = Image.open(dirFoto)
            screenshot = screenshot.resize((int(screenshot.width * 1.5),int(screenshot.height*1.5)), Image.LANCZOS) #Lo agranda 150% para que quede mejor en la placa
            screenshot.save(dirFoto)
            #print(f"Se guardo el screenshot de arribos de aeropuertosargentina.com en: {dirFoto}")
        else:
            print(f"No se encontro la clase {claseDiv} dentro de la URL especificada. Probablemente hubo cambios la pagina de aeropuertosargentina.com")

        navegador.close()

def cropScreenshotRight(pathFoto,porcentaje = 0.137): #Cropea la foto desde la derecha, si no especifica cuanto, se corta el 14%
    screenshot = Image.open(pathFoto)

    width, height= screenshot.size
    widthCrop = int(width*(1 - porcentaje)) #Se calcula el nuevo ancho de la imagen
    tuplaSize = (0,0,widthCrop,height)

    screenshot = screenshot.crop(tuplaSize)
    screenshot.save(pathFoto)

def sacaScreenshots(dirScreenshots, url, claseHtml):
    """
    Recibe la url de aa2000, junto con la carpeta de salida y la clase html del cuadro para generar los 2 screenshots, devuelve la dirección en la que guardó los screenshots.
    """
    dirScreenArribos = os.path.join(dirScreenshots, "vuelosArribos.png")
    dirScreenPartidas = os.path.join(dirScreenshots, "vuelosPartidas.png")

    sacaScreenArribos(url, claseHtml)
    # print(f"Screenshot guardado en {dirScreenArribos}")

    sacaScreenPartidas(url, claseHtml)
    # print(f"Screenshot guardado en {dirScreenPartidas}")

    try:
        cropScreenshotRight(dirScreenPartidas)
    except FileNotFoundError:
        print("No se pudo recortar la imagen de las partidas")
        return
    
    try:
        cropScreenshotRight(dirScreenArribos)
    except FileNotFoundError:
        print("No se pudo recortar la imagen de los arribos")
        return

    return dirScreenArribos, dirScreenPartidas

if __name__ == "__main__":
    pass