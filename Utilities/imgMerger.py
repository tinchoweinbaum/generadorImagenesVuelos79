from PIL import Image, UnidentifiedImageError
import sys
import os

def verificar_archivo(path):
    if not os.path.isfile(path):
        print(f"\nERROR: No se encontró la imagen {path}")
        return False
    try:
        with Image.open(path) as img:
            img.verify()
    except:
        return False
    return True 

def generaImg(placaPath, vuelosPath, salidaDir):
    if(not verificar_archivo(placaPath)) or (not verificar_archivo(vuelosPath)):
        sys.exit(1)
    
    placa = Image.open(placaPath).convert("RGBA")
    vuelos = Image.open(vuelosPath).convert("RGBA")

    # 1. REDIMENSIONAR LA IMAGEN
    # Opción A: Escalar por porcentaje (Ej: 0.8 achica la imagen al 80%)
    escala = 2.5
    nuevo_ancho = int(vuelos.width * escala)
    nuevo_alto = int(vuelos.height * escala)

    # Opción B: Forzar un ancho específico menor a 1920 (Descomenta estas 3 líneas si prefieres esto)
    # nuevo_ancho = 1500  # Cambia esto al ancho que prefieras
    # proporcion = nuevo_ancho / float(vuelos.width)
    # nuevo_alto = int(float(vuelos.height) * proporcion)

    vuelos = vuelos.resize((nuevo_ancho, nuevo_alto), Image.LANCZOS)

    # 2. POSICIONAMIENTO
    # Como ahora la imagen es más chica que 1920, la centramos matemáticamente en el eje X
    posX = 0
    
    # Posición Y fija (el "Ancla") alineada al cabezal
    posY = 310  

    # 3. CREAR RESULTADO
    resultado = Image.new("RGBA", (1920, 1080))
    resultado.paste(placa, (0, 0)) 
    
    # Pegamos los vuelos usando la misma imagen como máscara alfa para conservar transparencias
    resultado.paste(vuelos, (posX, posY), vuelos)

    os.makedirs(os.path.dirname(salidaDir), exist_ok=True)
    resultado.save(salidaDir)
    print(f"Placa creada en {salidaDir}.")

if __name__ == "__main__":
    if len(sys.argv) < 4:
        sys.exit(1)
    generaImg(sys.argv[1], sys.argv[2], sys.argv[3])