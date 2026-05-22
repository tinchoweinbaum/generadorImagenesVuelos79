import os
import time
import requests
import sys
from playwright.sync_api import sync_playwright
from PIL import Image

# Importamos getPath desde tu archivo principal
def getPath(ruta_relativa):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, ruta_relativa)
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ruta_relativa)

def paginaActiva(url, timeout=15):
    try:
        resp = requests.get(url, timeout=timeout)
        return resp.status_code == 200
    except requests.RequestException:
        return False

def sacaScreenPartidas(url, claseDiv):
    # RUTA CORREGIDA: Usamos getPath
    dirFoto = getPath("screenshots/vuelosPartidas.png")

    if(not paginaActiva(url)):
       print("La pagina no se encuentra activa, no existe, o tardo demasiado en responder.")
       exit()

    with sync_playwright() as p:
        navegador = p.chromium.launch(headless=True)
        tab = navegador.new_page()

        tab.goto(url, wait_until="load")
        tab.wait_for_load_state("networkidle")

        claseCerrar = ".fill-none.stroke-white"
        elemCerrar = tab.query_selector(f"{claseCerrar}")
        if claseCerrar:
            # Añadido chequeo de existencia antes de hacer click
            if elemCerrar: elemCerrar.click()

        elemento = tab.query_selector(claseDiv)

        if elemento: 
            elemento.screenshot(path=dirFoto)
            screenshot = Image.open(dirFoto)
            screenshot = screenshot.resize((int(screenshot.width * 1.5), int(screenshot.height * 1.5)), Image.LANCZOS)
            screenshot.save(dirFoto)
        else:
            print(f"No se encontro la clase {claseDiv}")

        navegador.close()

def sacaScreenArribos(url, claseDiv):
    # RUTA CORREGIDA: Usamos getPath
    dirFoto = getPath("screenshots/vuelosArribos.png")

    if(not paginaActiva(url)):
       print("La pagina no se encuentra activa, no existe, o tardo demasiado en responder.")
       sys.exit(1)

    with sync_playwright() as p:
        navegador = p.chromium.launch(headless=True)
        tab = navegador.new_page()

        tab.goto(url, wait_until="load")
        tab.wait_for_load_state("networkidle")

        claseCerrar = ".fill-none.stroke-white"
        elemCerrar = tab.query_selector(f"{claseCerrar}")
        if elemCerrar:
            elemCerrar.click()

        claseBoton = ".group.inline-flex.items-center.border-b-2.py-2.xl\\:py-2.px-3.lg\\:px-4.font-open.text-sm.font-semibold.leading-4.space-3.cursor-pointer.border-transparent.text-gray-500"
        elemArribos = tab.query_selector(f"{claseBoton}")

        if elemArribos:
            elemArribos.click()
                
        tab.wait_for_load_state("networkidle")
        time.sleep(1)

        elemento = tab.query_selector(claseDiv)
        time.sleep(1)

        if elemento: 
            elemento.screenshot(path=dirFoto)
            screenshot = Image.open(dirFoto)
            screenshot = screenshot.resize((int(screenshot.width * 1.5), int(screenshot.height * 1.5)), Image.LANCZOS)
            screenshot.save(dirFoto)
        else:
            print(f"No se encontro la clase {claseDiv}")

        navegador.close()

def cropScreenshotRight(pathFoto, porcentaje=0.137):
    screenshot = Image.open(pathFoto)
    width, height = screenshot.size
    widthCrop = int(width * (1 - porcentaje))
    tuplaSize = (0, 0, widthCrop, height)
    screenshot = screenshot.crop(tuplaSize)
    screenshot.save(pathFoto)

def sacaScreenshots(dirScreenshots, url, claseHtml):
    # RUTA CORREGIDA: Usamos getPath para los archivos dentro de la carpeta
    dirScreenArribos = getPath("screenshots/vuelosArribos.png")
    dirScreenPartidas = getPath("screenshots/vuelosPartidas.png")

    sacaScreenArribos(url, claseHtml)
    sacaScreenPartidas(url, claseHtml)

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