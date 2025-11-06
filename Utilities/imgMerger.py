"Este .py es una utility que el main va a llamar para hacer el merge de la imagen de la placa con la de los vuelos"
"Se llama de la siguiente manera:"
"python imgMerger.py *placaPath* *vuelosPath*"

import sys
from PIL import Image

def generaImg(placaPath,vuelosPath):
    placa = Image.open