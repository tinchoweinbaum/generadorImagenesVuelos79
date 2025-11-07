#Este programa llama a los 10 minutos de cada hora al programa que saca el screenshto

import subprocess
import schedule
import time
import os


#FALTA HACER LOS CAMBIOS NECESARIOS PARA HACER LO MISMO CON LAS 2 PLACAS: PARTIDAS Y ARRIBOS

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
                    return r"D:\Placas\MDQ", lineasArch[0]
                else:
                    return lineasArch[0], "https://www.aeropuertosargentina.com/es/vuelos?movtp=partidas&idarpt=Mar%20del%20Plata%2C%20MDQ"

            else:
                return r"D:\Placas\MDQ", "https://www.aeropuertosargentina.com/es/vuelos?movtp=partidas&idarpt=Mar%20del%20Plata%2C%20MDQ"
    except FileNotFoundError:
        print("No existe datosvuelos.txt")   

def generaPlaca(dir,url,dirPlacaArribos,dirVuelos,dirSalida):
    subprocess.run(["python","Utilities/screenshot.py",f"{url}"])
    subprocess.run(["python","Utilities/imgMerger.py",f"{dirPlacaArribos}",f"{dirArribos}",f"{dirSalida}"])
    print("Esperando a la hora xx:10...")

dirSalida, url = leeTxt() #dir tiene la direccion de donde guardar la placa terminada.

dirPlacaArribos = r"placas/placaArribos.png" #direccion de la placa de arribos para el imgMerger.
dirPlacaPartidas = r"placas/placaPartidas.png" #direccion de la placa de partidas para el imgMerger.

dirArribos = os.path.join("screenshots","vuelosArribos.png") #dirección del screenshot de arribos.
dirPartidas = os.path.join("screenshots","vuelosPartidas.png") #dirección del screenshot de partidas.

print("Esperando a la hora xx:10...")

schedule.every().hour.at(":50").do(lambda: generaPlaca(dirArribos,url,dirPlacaArribos,dirArribos,dirSalida))

while True:
    schedule.run_pending()
    time.sleep(1)
