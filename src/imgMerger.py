import os

from PIL import Image, ImageDraw, ImageFont

from config import getPath

_Y_TABLA = 0.29
_AZUL = (0, 82, 179, 255)
_GRIS = (90, 90, 90, 255)


def verificar_archivo(path):
    if not os.path.isfile(path):
        print(f"\nERROR: No se encontro la imagen {path}")
        return False

    try:
        Image.open(path).verify()
    except Image.UnidentifiedImageError:
        print("\nERROR: El archivo no es una imagen valida")
        return False
    except Exception as e:
        print(f"\nERROR: No se pudo leer {path}\n{e}")
        return False

    return True


def _cargar_fuente(size, bold=False):
    if bold:
        candidatos = [
            r"C:\Windows\Fonts\segoeuib.ttf",
            r"C:\Windows\Fonts\arialbd.ttf",
        ]
    else:
        candidatos = [
            r"C:\Windows\Fonts\segoeui.ttf",
            r"C:\Windows\Fonts\arial.ttf",
        ]
    for ruta in candidatos:
        if os.path.isfile(ruta):
            return ImageFont.truetype(ruta, size)
    return ImageFont.load_default()


def crear_placa_sin_vuelos(placa_base, destino):
    placa = Image.open(placa_base).convert("RGBA")
    overlay = Image.new("RGBA", placa.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    y_tabla = round(placa.height * _Y_TABLA)
    draw.rectangle((0, y_tabla, placa.width, placa.height), fill=(255, 255, 255, 235))

    font_titulo = _cargar_fuente(72, bold=True)
    font_sub = _cargar_fuente(36, bold=False)
    titulo = "No hay vuelos"
    sub = "No flights"

    bbox = draw.textbbox((0, 0), titulo, font=font_titulo)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    x = (placa.width - tw) // 2
    y = y_tabla + (placa.height - y_tabla) // 2 - th // 2 - 20
    draw.text((x, y), titulo, font=font_titulo, fill=_AZUL)

    bbox2 = draw.textbbox((0, 0), sub, font=font_sub)
    tw2 = bbox2[2] - bbox2[0]
    draw.text(((placa.width - tw2) // 2, y + th + 18), sub, font=font_sub, fill=_GRIS)

    resultado = Image.alpha_composite(placa, overlay)
    os.makedirs(os.path.dirname(destino) or ".", exist_ok=True)
    resultado.save(destino)
    return destino


def asegurar_placa_sin_vuelos(placa_base, placa_vacio):
    if os.path.isfile(placa_vacio):
        return placa_vacio
    print(f"No estaba la placa 'No hay vuelos', se genera desde {placa_base}")
    return crear_placa_sin_vuelos(placa_base, placa_vacio)


def generaImg(placaPath, vuelosPath, salidaDir):
    if not verificar_archivo(placaPath) or not verificar_archivo(vuelosPath):
        return False

    placa = Image.open(placaPath).convert("RGBA")
    vuelos = Image.open(vuelosPath).convert("RGBA")

    posX = (placa.width - vuelos.width) // 2
    posY = round(placa.height * _Y_TABLA)

    resultado = Image.new("RGBA", placa.size)
    resultado.paste(placa, (0, 0))
    resultado.paste(vuelos, (posX, posY), vuelos)

    os.makedirs(os.path.dirname(salidaDir) or ".", exist_ok=True)
    resultado.save(salidaDir)
    print(f"Placa creada en {salidaDir}.")
    return True


def publicaPlacaSinVuelos(placa_base, placa_vacio, salidaDir):
    ruta = asegurar_placa_sin_vuelos(placa_base, placa_vacio)
    if not verificar_archivo(ruta):
        return False

    os.makedirs(os.path.dirname(salidaDir) or ".", exist_ok=True)
    Image.open(ruta).convert("RGB").save(salidaDir)
    print(f"Placa 'No hay vuelos' publicada en {salidaDir}.")
    return True


def _publicar(dirSalida, nombre, captura, placa, placa_vacio):
    destino = os.path.join(dirSalida, nombre)
    if captura.estado == "ok" and captura.path:
        return generaImg(placa, captura.path, destino)
    if captura.estado == "sin_vuelos":
        return publicaPlacaSinVuelos(placa, placa_vacio, destino)

    print(f"No se actualiza {nombre}: error de captura. Se mantiene la placa anterior.")
    return False


def generaPlacas_aire(
    dirSalida,
    cap_arribos,
    cap_partidas,
    placaArribos,
    placaPartidas,
    placaArribosVacio=None,
    placaPartidasVacio=None,
):
    if placaArribosVacio is None:
        placaArribosVacio = getPath("placas/placaArribosSinVuelos.png")
    if placaPartidasVacio is None:
        placaPartidasVacio = getPath("placas/placaPartidasSinVuelos.png")

    _publicar(dirSalida, "arribos.bmp", cap_arribos, placaArribos, placaArribosVacio)
    _publicar(dirSalida, "partidas.bmp", cap_partidas, placaPartidas, placaPartidasVacio)


if __name__ == "__main__":
    crear_placa_sin_vuelos(
        getPath("placas/placaArribos.png"),
        getPath("placas/placaArribosSinVuelos.png"),
    )
    crear_placa_sin_vuelos(
        getPath("placas/placaPartidas.png"),
        getPath("placas/placaPartidasSinVuelos.png"),
    )
    print("Placas 'No hay vuelos' generadas.")
