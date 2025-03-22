from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from src.logger import Log
import re

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
                city, country = location_parts[0], location_parts[1] + (", " +location_parts[2] if len(location_parts) > 2 else "")
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
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )

            soup = BeautifulSoup(self.driver.page_source, "html.parser")

            contact_rows = soup.find_all("tr", attrs={"role": "group"})

            contacts = []

            for row in contact_rows:
                try:
                    first_name, last_name = self.extract_name(row)
                    role = self.extract_role(row)
                    email = self.extract_email(row)
                    #location = self.extract_location(row)

                    contact_data = {
                        "name": first_name,
                        "lastname": last_name,
                        "role": role,
                        "email": email
                    }

                    contacts.append(contact_data)

                except Exception as e:
                    Log.error(f"❌ Errore nell'estrazione di un contatto: {e}")

            return contacts

        except Exception as e:
            Log.error(f"❌ Errore generale durante l'estrazione dei dati dei contatti: {e}")
            return []
        
    def extract_name(self, row):
        try:
            span = row.find("span", string=re.compile(r"^[A-Z][a-z]+ [A-Z][a-z]+$"))
            full_name = span.text.strip() if span else "N/A"
            parts = full_name.split()
            return parts[0], " ".join(parts[1:]) if len(parts) > 1 else "N/A"
        except Exception as e:
            Log.error(f"❌ Errore nel parsing del nome: {e}")
            return "N/A", "N/A"

    def extract_role(self, row):
        try:
            keywords = re.compile(r"\b(Manager|Chief|Officer|Engineer|Developer|Head|Vice|President|Lead|Director|Founder|Data|Analyst|Intern|Consultant)\b", re.IGNORECASE)
            role_span = row.find("span", string=keywords)
            return role_span.text.strip() if role_span else "N/A"
        except Exception as e:
            Log.error(f"❌ Errore nel parsing del ruolo: {e}")
            return "N/A"

    def extract_email(self, row):
        try:
            span = row.find("span", string=re.compile(r"@"))
            return span.text.strip() if span else ""
        except Exception as e:
            Log.error(f"❌ Errore nel parsing dell'email: {e}")
            return ""

    '''
    def extract_location(self, row):
        try:
            p = row.find("p", string=re.compile(r"\w+,\s*\w+"))
            return p.text.strip() if p else "N/A"
        except Exception as e:
            Log.error(f"❌ Errore nel parsing della location: {e}")
            return "N/A"
    '''
