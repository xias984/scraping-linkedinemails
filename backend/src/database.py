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
        except Exception as e:
            Log.error(f"❌ Errore durante la connessione al database: {e}")

    def close(self):
        if self.conn:
            self.conn.close()

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
                    country TEXT,
                    is_active BOOLEAN NOT NULL,
                    type_company TEXT NOT NULL,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
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
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (company_id) REFERENCES companies(id)
                )
            """)

            self.conn.commit()
            Log.info("✅ Database e tabelle create con successo.")

        except Exception as e:
            Log.error(f"❌ Errore durante la creazione delle tabelle: {e}")

        finally:
            self.close()

    def insert_company(self, name, url, revenue, industry, city, country, email_found, type_company):
        try:
            self.connect()
            cursor = self.conn.cursor()
            cursor.execute("""
                INSERT INTO companies (name, url, revenue, industry, city, country, is_active, type_company)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (name, url, revenue, industry, city, country, email_found, type_company))
            self.conn.commit()

            company_id = cursor.lastrowid  # ✅ prende subito l'id sulla stessa connessione
            Log.info(f"✅ Azienda '{name}' inserita con successo (ID: {company_id}) in {type_company}.")
            return company_id

        except Exception as e:
            Log.error(f"❌ Errore durante l'inserimento dell'azienda '{name}' in {type_company}.")
            return None

        finally:
            self.close()

    def get_last_inserted_company_id(self):
        try:
            self.connect()
            cursor = self.conn.cursor()
            cursor.execute("SELECT last_insert_rowid()")
            company_id = cursor.fetchone()[0]
            return company_id
        except Exception as e:
            Log.error(f"❌ Errore nel recupero dell'ultimo ID azienda: {e}")
            return None
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
            Log.error(f"❌ Errore durante l'inserimento del contatto '{email}'.")

        finally:
            self.close()

    def company_exists(self, name):
        try:
            self.connect()
            cursor = self.conn.cursor()

            cursor.execute("SELECT id FROM companies WHERE name = ?", (name,))
            result = cursor.fetchone()
            return result is not None

        except Exception as e:
            Log.error(f"❌ Errore durante il controllo esistenza azienda '{name}': {e}")
            return False

        finally:
            self.close()
