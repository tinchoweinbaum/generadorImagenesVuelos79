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
        navegador = p.chromium.launch(headless=False)
        tab = navegador.new_page()

        tab.goto(url, wait_until="load")
        tab.wait_for_load_state("networkidle")

        # 1 — IFRAME como LOCATOR (NO FrameLocator)
        iframe_element = tab.frame_locator("iframe[src*='avionio.com'][src*='departures']")
        # 2 — Entrar al contenido del iframe
        tabla = iframe_element.locator(".tt")
        # 3 — Screenshot
        tabla.screenshot(path=dirFotoPartidas)

        print(f"Screenshot de partidas guardado en: {dirFotoPartidas}")
        
        iframe_element = tab.frame_locator("iframe[src*='avionio.com'][src*='arrivals']")
        # 2 — Entrar al contenido del iframe
        tabla = iframe_element.locator(".tt")
        # 3 — Screenshot
        tabla.screenshot(path=dirFotoArribos)

        navegador.close()

def cropScreenshotTop(dirFoto,porcentaje = 0.5):
    fotoOg = Image.open(dirFoto)

    width, height = fotoOg.size
    corte = int(height * porcentaje)

    # Recorta desde 'corte' hasta el final
    fotoCrop = fotoOg.crop((0, corte, width, height))

    fotoCrop.save(dirFoto)


if __name__ == "__main__":
    
    claseHtml = "html" #Clase del cuadro en bahiablanca


    if len(sys.argv) < 2:
        print("Uso: python Utilities/screenshot.py *url*")
        sys.exit(1)

    url = sys.argv[1]

    sacaScreenshots(url,claseHtml) #Genera los screenshots
    cropScreenshotTop(r"d:\repos\generadorImagenesVuelos79\Utilities\..\screenshots\vuelosPartidas.png")
    cropScreenshotTop(r"d:\repos\generadorImagenesVuelos79\Utilities\..\screenshots\vuelosArribos.png")