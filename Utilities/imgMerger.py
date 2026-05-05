"""
Mueve arbitrariamente 50 px para abajo la imagen para encajarla con la placa.
"""

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

    # Verifica primero que existan la placa y el screenshot
    if(not verificar_archivo(placaPath)):
        sys.exit(1)

    if(not verificar_archivo(vuelosPath)):
        sys.exit(1)
    
    placa = Image.open(placaPath).convert("RGBA")
    vuelos = Image.open(vuelosPath).convert("RGBA")

    # --- REESCALADO PARA 1920x1080 ---
    # Queremos que los vuelos ocupen el ancho total de la placa (1920)
    nuevo_ancho = 1920
    # Calculamos el alto proporcional para no deformar la tabla de vuelos
    proporcion = nuevo_ancho / float(vuelos.width)
    nuevo_alto = int(float(vuelos.height) * proporcion)

    vuelos = vuelos.resize(
        (nuevo_ancho, nuevo_alto),
        Image.LANCZOS
    )

    # --- CÁLCULO DE CENTRO ---
    # Horizontalmente queda en 0 porque ya mide 1920
    posX = 0
    # Verticalmente lo centramos respecto a los 1080 de la placa
    posY = ((placa.height - vuelos.height) // 2) + 50

    # Crear nueva imagen combinada (RGBA)
    resultado = Image.new("RGBA", (1920, 1080))
    resultado.paste(placa, (0, 0)) 
    
    # Pegamos los vuelos usando su propio canal alfa como máscara
    resultado.paste(vuelos, (posX, posY), vuelos)

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
