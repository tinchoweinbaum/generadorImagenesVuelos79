from PIL import Image
import sys
import os

def existeImagen(path):
    try:
        with Image.open(path) as img:
            img.verify()   # Verifica que no esté corrupta
        return True
    except Exception:
        return False

def generaImg(placaPath, vuelosPath, salidaDir):

    if(not existeImagen(placaPath)):
        print("No se encontró la placa de")


    placa = Image.open(placaPath).convert("RGBA")
    vuelos = Image.open(vuelosPath).convert("RGBA")

    # Calcular centro
    posX = (placa.width - vuelos.width) // 2
    posY = round((placa.height - placa.height * 0.71))

    # Crear nueva imagen combinada (RGBA)
    resultado = Image.new("RGBA", placa.size)
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
