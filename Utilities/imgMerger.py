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

    # 1. Ajuste de ancho fijo a 1920
    # Esto mantiene la proporción pero asegura que cubra la pantalla de lado a lado
    nuevo_ancho = 1920
    proporcion = nuevo_ancho / float(vuelos.width)
    nuevo_alto = int(float(vuelos.height) * proporcion)

    vuelos = vuelos.resize((nuevo_ancho, nuevo_alto), Image.LANCZOS)

    # 2. POSICIONAMIENTO FIJO (El "Ancla")
    # En lugar de centrar verticalmente, fijamos donde empieza la tabla.
    # Según tu configuración anterior donde con 4 vuelos quedaba bien:
    posX = 0
    
    # Ajustamos posY para que sea una constante. 
    # Si antes usabas (placa.height * 0.29) aprox, lo fijamos ahí:
    posY = 310  # <--- AJUSTÁ ESTE VALOR (en píxeles) para que alinee con el cabezal de tu placa

    # 3. Crear resultado
    resultado = Image.new("RGBA", (1920, 1080))
    resultado.paste(placa, (0, 0)) 
    
    # Pegamos los vuelos. Si hay pocos, quedará espacio libre ABAJO (lo cual es natural).
    # Si hay muchos, crecerá hacia abajo.
    resultado.paste(vuelos, (posX, posY), vuelos)

    os.makedirs(os.path.dirname(salidaDir), exist_ok=True)
    resultado.save(salidaDir)
    print(f"Placa creada en {salidaDir}.")

if __name__ == "__main__":
    if len(sys.argv) < 4:
        sys.exit(1)
    generaImg(sys.argv[1], sys.argv[2], sys.argv[3])