import os
import sys
import time
from datetime import datetime
from playwright.sync_api import sync_playwright

def sacaScreenshot(url, seccion, folder):
    # Definir nombre de archivo
    if seccion == "salidas":
        output = os.path.join(folder, "vuelosPartidas.png")
    else:
        output = os.path.join(folder, "vuelosArribos.png")

    # Forzar fecha (tu manual del Windows)
    dia_actual = datetime.now().strftime("%d")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        # Viewport grande para que quepan todos los vuelos del día
        context = browser.new_context(viewport={'width': 1280, 'height': 8000})
        page = context.new_page()
        
        try:
            print(f"--- Iniciando captura de {seccion} ---")
            # Usamos la URL tal cual viene del Main
            page.goto(url, wait_until="domcontentloaded", timeout=60000)
            time.sleep(5) 

            # Obtenemos todas las filas de la tabla de Avionio
            filas = page.query_selector_all("table.tt tr")
            filas_de_hoy = []
            
            for fila in filas:
                celda_fecha = fila.query_selector("td.tt-d")
                if celda_fecha:
                    texto = celda_fecha.inner_text().strip()
                    # Si la celda contiene el número de tu día (04)
                    if dia_actual in texto:
                        filas_de_hoy.append(fila)

            if filas_de_hoy:
                # Tomamos la primera y la última fila del grupo para delimitar el área
                primera_fila = filas_de_hoy[0]
                ultima_fila = filas_de_hoy[-1]

                box_inicio = primera_fila.bounding_box()
                box_fin = ultima_fila.bounding_box()

                if box_inicio and box_fin:
                    os.makedirs(folder, exist_ok=True)
                    
                    area_recorte = {
                        "x": box_inicio["x"],
                        "y": box_inicio["y"],
                        "width": box_inicio["width"],
                        "height": (box_fin["y"] + box_fin["height"]) - box_inicio["y"]
                    }

                    # Sacar el screenshot del área específica
                    page.screenshot(path=output, clip=area_recorte)
                    print(f"✅ EXITO: {seccion} guardada en {output}")
            else:
                print(f"⚠️ No se encontraron filas para el día {dia_actual} en {seccion}.")

        except Exception as e:
            print(f"❌ Error fatal en {seccion}: {e}")
        
        finally:
            browser.close()

if __name__ == "__main__":
    # Ajuste de rutas para que el Main (en la raíz) y este script (en Utilities) coincidan
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    OUTPUT_FOLDER = os.path.normpath(os.path.join(BASE_DIR, "..", "screenshots"))

    # URLs directas a Avionio
    sacaScreenshot("https://www.avionio.com/es/airport/bhi/departures?page=-1", "salidas", OUTPUT_FOLDER)
    sacaScreenshot("https://www.avionio.com/es/airport/bhi/arrivals?page=-1", "llegadas", OUTPUT_FOLDER)