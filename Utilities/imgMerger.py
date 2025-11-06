from PIL import Image
import sys
import os

def generaImg(placaPath, vuelosPath, salidaDir):
    placa = Image.open(placaPath).convert("RGBA")
    vuelos = Image.open(vuelosPath).convert("RGBA")
 
    vuelos = vuelos.resize((vuelos.width // 1.2,vuelos.height // 1.2)) #Reduce vuelos a la mitad de su tamaño

    # Calcular centro
    posX = (placa.width - vuelos.width) // 2
    posY = (placa.height - vuelos.height) // 2

    # Crear nueva imagen combinada (RGBA)
    resultado = Image.new("RGBA", placa.size)
    resultado.paste(placa, (0, 0)) #Copia la placa de vuelos a una nueva imagen para pegarle los vuelos encima
    resultado.paste(vuelos, (posX, posY), vuelos)  #Pega la imagen de vuelos encima de la placa, en el centro.

    # Guardar en formato compatible
    salidaPath = os.path.join(salidaDir,"salida.png")
    resultado.save(salidaPath)
    print(f"Salida creada en {salidaPath}.")

if len(sys.argv) < 4:
    print("Uso: python imgMerger.py *placaPath* *vuelosPath* *salidaPath*")
    sys.exit(1)

placaPath = sys.argv[1]
vuelosPath = sys.argv[2]
salidaDir = sys.argv[3]

generaImg(placaPath, vuelosPath, salidaDir)
