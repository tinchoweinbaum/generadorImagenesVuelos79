from PIL import Image
import sys
import os

def generaImg(placaPath, vuelosPath, salidaDir):
    placa = Image.open(placaPath).convert("RGBA")
    vuelos = Image.open(vuelosPath).convert("RGBA")

    vuelos = vuelos.resize(
        (vuelos.width * 2, vuelos.height * 2),
        Image.LANCZOS
    )

    # Calcular centro
    posX = (placa.width - vuelos.width) // 2
    posY = round((placa.height - placa.height * 0.71))

    # Crear nueva imagen combinada (RGBA)
    resultado = Image.new("RGBA", (1920,1080))
    resultado.paste(placa, (0, 0)) #Copia la placa de vuelos a una nueva imagen para pegarle los vuelos encima
    resultado.paste(vuelos, (posX, posY), vuelos)  #Pega la imagen de vuelos encima de la placa, en el centro.

    # Guardar en formato compatible
    os.makedirs(os.path.dirname(salidaDir), exist_ok=True)
    resultado.save(salidaDir)
    print(f"Placa creada en {salidaDir}.")

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Uso: python imgMerger.py *placaPath* *vuelosPath* *salidaPath*")
        sys.exit(1)

    placaPath = sys.argv[1]
    vuelosPath = sys.argv[2]
    salidaDir = sys.argv[3]

    generaImg(placaPath, vuelosPath, salidaDir)
