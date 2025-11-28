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
       sys.exit(1)

    with sync_playwright() as p:
        navegador = p.chromium.launch(headless=False) #Abre una instancia de chromium en headless y abre una página en este navegador
        tab = navegador.new_page()

        tab.goto(url, wait_until="load") #Va a la url y espera a que cargue
        tab.wait_for_load_state("networkidle")

        #verMas = tab.query_selector(r".flex.flex-row.items-center.justify-center.lg\:gap-2.gap-1")
        #if (verMas):   #Se clickea el botón de ver más antes de sacar la foto
        #    verMas.click()

        elemento = tab.locator(claseDiv) #Selecciona el elemento

        if elemento.count() > 0: 
            elemento.screenshot(path = dirFoto) #Si existe le saca screenshot, si no, tira error.
            screenshot = Image.open(dirFoto)
            screenshot = screenshot.resize((int(screenshot.width * 1.5),int(screenshot.height*1.5)), Image.LANCZOS) #Lo agranda 150% para que quede mejor en la placa
            screenshot.save(dirFoto)
            print(f"Se guardo el screenshot de partidas de aeropuertosargentina.com en: {dirFoto}")
        else:
            print("La clase es " + claseDiv)
            print(f"No hay vuelos")
            sys.exit(1)

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

        #elemArribos = tab.query_selector(f"{claseBoton}") #Hace click en arribos
        #if elemArribos:
        #    elemArribos.click()
        
        tab.wait_for_load_state("networkidle")
        time.sleep(1)

        elemento = tab.locator("tbody") #Selecciona el elemento

        
        if elemento.count() == 0:
             print(f"No hay vuelos")
             sys.exit(1)

        elemento = elemento.first #Selecciono la primera aparición del cuadro (x las dudas y x sintaxis de playwright)

        elemento.wait_for(state="visible", timeout=15000) 
        elemento.screenshot(path = dirFoto) #Si existe le saca screenshot, si no, tira error.
        screenshot = Image.open(dirFoto)
        screenshot = screenshot.resize((int(screenshot.width * 1.5),int(screenshot.height*1.5)), Image.LANCZOS) #Lo agranda 150% para que quede mejor en la placa
        screenshot.save(dirFoto)
        print(f"Se guardo el screenshot de arribos de aeropuertosargentina.com en: {dirFoto}")

        navegador.close()

if __name__ == "__main__":
    
    claseHtml = "tbody tr" #Clase del cuadro en bahiablanca


    if len(sys.argv) < 2:
        print("Uso: python Utilities/screenshot.py *url*")
        sys.exit(1)

    url = sys.argv[1]

    sacaScreenPartidas(url,claseHtml) #Genera el screenshot de las Partidas
    sacaScreenArribos(url,claseHtml) #General el screenshot de los Arribos