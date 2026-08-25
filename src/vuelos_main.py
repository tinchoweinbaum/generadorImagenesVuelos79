import schedule
import time

from config import getPath, lee_config
from imgMerger import generaPlacas_aire
from screenshot import sacaScreenshots


def generaPlaca(cfg):
    print("")
    print("Hora actual: " + time.strftime("%H:%M:%S"))
    print("Generando placas...")
    print(f"Salida: {cfg.dir}")
    print(f"URL: {cfg.url}")

    dirPlacaArribos = getPath("placas/placaArribos.png")
    dirPlacaPartidas = getPath("placas/placaPartidas.png")
    dirPlacaArribosVacio = getPath("placas/placaArribosSinVuelos.png")
    dirPlacaPartidasVacio = getPath("placas/placaPartidasSinVuelos.png")

    try:
        cap_arribos, cap_partidas = sacaScreenshots(cfg)
        time.sleep(2)
        generaPlacas_aire(
            cfg.dir,
            cap_arribos,
            cap_partidas,
            dirPlacaArribos,
            dirPlacaPartidas,
            dirPlacaArribosVacio,
            dirPlacaPartidasVacio,
        )
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    cfg = lee_config()
    generaPlaca(cfg)
    schedule.every().hour.at(":06").do(lambda: generaPlaca(cfg))

    while True:
        schedule.run_pending()
        time.sleep(1)
