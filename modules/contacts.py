from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from src.logger import Log

class Contacts:
    def __init__(self, driver):
        self.driver = driver

    def _insert_keywords(self, label_text, placeholder_text, keywords):
        try:
            if keywords:
                section = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, f"//p[text()='{label_text}']"))
                )
                section.click()
                time.sleep(1)

                input_field = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, f"//input[@placeholder='{placeholder_text}']"))
                )
                self.driver.execute_script("arguments[0].focus();", input_field)
                self.driver.execute_script("arguments[0].click();", input_field)
                time.sleep(1)

                for keyword in keywords:
                    input_field.send_keys(keyword + "\n")
                    time.sleep(1)

        except Exception as e:
            Log.error(f"❌ Errore durante l'inserimento di '{label_text}': {e}")

    def filter_data(self, title_keywords=None, exclude_keywords=None, country="Italy"):
        try:
            title_keywords_section = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//p[text()='Title Keywords']"))
            )
            title_keywords_section.click()

            popup = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//section[contains(@id, 'popover-content')]"))
            )

            time.sleep(2)

            self._insert_keywords("Is any of…", "Include keywords…", title_keywords)
            self._insert_keywords("Is not any of…", "Exclude keywords…", exclude_keywords)

            apply_filter_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Apply Filters')]"))
            )
            self.driver.execute_script("arguments[0].click();", apply_filter_button)
            Log.info("✅ Filtri applicati con successo.")
            time.sleep(3)

        except Exception as e:
            Log.error(f"❌ Errore durante il filtraggio dei contatti: {e}")
