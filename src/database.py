import sqlite3
from src.logger import Log
from config.settings import Settings  # Importiamo la classe Settings per la configurazione

class DatabaseManager:
    def __init__(self):
        self.db_name = Settings.DB_NAME
        self.conn = None

    def connect(self):
        try:
            self.conn = sqlite3.connect(self.db_name)
            Log.info(f"✅ Connessione al database '{self.db_name}' aperta con successo.")
        except Exception as e:
            Log.error(f"❌ Errore durante la connessione al database: {e}")

    def close(self):
        if self.conn:
            self.conn.close()
            Log.info("✅ Connessione al database chiusa con successo.")

    def create_tables(self):
        try:
            self.connect()
            cursor = self.conn.cursor()

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS companies (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    url TEXT UNIQUE,
                    revenue TEXT,
                    industry TEXT,
                    city TEXT,
                    country TEXT
                )
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS contacts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    company_id INTEGER NOT NULL,
                    name TEXT NOT NULL,
                    lastname TEXT NOT NULL,
                    role TEXT NOT NULL,
                    email TEXT NOT NULL UNIQUE,
                    FOREIGN KEY (company_id) REFERENCES companies(id)
                )
            """)

            self.conn.commit()
            Log.info("✅ Database e tabelle create con successo.")

        except Exception as e:
            Log.error(f"❌ Errore durante la creazione delle tabelle: {e}")

        finally:
            self.close()

    def insert_company(self, name, url, revenue, industry, city, country):
        try:
            self.connect()
            cursor = self.conn.cursor()

            cursor.execute("""
                INSERT OR IGNORE INTO companies (name, url, revenue, industry, city, country)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (name, url, revenue, industry, city, country))

            self.conn.commit()
            Log.info(f"✅ Azienda '{name}' inserita con successo.")

        except Exception as e:
            Log.error(f"❌ Errore durante l'inserimento dell'azienda '{name}': {e}")

        finally:
            self.close()

    def insert_contact(self, company_id, name, lastname, role, email):
        try:
            self.connect()
            cursor = self.conn.cursor()

            cursor.execute("""
                INSERT OR IGNORE INTO contacts (company_id, name, lastname, role, email)
                VALUES (?, ?, ?, ?, ?)
            """, (company_id, name, lastname, role, email))

            self.conn.commit()
            Log.info(f"✅ Contatto '{name} {lastname}' inserito con successo.")

        except Exception as e:
            Log.error(f"❌ Errore durante l'inserimento del contatto '{name} {lastname}': {e}")

        finally:
            self.close()
