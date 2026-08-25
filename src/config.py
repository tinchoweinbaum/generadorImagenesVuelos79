import os
import sys
from dataclasses import dataclass


DEFAULT_DIR = r"C:\Placas\aire\HD"
DEFAULT_URL = (
    "https://www.aeropuertosargentina.com/es/vuelos"
    "?movtp=partidas&idarpt=Mar%20del%20Plata%2C%20MDQ"
)
DEFAULT_CLASE = r".flex.flex-col.space-5.mb-6.xl\:mb-8.w-full"
DEFAULT_CLASE_ARRIBOS = (
    r".group.inline-flex.items-center.border-b-2.py-2.xl\:py-2.px-3"
    r".lg\:px-4.font-open.text-sm.font-semibold.leading-4.space-3"
    r".cursor-pointer.border-transparent.text-gray-500"
)
DEFAULT_CLASE_CERRAR = ".fill-none.stroke-white"
DEFAULT_CROP = 0.129

_CLAVES = {
    "dir": "dir",
    "directorio": "dir",
    "carpeta": "dir",
    "url": "url",
    "clase": "clase",
    "clase_html": "clase",
    "selector": "clase",
    "clase_arribos": "clase_arribos",
    "clase_cerrar": "clase_cerrar",
    "crop": "crop",
}


@dataclass
class ConfigVuelos:
    dir: str = DEFAULT_DIR
    url: str = DEFAULT_URL
    clase: str = DEFAULT_CLASE
    clase_arribos: str = DEFAULT_CLASE_ARRIBOS
    clase_cerrar: str = DEFAULT_CLASE_CERRAR
    crop: float = DEFAULT_CROP


def getPath(ruta_relativa):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, ruta_relativa)
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ruta_relativa)


def _limpia(valor):
    return valor.strip().strip('"').strip("'")


def _aplica_clave(cfg: ConfigVuelos, clave, valor):
    campo = _CLAVES[clave]
    valor = _limpia(valor)
    if not valor:
        return
    if campo == "crop":
        try:
            cfg.crop = float(valor.replace(",", "."))
        except ValueError:
            print(f"Valor de crop invalido ({valor}), se usa {cfg.crop}.")
        return
    setattr(cfg, campo, valor)


def _parsear_lineas(lineas):
    cfg = ConfigVuelos()
    posicioneles = []
    uso_claves = False

    for cruda in lineas:
        linea = cruda.strip()
        if not linea or linea.startswith("#"):
            continue

        if "=" in linea:
            clave, valor = linea.split("=", 1)
            clave = clave.strip().lower()
            if clave in _CLAVES:
                uso_claves = True
                _aplica_clave(cfg, clave, valor)
                continue

        posicioneles.append(linea)

    if posicioneles and not uso_claves:
        if len(posicioneles) >= 1:
            cfg.dir = _limpia(posicioneles[0]) or cfg.dir
        if len(posicioneles) >= 2:
            cfg.url = _limpia(posicioneles[1]) or cfg.url
        if len(posicioneles) >= 3:
            cfg.clase = _limpia(posicioneles[2]) or cfg.clase
        if len(posicioneles) >= 4:
            cfg.clase_arribos = _limpia(posicioneles[3]) or cfg.clase_arribos
        if len(posicioneles) >= 5:
            cfg.clase_cerrar = _limpia(posicioneles[4]) or cfg.clase_cerrar

    return cfg


def _rutas_config():
    yield os.path.join(os.getcwd(), "datosvuelos.txt")
    yield getPath("datosvuelos.txt")


def lee_config():
    for ruta in _rutas_config():
        try:
            with open(ruta, "r", encoding="utf-8") as arch:
                cfg = _parsear_lineas(arch.readlines())
            print(f"Config leida de {ruta}")
            return cfg
        except FileNotFoundError:
            continue
        except OSError as e:
            print(f"No se pudo leer {ruta}: {e}")
            continue

    print("No se encontro datosvuelos.txt, usando valores por defecto.")
    return ConfigVuelos()
