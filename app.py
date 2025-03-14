import multiprocessing
from selenium import webdriver
from src.auth import KoalaAuth
from src.logger import Log
from modules.list_interaction import KoalaListProcessor

def configure_webdriver():
    """Configura e restituisce una nuova istanza di WebDriver."""
    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    return webdriver.Chrome(options=options)

def process_list(list_name):
    """Esegue l'intero processo per una lista specifica."""
    driver = configure_webdriver()

    try:
        auth = KoalaAuth(driver)
        auth.login()

        processor = KoalaListProcessor(driver, list_name)
        processor.open_list()
        processor.process_companies()

        Log.info(f"🟢 Processo completato con successo per '{list_name}'.")

    except Exception as error:
        Log.error(f"❌ Errore critico per '{list_name}': {error}")

    finally:
        driver.quit()
        Log.info(f"🚪 WebDriver chiuso per '{list_name}'.")

if __name__ == "__main__":
    process_torino = multiprocessing.Process(target=process_list, args=("Per progetti Torino",))
    process_consulenza = multiprocessing.Process(target=process_list, args=("Per consulenza",))

    process_torino.start()
    process_consulenza.start()

    process_torino.join()
    process_consulenza.join()

    Log.info("✅ Entrambi i processi sono completati!")
