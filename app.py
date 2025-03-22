import multiprocessing
from selenium import webdriver
from src.auth import KoalaAuth
from src.logger import Log
from modules.list_interaction import KoalaListProcessor
import argparse

def configure_webdriver(headless=False):
    """Configura e restituisce una nuova istanza di WebDriver."""
    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument("--user-data-dir=C:/Users/CostarelliD/chrome-koala-profile")


    if headless:
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        options.add_argument('--window-size=1920x1080')
    
    return webdriver.Chrome(options=options)

def process_list(list_name, headless):
    """Esegue l'intero processo per una lista specifica."""
    driver = configure_webdriver(headless)

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
    '''process_torino = multiprocessing.Process(target=process_list, args=("Per progetti Torino",))
    process_consulenza = multiprocessing.Process(target=process_list, args=("Per consulenza",))

    process_torino.start()
    process_consulenza.start()

    process_torino.join()
    process_consulenza.join()

    '''
    from src.database import DatabaseManager

    db = DatabaseManager()
    db.create_tables()

    parser = argparse.ArgumentParser(description="Processa le liste di Koala.")
    parser.add_argument('--id', required=True, help="1 = Per progetti Torino, 2 = Per consulenti")
    parser.add_argument('--headless', action='store_true', help="Esegui il processo in modalità headless")
    args = parser.parse_args()

    lista_map = {
        "1": "Per progetti Torino",
        "2": "Per consulenza"
    }

    list_name = lista_map.get(args.id)
    if not list_name:
        print("Valore non valido per --id. Usa 1 o 2.")
        exit(1)

    process_list(list_name, headless=args.headless)
    Log.info(f"✅ Il processo {list_name} è stato completato!")