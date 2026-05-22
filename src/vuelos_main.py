import schedule
import time
import os

from screenshot import sacaScreenshots
from imgMerger import generaPlacas_aire

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def leeTxt():
    """
    Lee el archivo datosvuelos.txt y obtiene la carpeta de salida y la URL.
    Si no existe o está incompleto, usa valores por defecto.
    """
    default_dir = r"C:\Placas\aire\HD"
    default_url = "https://www.aeropuertosargentina.com/es/vuelos?movtp=partidas&idarpt=Mar%20del%20Plata%2C%20MDQ"

    config_path = os.path.join(BASE_DIR, "datosvuelos.txt")

    try:
        with open(config_path, "r", encoding="utf-8") as arch:
            lineas = [linea.strip() for linea in arch.readlines()]

        if len(lineas) == 2:
            return lineas[0], lineas[1]
        elif len(lineas) == 1:
            if lineas[0].lower() == 'h': 
                return default_dir, lineas[0]
            else:
                return lineas[0], default_url
        else:
            return default_dir, default_url

    except FileNotFoundError:
        return default_dir, default_url

def generaPlaca(dirSalida, url):
    print("Hora actual: " + time.strftime("%H:%M:%S"))
    print("Generando placas...\n")
    dirPlacaArribos = os.path.join(BASE_DIR, "..", "placas", "placaArribos.png") # Dirección de las placas vacías
    dirPlacaPartidas = os.path.join(BASE_DIR, "..", "placas", "placaPartidas.png")

    dirScreenshots = os.path.join(BASE_DIR, "..", "screenshots") # Dirección de la carpeta donde se guardan los screens
    claseHtml = r".flex.flex-col.space-5.mb-6.xl\:mb-8.w-full" #Clase HTML del cuadro de vuelos

    try:
        dirScreenArribos, dirScreenPartidas = sacaScreenshots(dirScreenshots, url, claseHtml) # Saca los screenshots de la página y guarda sus paths.
        time.sleep(2)
        generaPlacas_aire(dirSalida, dirScreenArribos, dirScreenPartidas, dirPlacaArribos, dirPlacaPartidas) # Combina screenshots con placas.
    except Exception as e:
        print(f"No se pudieron generar las placas.")

if __name__ == "__main__":
    dirSalida, url = leeTxt()

    generaPlaca(dirSalida, url) #Genera placas cuando arranca el programa

    print("Esperando a la hora xx:06...")
    schedule.every().hour.at(":06").do(lambda: generaPlaca(dirSalida, url))

    while True:
        schedule.run_pending()
        time.sleep(1)