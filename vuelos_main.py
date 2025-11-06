#Este programa llama a los 10 minutos de cada hora al programa que saca el screenshto

import subprocess
import schedule
import time


def llamaScreenshot():
    subprocess.run(["python","Utilities/screenshot.py"])

schedule.every().hour.at(":10").do(llamaScreenshot)

while True:
    schedule.run_pending()
    time.sleep(1)
