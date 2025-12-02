import subprocess
import schedule
import time
import os


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def leeTxt():
    """
    Lee el archivo datosvuelos.txt y obtiene la carpeta de salida y la URL.
    Si no existe o está incompleto, usa valores por defecto.
    """
    default_dir = r"C:\Placas\aire\HD"
    default_url = "https://www.aeropuertobahiablanca.com/"

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
    print("")
    print("Hora actual: " + time.strftime("%H:%M:%S"))
    print("Generando placas...\n")

    screenshot_py = os.path.join(BASE_DIR, "Utilities", "screenshot.py")
    imgMerger_py = os.path.join(BASE_DIR, "Utilities", "imgMerger.py")

    dirPlacaArribos = os.path.join(BASE_DIR, "placas", "arribosBahia.bmp")
    dirPlacaPartidas = os.path.join(BASE_DIR, "placas", "partidasBahia.bmp")

    dirArribos = os.path.join(BASE_DIR, "screenshots", "vuelosArribos.png")
    dirPartidas = os.path.join(BASE_DIR, "screenshots", "vuelosPartidas.png")

    dirSalidaArribos = os.path.join(dirSalida, "arribos.bmp")
    dirSalidaPartidas = os.path.join(dirSalida, "partidas.bmp")

    try:
        subprocess.run(["python", screenshot_py, url], check=True)

        try:
            subprocess.run(["python", imgMerger_py, dirPlacaArribos, dirArribos, dirSalidaArribos],
                           check=True)
        except subprocess.CalledProcessError:
            print("No se pudo generar la placa de arribos.\n")

        try:
            subprocess.run(["python", imgMerger_py, dirPlacaPartidas, dirPartidas, dirSalidaPartidas],
                           check=True)
        except subprocess.CalledProcessError:
            print("No se pudo generar la placa de partidas.\n")

    except subprocess.CalledProcessError:
        print("No se pudieron generar las placas")
        return

dirSalida, url = leeTxt()

generaPlaca(dirSalida, url)

print("\nEsperando a la hora xx:10...")
schedule.every().hour.at(":10").do(lambda: generaPlaca(dirSalida, url))

while True:
    schedule.run_pending()
    time.sleep(1)
