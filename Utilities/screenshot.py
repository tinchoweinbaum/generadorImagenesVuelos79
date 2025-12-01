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

def sacaScreenshots(url, claseDiv):

    dirFotoPartidas = os.path.join(BASE_DIR, "..", "screenshots", "vuelosPartidas.png")

    dirFotoArribos = os.path.join(BASE_DIR, "..", "screenshots", "vuelosArribos.png")

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
        tab.screenshot(path=dirFotoPartidas, clip=clip)
        print("Screenshot guardado:", dirFotoPartidas)
        
        #Hace lo mismo pero con el iframe de llegadas ahora
        iframe_element = tab.frame_locator("iframe[src*='avionio.com'][src*='arrivals']")

        tabla = iframe_element.locator("tbody")

        primer_tr = tabla.locator("tr").first

        if(primer_tr.count() == 1):
            print("hola")

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
        tab.screenshot(path=dirFotoArribos, clip=clip)
        print("Screenshot guardado:", dirFotoArribos)

        navegador.close()

if __name__ == "__main__":
    
    claseHtml = "html" #Clase del cuadro en bahiablanca


    if len(sys.argv) < 2:
        print("Uso: python Utilities/screenshot.py *url*")
        sys.exit(1)

    url = sys.argv[1]

    sacaScreenshots(url,claseHtml) #Genera los screenshots
    #cropScreenshotTop(r"d:\repos\generadorImagenesVuelos79\Utilities\..\screenshots\vuelosPartidas.png")
    #cropScreenshotTop(r"d:\repos\generadorImagenesVuelos79\Utilities\..\screenshots\vuelosArribos.png",0.4)