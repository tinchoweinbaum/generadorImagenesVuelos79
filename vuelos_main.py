import subprocess
import schedule
import time


def llamaScreenshot():
    subprocess.run(["python","Utilities/screenshot.py"])

schedule.every().hour.at(":33").do(llamaScreenshot)

while True:
    schedule.run_pending()
    time.sleep(1)
