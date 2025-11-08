#Este programa llama a los 10 minutos de cada hora al programa que saca el screenshto
import subprocess
import schedule
import time
import os


#FALTA HACER LOS CAMBIOS NECESARIOS PARA HACER LO MISMO CON LAS 2 PLACAS: PARTIDAS Y ARRIBOS
#TENER EN CUENTA QUE ACTUALMENTE LE ESTA SACANDO FOTO A LAS PARTIDAS, NO A LOS ARRIBOS, MANEJAR ESO EN SCREENSHOT.PY

def leeTxt():

    "Esta funcion se encarga de leer el .txt y ver que parámetro fue el que se específicó."
    "si no se especifica alguno de los dos (o los 2), defaultea a lo que está escrito en el readme.txt."

    try:
        with open("datosvuelos.txt", "r", encoding="utf-8") as arch:
            lineasArch = [linea.strip() for linea in arch.readlines()]

            if len(lineasArch) == 2:
                # [0] = dir ; [1] = url
                return lineasArch[0], lineasArch[1]

            elif len(lineasArch) == 1:
                if lineasArch[0].lower() == 'h':  # ignora mayúsculas/minúsculas
                    return r"C:\Placas\aire\HD", lineasArch[0]
                else:
                    return lineasArch[0], "https://www.aeropuertosargentina.com/es/vuelos?movtp=partidas&idarpt=Mar%20del%20Plata%2C%20MDQ"

            else:
                return r"C:\Placas\aire\HD", "https://www.aeropuertosargentina.com/es/vuelos?movtp=partidas&idarpt=Mar%20del%20Plata%2C%20MDQ"
    except FileNotFoundError:
        return r"C:\Placas\aire\HD", "https://www.aeropuertosargentina.com/es/vuelos?movtp=partidas&idarpt=Mar%20del%20Plata%2C%20MDQ" 

def generaPlaca(dirSalida,url,dirPlacaArribos,dirPlacaPartidas,dirArribos,dirPartidas):
    print("Generando placas...")
    subprocess.run(["python","Utilities/screenshot.py",f"{url}"]) #Crea los dos screenshots

    dirSalidaArribos = os.path.join(dirSalida,"arribos.bmp")
    subprocess.run(["python","Utilities/imgMerger.py",f"{dirPlacaArribos}",f"{dirArribos}",f"{dirSalidaArribos}"]) #crea placaArribos

    dirSalidaPartidas = os.path.join(dirSalida,"partidas.bmp")
    subprocess.run(["python","Utilities/imgMerger.py",f"{dirPlacaPartidas}",f"{dirPartidas}",f"{dirSalidaPartidas}"]) #crea placaPartidas


dirSalida, url = leeTxt() #dirSalida tiene la direccion de donde guardar la placa terminada.

dirPlacaArribos = r"placas/placaArribos.png" #direccion de la placa de arribos para el imgMerger.
dirPlacaPartidas = r"placas/placaPartidas.png" #direccion de la placa de partidas para el imgMerger.

dirArribos = os.path.join("screenshots","vuelosArribos.png") #dirección del screenshot de arribos.
dirPartidas = os.path.join("screenshots","vuelosPartidas.png") #dirección del screenshot de partidas.

generaPlaca(dirSalida,url,dirPlacaArribos,dirPlacaPartidas,dirArribos,dirPartidas)

print("Esperando a la hora xx:10...")

schedule.every().hour.at(":10").do(lambda: generaPlaca(dirSalida,url,dirPlacaArribos,dirPlacaPartidas,dirArribos,dirPartidas))



while True:
    schedule.run_pending()
    time.sleep(1)
