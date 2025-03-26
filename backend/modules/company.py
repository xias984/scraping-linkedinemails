from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from src.logger import Log
from modules.scraper import Scraper
from modules.contacts import Contacts

class Company:
    def __init__(self, driver, name, list_name):
        self.driver = driver
        self.name = name
        self.list_name = list_name
        self.scraper = Scraper(driver)
        self.contacts = Contacts(driver)
        self.list_url = driver.current_url

    def get_filters(self):
        filters = {
            "Per progetti Torino": {
                "title_keywords": ["manager", "head of", "ceo", "cio", "chief", "it manager", "responsabile", "founder"],
                "exclude_keywords": {"project", "hr", "marketing", "finance", "financial", "account", "fleet"},
                "country": ["Italy"]
            },
            "Per consulenza": {
                "title_keywords": ["Head of", "Chief", "COO", "CEO", "Manager"],
                "exclude_keywords": {"Project", "service", "marketing", "finance", "financial", "security"},
                "country": ["Italy"]
            }
        }
        return filters.get(self.list_name, {})

    def start_prospecting(self, company_data):
        try:
            start_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//a[contains(@class, 'chakra-button') and contains(text(), 'Start prospecting')]"))
            )
            start_button.click()
            time.sleep(3)
            
            filters = self.get_filters()
            self.contacts.filter_data(
                title_keywords=filters.get("title_keywords"),
                exclude_keywords=filters.get("exclude_keywords"),
                country=filters.get("country")
            )

            self.contacts.process_contacts(self.list_name, company_data)
        except Exception as e:
            Log.error(f"❌ Errore durante il 'Start prospecting' per {self.name}.")

    def go_to_list_company(self):
        try:
            self.driver.get(self.list_url)

            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )

            list_element = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, f"//span[text()='{self.list_name}']"))
            )

            self.driver.execute_script("arguments[0].scrollIntoView();", list_element)
            time.sleep(1)
            list_element.click()
            time.sleep(2)

        except Exception as e:
            Log.error(f"❌ Errore durante il ritorno alla lista '{self.list_name}'.")
    
    def fetch_company_data(self):
        try:
            company_element = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[div[text()='Company']]"))
            )
            company_element.click()
            time.sleep(3)

            company_data = Scraper(self.driver)
            return company_data.get_company_data()
        except Exception as e:
            Log.error(f"❌ Tab company non trovata su {self.name}.")