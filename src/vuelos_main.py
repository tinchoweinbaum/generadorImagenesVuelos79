"""
Esta es la peor mierda que programé en mi vida y la odio.
No se porque en vez de uasr módulos hice que los programas se corran entre sí. Soy literal retrasado.
"""

import subprocess
import schedule
import time
import os
import sys

from screenshot import sacaScreenshots
from imgMerger import generaPlacas_aire


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def getPath(ruta_relativa):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, ruta_relativa)
    
    # Busca la carpeta padre de "src"
    base = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
    # abspath resuelve el ".." y te devuelve una ruta limpia (ej: C:\...\placas\imagen.png)
    return os.path.abspath(os.path.join(base, ruta_relativa))

def leeTxt():
    """Abre el .txt para configurar la creación de imágenes"""

    config_path = os.path.join(os.getcwd(), "datosvuelos.txt")
    default_dir = r"C:\Placas\aire\HD"
    default_url = "https://www.aeropuertobahiablanca.com/"

    try:
        with open(config_path, "r", encoding="utf-8") as arch:
            lineas = [linea.strip() for linea in arch.readlines()]
        return (lineas[0], lineas[1]) if len(lineas) == 2 else (default_dir, default_url)
    except:
        return default_dir, default_url

def generaPlaca(dirSalida, url):
    print("")
    print("Hora actual: " + time.strftime("%H:%M:%S"))
    print("Generando placas...")
    # Rutas limpias: getPath recibe la ruta relativa, NADA de BASE_DIR ni ".."
    dirPlacaArribos = getPath(r"placas\arribosBahia.bmp")
    dirPlacaPartidas = getPath(r"placas\partidasBahia.bmp")
    dirScreenshots = getPath("screenshots")

    try:
        dirScreenArribos, dirScreenPartidas = sacaScreenshots(url)
        time.sleep(2)
        generaPlacas_aire(dirSalida, dirScreenArribos, dirScreenPartidas, dirPlacaArribos, dirPlacaPartidas)
    except Exception as e:
        print(f"Error: {e}")
        

if __name__ == "__main__":
    dirSalida, url = leeTxt()
    generaPlaca(dirSalida, url)
    schedule.every().hour.at(":06").do(lambda: generaPlaca(dirSalida, url))

    while True:
        schedule.run_pending()
        time.sleep(1)