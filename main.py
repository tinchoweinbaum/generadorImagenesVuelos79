from playwright.sync_api import sync_playwright

def sacaScreen(url, claseDiv, archivo="screenshot.png"):  #La función pide 3 parámetros: url, nombre de la clase a capturar, y nombre del archivo a crear.
    selector = rf".{claseDiv}"

    with sync_playwright() as p:
        navegador = p.chromium.launch(headless=True)#Abre una instancia de chromium en headless y abre una página en este navegador
        pagina = navegador.new_page()

        pagina.goto(url, wait_until="load") #Va a la ulr y espera a que cargue
        pagina.wait_for_load_state("networkidle")

        elemento = pagina.query_selector(selector) #Selecciona el elemento

        if elemento: 
            elemento.screenshot(path=archivo) #Si existe le saca screenshot, si no, tira error.
            print(f"Se guardó el archivo como: {archivo}")
        else:
            print(f"No se encontró la clase {selector}")

        navegador.close()


sacaScreen("https://www.aeropuertosargentina.com/es/vuelos?movtp=partidas&idarpt=Mar%20del%20Plata%2C%20MDQ&fecha=05-11-2025",r"flex.flex-col.tablet\:w-\[41\.5rem\].tablet\:mx-auto.xl\:w-full.mt-6.xl\:mt-8", "vuelos.png")