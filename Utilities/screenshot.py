"Esto está recontra hardcodeado. Ignora completamente el argumento que recibe y usa la url de avionio"
import os
import sys
import time
from datetime import datetime
from playwright.sync_api import sync_playwright

import os
import time
from datetime import datetime
from playwright.sync_api import sync_playwright

def sacaScreenshot(url, seccion, folder):
    output = os.path.join(folder, "vuelosPartidas.png" if seccion == "salidas" else "vuelosArribos.png")
    dia_actual = datetime.now().strftime("%d")

    if os.path.exists(output): os.remove(output)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={'width': 1280, 'height': 5000})
        page = context.new_page()
        
        try:
            page.goto(url, wait_until="networkidle")
            
            # Buscamos filas del día actual
            filas_hoy = [f for f in page.query_selector_all("tr.tt-row:not(.tt-child)") 
                         if dia_actual in (f.query_selector("td.tt-d").inner_text() if f.query_selector("td.tt-d") else "")]

            if filas_hoy:
                target_rows = [filas_hoy[0], filas_hoy[-1]]
            else:
                # Buscamos todas las filas
                todas_las_filas = page.query_selector_all("table.tt tr")
                
                if todas_las_filas:
                    # Seleccionamos forzosamente la última fila
                    ultimo_elemento = todas_las_filas[-1]
                    
                    # Hacemos click en el último elemento (el cartel de 'Ver más' o similar)
                    ultimo_elemento.click()
                    
                    # Esperamos a que la web cargue el mensaje de "Sin vuelos"
                    time.sleep(3) 
                    
                    # Refrescamos la lista tras el click
                    todas_las_filas = page.query_selector_all("table.tt tr")
                    target_rows = [todas_las_filas[-1], todas_las_filas[-1]]
                else:
                    target_rows = []

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

    # IMPORTANTE: Asegurate de usar page=-1 para ver todo el listado
    sacaScreenshot("https://www.avionio.com/es/airport/bhi/departures?page=-1", "salidas", OUTPUT_FOLDER)
    sacaScreenshot("https://www.avionio.com/es/airport/bhi/arrivals?page=-1", "llegadas", OUTPUT_FOLDER)