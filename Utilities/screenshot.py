import os
import sys
import time
from datetime import datetime
from playwright.sync_api import sync_playwright

def sacaScreenshot(url, seccion, folder):
    output = os.path.join(folder, "vuelosPartidas.png" if seccion == "salidas" else "vuelosArribos.png")
    dia_actual = datetime.now().strftime("%d")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        # Aumentamos el viewport para asegurar que las filas "existan" para el navegador
        context = browser.new_context(viewport={'width': 1280, 'height': 10000})
        page = context.new_page()
        
        try:
            print(f"--- Iniciando captura de {seccion} ---")
            page.goto(url, wait_until="domcontentloaded", timeout=60000)
            
            # 1. Scroll para "despertar" las filas de más abajo
            page.evaluate("window.scrollTo(0, document.body.scrollHeight / 2)")
            time.sleep(2)
            page.evaluate("window.scrollTo(0, 0)")
            time.sleep(3) 

            # 2. Solo buscar filas que NO sean tt-child (filtramos basura)
            filas = page.query_selector_all("tr.tt-row:not(.tt-child)")
            filas_de_hoy = []
            
            for fila in filas:
                celda_fecha = fila.query_selector("td.tt-d")
                if celda_fecha:
                    texto = celda_fecha.inner_text().strip()
                    # Verificamos si el día (04) está en el texto de la celda
                    if dia_actual in texto:
                        filas_de_hoy.append(fila)

            if filas_de_hoy:
                box_inicio = filas_de_hoy[0].bounding_box()
                box_fin = filas_de_hoy[-1].bounding_box()

                if box_inicio and box_fin:
                    os.makedirs(folder, exist_ok=True)
                    
                    area_recorte = {
                        "x": box_inicio["x"],
                        "y": box_inicio["y"],
                        "width": box_inicio["width"],
                        "height": (box_fin["y"] + box_fin["height"]) - box_inicio["y"]
                    }

                    page.screenshot(path=output, clip=area_recorte)
                    print(f"✅ EXITO: {seccion} guardada en {output}")
                else:
                    print(f"❌ Error: No se pudieron calcular las coordenadas de las filas en {seccion}.")
            else:
                print(f"⚠️ No se encontraron vuelos para el día {dia_actual} en {seccion}.")

        except Exception as e:
            print(f"❌ Error fatal en {seccion}: {e}")
        finally:
            browser.close()

if __name__ == "__main__":
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    OUTPUT_FOLDER = os.path.normpath(os.path.join(BASE_DIR, "..", "screenshots"))

    # IMPORTANTE: Asegurate de usar page=-1 para ver todo el listado
    sacaScreenshot("https://www.avionio.com/es/airport/bhi/departures?page=-1", "salidas", OUTPUT_FOLDER)
    sacaScreenshot("https://www.avionio.com/es/airport/bhi/arrivals?page=-1", "llegadas", OUTPUT_FOLDER)