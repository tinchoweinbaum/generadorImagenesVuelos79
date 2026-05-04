import os
import sys
from datetime import datetime
from playwright.sync_api import sync_playwright

# Configuración de rutas
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, "..", "screenshots")
os.makedirs(OUTPUT_DIR, exist_ok=True)

def capturar_seccion_vuelos(page, tipo_vuelo, hoy):
    """
    Localiza el iframe, filtra los vuelos de hoy y captura solo esa área.
    """
    print(f"--- Procesando {tipo_vuelo.upper()} ---")
    
    # 1. Localizar el iframe específico
    iframe_selector = f"iframe[src*='{tipo_vuelo}']"
    iframe_element = page.wait_for_selector(iframe_selector, timeout=20000)
    frame = iframe_element.content_frame()
    
    if not frame:
        print(f"No se pudo acceder al contenido del iframe: {tipo_vuelo}")
        return

    # 2. Asegurar que la tabla esté cargada y scrollear para activar Lazy Load
    # Avionio renderiza filas a medida que se hace scroll.
    tabla = frame.locator("table")
    tabla.wait_for(state="visible", timeout=10000)
    
    # Scroll al fondo y volver para asegurar que todos los TR existan
    frame.evaluate("window.scrollTo(0, document.body.scrollHeight)")
    page.wait_for_timeout(1500)
    
    # 3. Filtrar las filas que corresponden a 'hoy'
    # Usamos el selector 'has-text' que es el más flexible para fechas
    filas_hoy = frame.locator("tr").filter(has_text=hoy)
    
    if filas_hoy.count() == 0:
        print(f"No se encontraron vuelos para el día {hoy}.")
        return

    print(f"Vuelos detectados: {filas_hoy.count()}")

    # 4. CAPTURA INTELIGENTE
    # En lugar de clip manual, ocultamos lo que NO es de hoy y capturamos la tabla
    # O mejor aún: definimos el clip basado en el primer y último elemento de hoy
    
    primera_fila = filas_hoy.first
    ultima_fila = filas_hoy.last
    
    primera_fila.scroll_into_view_if_needed()
    ultima_fila.scroll_into_view_if_needed()
    
    # Pequeña pausa para que el navegador recalcule posiciones
    page.wait_for_timeout(500)

    box_top = primera_fila.bounding_box()
    box_bottom = ultima_fila.bounding_box()
    frame_box = iframe_element.bounding_box()

    # --- DEBUG ---
    if not box_top: print(f"DEBUG: box_top es None en {tipo_vuelo}")
    if not box_bottom: print(f"DEBUG: box_bottom es None en {tipo_vuelo}")
    if not frame_box: print(f"DEBUG: frame_box es None en {tipo_vuelo}")
    # --------------

    if box_top and box_bottom and frame_box:
        # Tu lógica de recorte...
        recorte = {
            "x": frame_box["x"] + box_top["x"],
            "y": frame_box["y"] + box_top["y"],
            "width": frame_box["width"], # Usa el ancho del iframe para mayor seguridad
            "height": (box_bottom["y"] + box_bottom["height"]) - box_top["y"]
        }
        
        # Aseguramos que la carpeta exista justo antes
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        path_final = os.path.join(OUTPUT_DIR, f"vuelos{tipo_vuelo.capitalize()}.png")
        
        page.screenshot(path=path_final, clip=recorte)
        print(f"Éxito: vuelos{tipo_vuelo.capitalize()}.png generado.")
    else:
        # PLAN B: Si los bounding boxes fallan, saca la foto al iframe completo 
        # para no quedarte con las manos vacías
        print(f"Advertencia: Fallaron los boxes de {tipo_vuelo}. Capturando iframe completo...")
        path_emergencia = os.path.join(OUTPUT_DIR, f"vuelos{tipo_vuelo.capitalize()}.png")
        iframe_element.screenshot(path=path_emergencia)

def ejecutar(url):
    with sync_playwright() as p:
        # Lanzamos el navegador
        browser = p.chromium.launch(headless=False)
        # Importante: un viewport grande evita que los elementos se encimen
        context = browser.new_context(viewport={'width': 1280, 'height': 2000})
        page = context.new_page()

        try:
            print(f"Accediendo a: {url}")
            page.goto(url, wait_until="networkidle")
            
            hoy = datetime.now().strftime("%d")
            
            # Procesar Arribos y Partidas
            capturar_seccion_vuelos(page, "arrivals", hoy)
            capturar_seccion_vuelos(page, "departures", hoy)

        except Exception as e:
            print(f"Error en el proceso: {e}")
        finally:
            browser.close()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python screenshot.py <URL>")
        sys.exit(1)
    
    ejecutar(sys.argv[1])