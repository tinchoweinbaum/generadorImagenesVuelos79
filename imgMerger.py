"Este .py es una utility que el main va a llamar para hacer el merge de la imagen de la placa con la de los vuelos"
"Se llama de la siguiente manera:"
"python imgMerger.py *placaPath* *vuelosPath*"

import sys
from PIL import Image

def generaImg(placaPath,vuelosPath,salidaPath):
    placa = Image.open(placaPath).convert("RGBA")
    vuelos = Image.open(vuelosPath).convert("RGBA")

    posX = (placa.width - vuelos.width) // 2
    posY = (placa.height - vuelos.height) // 2

    placa.paste(vuelos,(posX,posY),vuelos)
    placa.save(salidaPath)

    print(f"{salidaPath} creada.")

if (len(sys.argv) < 3):
    print("Parametros insuficientes para imgMerger.py")
    sys.exit(1)

placaPath = sys.argv[1]
vuelosPath = sys.argv[2]
salidaPath = sys.argv[3]

generaImg(placaPath,vuelosPath,salidaPath)