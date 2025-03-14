from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from src.logger import Log
from config.settings import Settings  # Importiamo la classe Settings

class KoalaAuth:
    def __init__(self, driver):
        self.driver = driver
        self.email = Settings.EMAIL
        self.password = Settings.PASSWORD

    def login(self):
        self.driver.get(Settings.LOGIN_URL)  # Usa l'URL da Settings

        try:
            # Attendi che il campo email sia visibile e inserisci l'email
            email_field = WebDriverWait(self.driver, Settings.DEFAULT_TIMEOUT).until(
                EC.presence_of_element_located((By.ID, 'email'))
            )
            email_field.send_keys(self.email)

            # Clicca su "Continue with email"
            continue_button = WebDriverWait(self.driver, Settings.DEFAULT_TIMEOUT).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))
            )
            continue_button.click()

            # Clicca su "Log in with password"
            continue_login_psw = WebDriverWait(self.driver, Settings.DEFAULT_TIMEOUT).until(
                EC.element_to_be_clickable((By.XPATH, "//button[text()='Log in with password']"))
            )
            continue_login_psw.click()

            # Attendi il campo password e inserisci la password
            password_field = WebDriverWait(self.driver, Settings.DEFAULT_TIMEOUT).until(
                EC.presence_of_element_located((By.ID, 'password'))
            )
            password_field.send_keys(self.password)

            # Clicca il bottone di login
            login_button = WebDriverWait(self.driver, Settings.DEFAULT_TIMEOUT).until(
                EC.element_to_be_clickable((By.XPATH, "//button[text()='Log in with password']"))
            )
            login_button.click()

            Log.info("✅ Login effettuato con successo!")

        except Exception as e:
            Log.error(f"❌ Errore durante il login: {e}")
