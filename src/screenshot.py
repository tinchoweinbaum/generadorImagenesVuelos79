import os
import re
import time

import requests
from PIL import Image
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from playwright.sync_api import sync_playwright

from config import getPath

OK = "ok"
SIN_VUELOS = "sin_vuelos"
ERROR = "error"

_FRASES_SIN_VUELOS = (
    "no hay vuelos",
    "sin vuelos",
    "no hay resultados",
    "no se encontraron vuelos",
    "no se encontro vuelos",
    "no se encontraron resultados",
    "no encontramos vuelos",
    "no flights",
    "there are no flights",
    "no hay informacion",
    "no hay información",
)
_RE_HORA = re.compile(r"\b\d{1,2}:\d{2}\b")
_ALTURA_MINIMA = 40


class Captura:
    def __init__(self, estado, path=None):
        self.estado = estado
        self.path = path


def paginaActiva(url, timeout=15):
    try:
        resp = requests.get(url, timeout=timeout)
        return resp.status_code == 200
    except requests.RequestException:
        return False


def texto_tiene_vuelos(texto, altura=None, altura_min=_ALTURA_MINIMA):
    if altura is not None and altura < altura_min:
        return False
    t = (texto or "").strip()
    if not t:
        return False
    low = t.lower()
    if any(frase in low for frase in _FRASES_SIN_VUELOS):
        return False
    return bool(_RE_HORA.search(t))


def _elemento_tiene_vuelos(elemento):
    try:
        texto = elemento.inner_text() or ""
    except Exception:
        texto = ""
    try:
        box = elemento.bounding_box()
        altura = box["height"] if box else None
    except Exception:
        altura = None
    return texto_tiene_vuelos(texto, altura)


def cropScreenshotRight(pathFoto, porcentaje=0.129):
    screenshot = Image.open(pathFoto)
    width, height = screenshot.size
    widthCrop = int(width * (1 - porcentaje))
    screenshot = screenshot.crop((0, 0, widthCrop, height))
    screenshot.save(pathFoto)


def _cerrar_popup(tab, clase_cerrar):
    if not clase_cerrar:
        return
    elem = tab.query_selector(clase_cerrar)
    if elem:
        elem.click()


def _guardar_screenshot(elemento, dest, crop):
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    elemento.screenshot(path=dest)
    screenshot = Image.open(dest)
    if screenshot.height < 50:
        return False
    screenshot = screenshot.resize(
        (int(screenshot.width * 1.5), int(screenshot.height * 1.5)),
        Image.LANCZOS,
    )
    screenshot.save(dest)
    cropScreenshotRight(dest, crop)
    return True


def _pagina_dice_sin_vuelos(tab):
    try:
        texto = tab.inner_text("body") or ""
    except Exception:
        return False, False
    return (
        any(frase in texto.lower() for frase in _FRASES_SIN_VUELOS),
        bool(_RE_HORA.search(texto)),
    )


def _capturar_lista(tab, clase_div, dest, crop):
    time.sleep(1)
    dice_vacio, tiene_horarios = _pagina_dice_sin_vuelos(tab)
    if dice_vacio:
        print("La pagina indica que no hay vuelos. Se publica la placa 'No hay vuelos'.")
        return Captura(SIN_VUELOS)

    try:
        elemento = tab.wait_for_selector(clase_div, timeout=10000, state="attached")
    except PlaywrightTimeoutError:
        if tiene_horarios:
            print("Hay horarios en la pagina pero no se encontro la clase configurada. No se actualiza la placa.")
            return Captura(ERROR)
        print("No se encontro la lista de vuelos. Se publica la placa 'No hay vuelos'.")
        return Captura(SIN_VUELOS)
    except Exception as e:
        print(f"Error buscando la lista de vuelos: {e}")
        return Captura(ERROR)

    if not _elemento_tiene_vuelos(elemento):
        print("La lista no tiene vuelos. Se publica la placa 'No hay vuelos'.")
        return Captura(SIN_VUELOS)

    try:
        if not _guardar_screenshot(elemento, dest, crop):
            print("El screenshot de vuelos quedo vacio o roto. Se publica la placa 'No hay vuelos'.")
            return Captura(SIN_VUELOS)
    except Exception as e:
        print(f"No se pudo sacar el screenshot: {e}")
        return Captura(ERROR)

    return Captura(OK, dest)


def sacaScreenPartidas(cfg):
    dest = getPath("screenshots/vuelosPartidas.png")

    with sync_playwright() as p:
        navegador = None
        try:
            navegador = p.chromium.launch(headless=True)
            tab = navegador.new_page()
            tab.goto(cfg.url, wait_until="load")
            tab.wait_for_load_state("networkidle")
            _cerrar_popup(tab, cfg.clase_cerrar)
            return _capturar_lista(tab, cfg.clase, dest, cfg.crop)
        except Exception as e:
            print(f"Error capturando partidas: {e}")
            return Captura(ERROR)
        finally:
            if navegador is not None:
                navegador.close()


def sacaScreenArribos(cfg):
    dest = getPath("screenshots/vuelosArribos.png")

    with sync_playwright() as p:
        navegador = None
        try:
            navegador = p.chromium.launch(headless=True)
            tab = navegador.new_page()
            tab.goto(cfg.url, wait_until="load")
            tab.wait_for_load_state("networkidle")
            _cerrar_popup(tab, cfg.clase_cerrar)

            if cfg.clase_arribos:
                elem_arribos = tab.query_selector(cfg.clase_arribos)
                if not elem_arribos:
                    print("No se encontro el tab de arribos. No se actualiza esa placa.")
                    return Captura(ERROR)
                elem_arribos.click()
                tab.wait_for_load_state("networkidle")
                time.sleep(1)

            return _capturar_lista(tab, cfg.clase, dest, cfg.crop)
        except Exception as e:
            print(f"Error capturando arribos: {e}")
            return Captura(ERROR)
        finally:
            if navegador is not None:
                navegador.close()


def sacaScreenshots(cfg):
    if not paginaActiva(cfg.url):
        print("La pagina no se encuentra activa, no existe, o tardo demasiado en responder.")
        print("No se actualizan las placas para no mandar al aire una imagen rota.")
        return Captura(ERROR), Captura(ERROR)

    cap_arribos = sacaScreenArribos(cfg)
    cap_partidas = sacaScreenPartidas(cfg)
    return cap_arribos, cap_partidas
