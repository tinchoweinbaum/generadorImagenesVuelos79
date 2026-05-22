from PIL import Image
import sys
import os

def getPath(ruta_relativa):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, ruta_relativa)
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ruta_relativa)

def verificar_archivo(path):
    """Verifica que un archivo exista y sea accesible."""
    if not os.path.isfile(path):
        print(f"\nERROR: No se encontró la imagen {path}")
        return False

    try:
        Image.open(path).verify()  # verificar que sea una imagen válida
    except Image.UnidentifiedImageError:
        print(f"\nERROR: El archivo no es una imagen válida")
        return False
    except Exception as e:
        print(f"\nERROR: No se pudo leer {path}\n{e}")
        return False
    
    return True 

def generaImg(placaPath, vuelosPath, salidaDir):

    if(not verificar_archivo(placaPath)):
        sys.exit(1)

    if(not verificar_archivo(vuelosPath)):
        sys.exit(1)

    placa = Image.open(placaPath).convert("RGBA")  
    vuelos = Image.open(vuelosPath).convert("RGBA")

    # Calcular centro
    posX = (placa.width - vuelos.width) // 2
    posY = round((placa.height - placa.height * 0.71))

    # Crear nueva imagen combinada (RGBA)
    resultado = Image.new("RGBA", placa.size)
    resultado.paste(placa, (0, 0)) 
    resultado.paste(vuelos, (posX, posY), vuelos)

    # Guardar en formato compatible
    os.makedirs(os.path.dirname(salidaDir), exist_ok=True)
    resultado.save(salidaDir)
    print(f"Placa creada en {salidaDir}.")

def generaPlacas_aire(dirSalida, screenArribos, screenPartidas, placaArribos, placaPartidas):
    """
    Recibe la dirección de los 2 screenshots junto con la de las placas.
    """
    # Se asegura que el directorio de salida sea absoluto
    dirFinalArribos = os.path.join(dirSalida, "arribos.bmp")
    generaImg(placaArribos, screenArribos, dirFinalArribos)

    dirFinalPartidas = os.path.join(dirSalida, "partidas.bmp")
    generaImg(placaPartidas, screenPartidas, dirFinalPartidas)

    return dirFinalArribos, dirFinalPartidas

if __name__ == "__main__":
    pass