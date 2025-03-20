from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from src.logger import Log

class Scraper:
    def __init__(self, driver):
        self.driver = driver

    def get_company_data(self):
        try:
            # Attendere il caricamento della pagina
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )

            # Estrarre il codice HTML della pagina
            page_source = self.driver.page_source
            soup = BeautifulSoup(page_source, "html.parser")

            # Estrazione dati azienda
            company_name = soup.find("h2").text.strip() if soup.find("h2") else "N/A"
            company_url = soup.find("a", attrs={"target": "_blank"})["href"] if soup.find("a", attrs={"target": "_blank"}) else "N/A"

            revenue_element = soup.find("div", text="Revenue")
            revenue = revenue_element.find_next_sibling("div").text.strip() if revenue_element else "N/A"

            location_element = soup.find("div", text="Location")
            location = location_element.find_next_sibling("div").text.strip() if location_element else "N/A"

            location_parts = location.split(", ")
            if len (location_parts) >= 2:
                city, country = location_parts[0], location_parts[1]
            else:
                city, country = location, "N/A"

            industry_label = soup.find("div", text="Industry")
            industry_text = industry_label.find_next("div").text.strip() if industry_label else "N/A"
            industry_text = industry_text.replace("Copy to clipboard", "").strip()

            company_data = {
                "name": company_name,
                "url": company_url,
                "revenue": revenue,
                "industry": industry_text,
                "country": country,
                "city": city
            }

            return company_data

        except Exception as e:
            Log.error(f"❌ Errore durante l'estrazione dei dati aziendali: {e}")
            return None

    def get_contact_data(self):
        try:
            # Attendere il caricamento dei contatti
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )

            # Estrarre il codice HTML della pagina
            page_source = self.driver.page_source
            soup = BeautifulSoup(page_source, "html.parser")

            contacts = []
            contact_elements = soup.find_all("div", class_="contact-card")  # Sostituisci con la classe corretta

            for contact in contact_elements:
                name_element = contact.find("div", class_="contact-name")
                name = name_element.text.strip() if name_element else "N/A"

                lastname_element = contact.find("div", class_="contact-lastname")
                lastname = lastname_element.text.strip() if lastname_element else "N/A"

                role_element = contact.find("div", class_="contact-role")
                role = role_element.text.strip() if role_element else "N/A"

                email_element = contact.find("div", class_="contact-email")
                email = email_element.text.strip() if email_element else "N/A"

                contact_data = {
                    "name": name,
                    "lastname": lastname,
                    "role": role,
                    "email": email
                }
                contacts.append(contact_data)

            Log.info(f"✅ {len(contacts)} contatti estratti.")
            return contacts

        except Exception as e:
            Log.error(f"❌ Errore durante l'estrazione dei contatti: {e}")
            return []
