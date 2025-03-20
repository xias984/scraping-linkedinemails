from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from src.logger import Log
from modules.company import Company

class KoalaListProcessor:
    def __init__(self, driver, list_name):
        self.driver = driver
        self.list_name = list_name

    def open_list(self):
        try:
            list_element = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, f"//span[text()='{self.list_name}']"))
            )
            list_element.click()
        except Exception as e:
            Log.error(f"❌ Errore nell'apertura della lista '{self.list_name}': {e}")

    def process_companies(self):
        try:
            while True:
                companies = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, "table tbody tr a.koala-1kg28i4"))
                )

                for index in range(len(companies)):  
                    try:
                        companies = WebDriverWait(self.driver, 10).until(
                            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "table tbody tr a.koala-1kg28i4"))
                        )

                        company_element = companies[index]
                        company_name = company_element.get_attribute("title")

                        self.driver.execute_script("arguments[0].click();", company_element)
                        time.sleep(3)

                        company = Company(self.driver, company_name, self.list_name)
                        company_data = company.fetch_company_data()
                        company.start_prospecting()

                        #input("Premi INVIO per continuare...")
                        company.go_to_list_company()

                        WebDriverWait(self.driver, 10).until(
                            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "table tbody tr a.koala-1kg28i4"))
                        )

                    except Exception as e:
                        Log.error(f"⚠ Errore con l'azienda {company_name}: {e}")

                if not self.next_page():
                    break

        except Exception as e:
            Log.error(f"❌ Errore durante il processo delle aziende: {e}")

    def next_page(self):
        try:
            next_buttons = self.driver.find_elements(By.XPATH, "//a[@rel='next']")
            if next_buttons:
                next_button = next_buttons[0]
                if next_button.is_displayed() and next_button.is_enabled():
                    Log.info("➡ Passando alla pagina successiva...")
                    next_button.click()
                    time.sleep(3)
                    return True
                else:
                    Log.warning("✅ Nessuna altra pagina disponibile.")
                    return False
            else:
                Log.info("✅ Fine della lista.")
                return False
        except:
            Log.error("❌ Errore durante la gestione della paginazione.")
            return False
