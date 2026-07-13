import os
import time
import requests
import sys
from playwright.sync_api import sync_playwright
from PIL import Image

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def getPath(ruta_relativa):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, ruta_relativa)
    
    # Busca la carpeta padre de "src"
    base = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
    # abspath resuelve el ".." y te devuelve una ruta limpia (ej: C:\...\placas\imagen.png)
    return os.path.abspath(os.path.join(base, ruta_relativa))

def paginaActiva(url,timeout = 15):
    try:
        resp = requests.get(url,timeout = timeout)
        return resp.status_code == 200
    except requests.RequestException:
        return False

def sacaScreenshots(url):

    dirScreenArribos = getPath("screenshots/vuelosArribos.png")
    dirScreenPartidas = getPath("screenshots/vuelosPartidas.png")


    if not paginaActiva(url):
        print("La pagina no se encuentra activa.")
        sys.exit(1)

    with sync_playwright() as p:
        navegador = p.chromium.launch(headless=True)
        tab = navegador.new_page()

        tab.goto(url, wait_until="load")
        tab.wait_for_load_state("networkidle")

        #Entro al iframe
        iframe_element = tab.frame_locator("iframe[src*='avionio.com'][src*='departures']")
        #Entro a la tabla dentro del iframe
        tabla = iframe_element.locator("tbody")

        primer_tr = tabla.locator("tr").first

        tbody_box = tabla.bounding_box()
        tr_box = primer_tr.bounding_box()

            # defino la región recortada: debajo del primer <tr>
        clip = {
            "x": tbody_box["x"],
            "y": tr_box["y"] + tr_box["height"],   # empieza después del primer tr
            "width": tbody_box["width"],
            "height": (tbody_box["y"] + tbody_box["height"]) - (tr_box["y"] + tr_box["height"])
        }

        # Screenshot de SOLO esa región exacta del iframe
        tab.screenshot(path=dirScreenPartidas, clip=clip)
        #print("Screenshot guardado:", dirFotoPartidas)
        
        #Hace lo mismo pero con el iframe de llegadas ahora
        iframe_element = tab.frame_locator("iframe[src*='avionio.com'][src*='arrivals']")

        tabla = iframe_element.locator("tbody")

        primer_tr = tabla.locator("tr").first #Toma el primer tr (boton de vuelos anteriores)

        tbody_box = tabla.bounding_box() #Se queda con las coordenadas en la pagina de la tabla y el primer tr
        tr_box = primer_tr.bounding_box()

        # defino la región recortada: debajo del primer <tr>
        clip = {
            "x": tbody_box["x"],
            "y": tr_box["y"] + tr_box["height"],   #toma la parte de la tabla que va despues del primer tr
            "width": tbody_box["width"],
            "height": (tbody_box["y"] + tbody_box["height"]) - (tr_box["y"] + tr_box["height"]) #Cropea la parte que no necesita
        }

        # Screenshot de SOLO esa región exacta del iframe
        tab.screenshot(path=dirScreenArribos, clip=clip)
        #print("Screenshot guardado:", dirFotoArribos)

        navegador.close()

        return dirScreenArribos, dirScreenPartidas # Devuelvo el Path de los dos screenshots para vuelos_main.py

if __name__ == "__main__":
    pass