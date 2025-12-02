from PIL import Image, UnidentifiedImageError
import sys
import os

def verificar_archivo(path):
    """Verifica que un archivo exista y sea accesible."""
    if not os.path.isfile(path):
        print(f"\nERROR: No se encontró la imagen {path}")
        return False

    try:
        Image.open(path).verify()  # verificar que sea una imagen válida
    except UnidentifiedImageError:
        print(f"\nERROR: El archivo no es una imagen válida")
        return False
    except Exception as e:
        print(f"\nERROR: No se pudo leer {path}\n{e}")
        return False
    
    return True #Si llega al final de la funcion es que exsite

def generaImg(placaPath, vuelosPath, salidaDir):

    #Verifica primero que existan la placa y el screenshot
    if(not verificar_archivo(placaPath)):
        sys.exit(1)

    if(not verificar_archivo(vuelosPath)):
        sys.exit(1)
    
    placa = Image.open(placaPath).convert("RGBA")
    vuelos = Image.open(vuelosPath).convert("RGBA")

    vuelos = vuelos.resize(
        (vuelos.width * 3, vuelos.height * 3),
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
