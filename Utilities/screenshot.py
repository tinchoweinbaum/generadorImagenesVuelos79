import os
import sys
import time
from datetime import datetime
from playwright.sync_api import sync_playwright

def sacaScreenshot(url, seccion, folder):
    output = os.path.join(folder, "vuelosPartidas.png" if seccion == "salidas" else "vuelosArribos.png")
    dia_actual = datetime.now().strftime("%d")

    if os.path.exists(output): os.remove(output)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            viewport={'width': 1280, 'height': 5000},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            locale='es-AR',       # Fuerza el idioma español de Argentina
            timezone_id='America/Argentina/Buenos_Aires' # Clava la zona horaria local para que las horas coincidan
        )
        page = context.new_page()
        try:
            page.goto(url)
            
            # Un pequeño delay para asegurar la carga visual antes de medir
            time.sleep(4)

            # --- PASO 1: FILTRAR SOLO HOY ---
            # Capturamos únicamente las filas reales de vuelos que tengan el número de día de hoy
            filas_hoy = [f for f in page.query_selector_all("tr.tt-row:not(.tt-child)")
                         if dia_actual in (f.query_selector("td.tt-d").inner_text() if f.query_selector("td.tt-d") else "")]

            if filas_hoy:
                # El inicio de la captura es el primer vuelo de hoy, el fin es el último vuelo de hoy
                target_rows = [filas_hoy[0], filas_hoy[-1]]
            else:
                # Si por alguna razón quedó vacía, usamos el último elemento disponible de la tabla por seguridad
                todas_las_filas = page.query_selector_all("table.tt tr")
                target_rows = [todas_las_filas[-1], todas_las_filas[-1]] if todas_las_filas else []

            # --- PASO 2: RECORTE Y CAPTURA ---
            if target_rows:
                box_inicio = target_rows[0].bounding_box()
                box_fin = target_rows[-1].bounding_box()

                if box_inicio and box_fin:
                    area = {
                        "x": box_inicio["x"],
                        "y": box_inicio["y"],
                        "width": box_inicio["width"],
                        "height": max(100, (box_fin["y"] + box_fin["height"]) - box_inicio["y"])
                    }
                    os.makedirs(folder, exist_ok=True)
                    page.screenshot(path=output, clip=area)

        except Exception as e:
            print(f"Error al sacar screenshot de {seccion}: {e}")
        finally:
            browser.close()

if __name__ == "__main__":
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    OUTPUT_FOLDER = os.path.normpath(os.path.join(BASE_DIR, "..", "screenshots"))

    sacaScreenshot("https://www.avionio.com/es/airport/bhi/departures", "salidas", OUTPUT_FOLDER)
    sacaScreenshot("https://www.avionio.com/es/airport/bhi/arrivals", "llegadas", OUTPUT_FOLDER)