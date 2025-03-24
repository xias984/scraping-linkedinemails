from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import time
from src.logger import Log
from src.database import DatabaseManager as DB
from modules.scraper import Scraper

class Contacts:
    def __init__(self, driver):
        self.driver = driver
        self.db = DB()
        self.scraper = Scraper(driver)

    def _open_filter_section(self, label_popup):
        try:
            filter_button = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, f"//button[.//p[text()='{label_popup}']]"))
            )
            
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", filter_button)
            time.sleep(1)
            
            WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable(filter_button))
            
            try:
                filter_button.click()
            except:
                self.driver.execute_script("arguments[0].click();", filter_button)

            return WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//section[contains(@id, 'popover-content')]"))
            )
        except Exception as e:
            Log.error(f"❌ Errore durante l'apertura della sezione '{label_popup}': {e}")
            return None


    def _insert_keywords(self, label_popup, checklabel_text, placeholder_text, keywords):
        """Inserisce parole chiave nel filtro specificato."""
        if not keywords:
            return

        popup = self._open_filter_section(label_popup)
        if not popup:
            return

        try:
            if checklabel_text == "Is not any of…":
                toggle_exclude_button = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//p[text()='Is not any of…']"))
                )
                self.driver.execute_script("arguments[0].click();", toggle_exclude_button)
                time.sleep(1)

            input_field = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, f"//p[text()='{checklabel_text}']/following::input[@placeholder='{placeholder_text}']"))
            )
            self.driver.execute_script("arguments[0].focus();", input_field)
            self.driver.execute_script("arguments[0].click();", input_field)
            time.sleep(1)

            for keyword in keywords:
                input_field.send_keys(keyword + "\n")
                time.sleep(1)

            self._apply_filters()
        except Exception as e:
            Log.error(f"❌ Errore durante l'inserimento di '{label_popup}': {e}")

    def _select_country(self, country_list):
        """Seleziona i paesi desiderati digitando direttamente nel campo di ricerca del popup Country."""
        popup = self._open_filter_section("Country")
        if not popup:
            Log.error("❌ Il popup 'Country' non si è aperto correttamente.")
            return

        # XPath per l'input di ricerca
        xpath = ".//input[contains(@class, 'koala-7e4x79')]"

        try:
            # Attendere che l'input sia cliccabile
            search_input = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, xpath))
            )
            
            if search_input.get_attribute("disabled") or search_input.get_attribute("readonly"):
                Log.error("❌ L'input è disabilitato o in sola lettura.")
                return

            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", search_input)
            time.sleep(1)
            self.driver.execute_script("arguments[0].focus();", search_input)

            try:
                search_input.click()
            except Exception:
                Log.warning("⚠️ Click diretto fallito, proviamo con JavaScript...")
                self.driver.execute_script("arguments[0].click();", search_input)

            for country in country_list:
                try:
                    search_input.clear()
                    search_input.send_keys(country)
                    time.sleep(2)

                    self._select_all_checkboxes(country)

                except Exception as e:
                    Log.error(f"❌ Errore durante la selezione del paese '{country}': {e}")

            self._apply_filters()

        except Exception as e:
            Log.error("❌ Errore durante la ricerca dell'input.")
            exit()
        
    def _select_all_checkboxes(self, label):
        xpath = f"//input[@class='chakra-checkbox__input' and ancestor::label[contains(@class, 'chakra-checkbox')]//p[contains(text(), '{label}')]]"
    
        try:
            time.sleep(1)
            checkboxes = WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located((By.XPATH, xpath))
            )

            if not checkboxes:
                Log.warning("Nessun checkbox trovato.")
                return

            counter = 0
            for checkbox in checkboxes:
                try:
                    self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", checkbox)
                    time.sleep(1)
                    self.driver.execute_script("arguments[0].click();", checkbox)
                except Exception as e:
                    Log.error(f"Errore nella selezione del checkbox: {e}")
            
            return counter
        
        except Exception as e:
            Log.error(f"Errore nel recupero dei checkbox: {e}")

    def _apply_filters(self):
        xpath = f".//button[contains(text(), 'Apply Filters')]"
        
        try:
            apply_filter_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, xpath))
            )
            self.driver.execute_script("arguments[0].click();", apply_filter_button)
        except Exception as e:
            Log.error(f"❌ Errore durante l'applicazione dei filtri: {e}")

    def filter_data(self, title_keywords=None, exclude_keywords=None, country=["Italy"]):
        """Applica tutti i filtri ai contatti."""
        try:
            self._select_country(country)
            self._insert_keywords("Title Keywords", "Is any of…", "Include keywords…", title_keywords)
            self._insert_keywords("Title Keywords", "Is not any of…", "Exclude keywords…", exclude_keywords)

        except Exception as e:
            Log.error(f"❌ Errore durante il filtraggio dei contatti: {e}")

    def enrich_email(self, index):
        """Effettua l'enrichment per il contatto all'indice specificato e restituisce l'email trovata o None."""
        try:
            find_email_buttons = self.driver.find_elements(By.XPATH, "//button[@aria-label='Find email address']")
            Log.debug(f"🔎 Trovati {len(find_email_buttons)} pulsanti 'Find email address'.")

            if index >= len(find_email_buttons):
                Log.warning(f"⚠️ Nessun pulsante 'Find email address' all'indice {index}.")
                return None

            button = find_email_buttons[index]
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", button)
            time.sleep(1)
            self.driver.execute_script("arguments[0].click();", button)
            Log.info(f"✅ Cliccato su 'Find email address' per contatto [{index}].")

            # Attendi stato "Enriching..."
            try:
                WebDriverWait(self.driver, 60).until(
                    EC.presence_of_element_located(
                        (By.XPATH, "//button[@aria-label='Find email address' and contains(text(), 'Enriching')]")
                    )
                )
                Log.info(f"⏳ Enrichment in corso per contatto [{index}]...")

            except:
                Log.warning(f"⚠️ Timeout enrichment per contatto [{index}], continuo comunque...")

            # Controlla se compare una email
            try:
                email_element = WebDriverWait(self.driver, 60).until(
                    EC.presence_of_element_located(
                        (By.XPATH, "//span[contains(@class, 'chakra-text') and contains(text(), '@')]")
                    )
                )
                email = email_element.text.strip()
                Log.info(f"📩 Email trovata per contatto [{index}]: {email}")
                return email

            except:
                # Controllo alternativo: "No email found"
                no_email = self.driver.find_elements(By.XPATH, "//span[contains(text(), 'No email found')]")
                if no_email:
                    Log.warning(f"🚫 Nessuna email trovata per contatto [{index}].")
                else:
                    Log.error(f"❌ Errore sconosciuto durante l'enrichment del contatto [{index}].")
                return None

        except Exception as e:
            Log.error(f"❌ Errore nell'enrichment del contatto [{index}].")
            return None


    def next_page(self):
        """Cambia pagina se il pulsante 'Next' non è disabilitato."""
        try:
            next_buttons = self.driver.find_elements(By.XPATH, "//button[normalize-space(text())='Next' and not(@disabled)]")

            if next_buttons:
                next_button = next_buttons[0]
                if next_button.is_displayed() and next_button.is_enabled():
                    self.driver.execute_script("arguments[0].click();", next_button)
                    time.sleep(3)
                    return True
                else:
                    return False
            else:
                return False

        except Exception as e:
            Log.error(f"❌ Errore durante il cambio pagina nei contatti.")
            return False
        
    def process_contacts(self, list_name, company_data):
        all_contacts = []
        email_found = False
        pagina = 1

        while True:
            try:
                contact_list = self.scraper.get_contact_data()

                for index, contact in enumerate(contact_list):
                    email = contact.get('email', '').strip()
                    Log.debug(f"📧 Contatto [{index}] email: {email}")

                    if email is None or email == '':
                        Log.debug(f"📧 Contatto senza email, arricchimento...")
                        enriched_email = self.enrich_email(index)
                        if enriched_email:
                            contact['email'] = enriched_email
                            email_found = True 
                            all_contacts.append(contact)
                        else:
                            Log.warning(f"⛔ Contatto [{index}] ignorato: nessuna email trovata.")
                    else:
                        email_found = True
                        all_contacts.append(contact)
                        Log.info(f"✅ Contatto [{index}] con email già presente.")

                if not self.next_page():
                    break
                else:
                    pagina += 1

            except Exception as e:
                Log.error(f"❌ Errore durante il processamento dei contatti: {e}")
                break

        try:
            company_id = self.db.insert_company(
                company_data['name'],
                company_data['url'],
                company_data['revenue'],
                company_data['industry'],
                company_data['city'],
                company_data['country'],
                email_found,
                list_name
            )

            if not company_id:
                Log.error("❌ Errore durante l'inserimento dell'azienda.")
                return

            for contact in all_contacts:
                if contact.get('email') and "@" in contact['email']:
                    self.db.insert_contact(
                        company_id,
                        contact['name'],
                        contact['lastname'],
                        contact['role'],
                        contact['email']
                    )

        except Exception as e:
            Log.error(f"❌ Errore nel salvataggio dei dati: {e}")
