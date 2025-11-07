import os
import requests
import sys
from playwright.sync_api import sync_playwright
from PIL import Image

def paginaActiva(url,timeout = 15):
    try:
        resp = requests.get(url,timeout = timeout)
        return resp.status_code == 200
    except requests.RequestException:
        return False

def sacaScreen(url, claseDiv):  #La función pide 3 parámetros: url, nombre de la clase a capturar, y nombre del archivo a crear.

    dirFoto = os.path.join("screenshots","vuelosArribos.png")

    if(not paginaActiva(url)):
       print("La pagina no se encuentra activa, no existe, o tardo demasiado en responder.")
       exit()

    with sync_playwright() as p:
        navegador = p.chromium.launch(headless=True)#Abre una instancia de chromium en headless y abre una página en este navegador
        tab = navegador.new_page()

        tab.goto(url, wait_until="load") #Va a la url y espera a que cargue
        tab.wait_for_load_state("networkidle")

        #verMas = tab.query_selector(r".flex.flex-row.items-center.justify-center.lg\:gap-2.gap-1")
        #if (verMas):   #Se clickea el botón de ver más antes de sacar la foto
        #    verMas.click()

        elemento = tab.query_selector(claseDiv) #Selecciona el elemento

        if elemento: 
            elemento.screenshot(path = dirFoto) #Si existe le saca screenshot, si no, tira error.
            screenshot = Image.open(dirFoto)
            screenshot = screenshot.resize((int(screenshot.width * 1.5),int(screenshot.height*1.5)), Image.LANCZOS) #Lo agranda 150% para que quede mejor en la placa
            screenshot.save(dirFoto)
            print(f"Se guardo el screenshot de arribos de aeropuertosargentina.com en: {dirFoto}")
        else:
            print(f"No se encontro la clase {claseDiv} dentro de la URL especificada. Probablemente hubo cambios la pagina de aeropuertosargentina.com")

        navegador.close()

def cropScreenshotRight(pathFoto,porcentaje = 0.14): #Cropea la foto desde la derecha, si no especifica cuanto, se corta el 14%
    screenshot = Image.open(pathFoto)

    width, height= screenshot.size
    widthCrop = int(width*(1 - porcentaje)) #Se calcula el nuevo ancho de la imagen
    tuplaSize = (0,0,widthCrop,height)

    screenshot = screenshot.crop(tuplaSize)
    screenshot.save(pathFoto)
    print("Se recorto la imagen.")

if __name__ == "__main__":

    claseHtml = r".flex.flex-col.space-5.mb-6.xl\:mb-8.w-full" #Clase HTML del cuadro de vuelos

    if len(sys.argv) < 2:
        print("Uso: python Utilities/screenshot.py *dirFoto* *url*")
        sys.exit(1)

    url = sys.argv[1]

    sacaScreen(url,claseHtml) #Genera el screenshot de la pagina de vuelos.

    pathScreenshot = os.path.join("screenshots", "vuelosArribos.png")  # Guarda la dirección de la imagen en una variable.

    try:
        cropScreenshotRight(pathScreenshot)
    except FileNotFoundError:
        sys.exit(1)