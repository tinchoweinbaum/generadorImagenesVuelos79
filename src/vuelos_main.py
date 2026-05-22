import schedule
import time
import os
import sys

from screenshot import sacaScreenshots
from imgMerger import generaPlacas_aire

def getPath(ruta_relativa):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, ruta_relativa)
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ruta_relativa)

def leeTxt():
    # Usamos os.getcwd() para buscar el archivo .txt al lado del .exe
    config_path = os.path.join(os.getcwd(), "datosvuelos.txt")
    default_dir = r"C:\Placas\aire\HD"
    default_url = "https://www.aeropuertosargentina.com/es/vuelos?movtp=partidas&idarpt=Mar%20del%20Plata%2C%20MDQ"

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
    dirPlacaArribos = getPath("placas/placaArribos.png")
    dirPlacaPartidas = getPath("placas/placaPartidas.png")
    dirScreenshots = getPath("screenshots")
    
    claseHtml = r".flex.flex-col.space-5.mb-6.xl\:mb-8.w-full"

    try:
        dirScreenArribos, dirScreenPartidas = sacaScreenshots(dirScreenshots, url, claseHtml)
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