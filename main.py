import os
import subprocess
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.togglebutton import ToggleButton
from kivy.clock import Clock
from functools import partial
import sys

LOG_DIR = "logs"
PROCESS_REFERENCES = {}  # Per tenere traccia dei processi

class MainLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', padding=10, spacing=10, **kwargs)

        self.headless_toggle = ToggleButton(text="Modalità Headless: OFF", size_hint_y=None, height=40)
        self.headless_toggle.bind(on_press=self.toggle_headless)
        self.add_widget(self.headless_toggle)

        # Pulsanti Start/Stop
        self.add_widget(self.make_scraping_buttons("Progetti Torino", 1))
        self.add_widget(self.make_scraping_buttons("Consulenti", 2))

        # Esporta
        self.export_torino = Button(text="Esporta Progetti Torino", size_hint_y=None, height=40)
        self.export_torino.bind(on_press=partial(self.export_excel, "Per progetti Torino"))
        self.add_widget(self.export_torino)

        self.export_consulenti = Button(text="Esporta Consulenti", size_hint_y=None, height=40)
        self.export_consulenti.bind(on_press=partial(self.export_excel, "Per consulenza"))
        self.add_widget(self.export_consulenti)

        # TextArea per log
        self.log_area = TextInput(readonly=True, size_hint_y=1, font_size=12)
        self.add_widget(self.log_area)

        # Aggiorna log ogni 5 secondi
        Clock.schedule_interval(self.update_logs, 5)

    def make_scraping_buttons(self, label, list_id):
        layout = BoxLayout(size_hint_y=None, height=40)
        start_btn = Button(text=f"Start {label}")
        stop_btn = Button(text=f"Stop {label}")

        start_btn.bind(on_press=partial(self.run_scraping, list_id, label))
        stop_btn.bind(on_press=partial(self.stop_scraping, list_id, label))

        layout.add_widget(start_btn)
        layout.add_widget(stop_btn)
        return layout

    def toggle_headless(self, instance):
        if instance.state == 'down':
            instance.text = "Modalità Headless: ON"
        else:
            instance.text = "Modalità Headless: OFF"

    def get_python_cmd(self):
        if getattr(sys, 'frozen', False):
            # Se siamo nel .exe, usiamo il python del venv locale (env/Scripts/python.exe)
            return os.path.join(os.getcwd(), 'env', 'Scripts', 'python.exe')
        return sys.executable

    def run_scraping(self, list_id, label, instance):
        exe_dir = os.path.dirname(sys.executable) if getattr(sys, 'frozen', False) else os.path.abspath(".")
        script_path = os.path.join(exe_dir, "backend", "app.py")
        if not os.path.exists(script_path):
            print(f"❌ File non trovato: {script_path}")
            return


        python_cmd = self.get_python_cmd()
        cmd = [python_cmd, script_path, f"--id={list_id}"]
        if self.headless_toggle.state == 'down':
            cmd.append("--headless")

        process = subprocess.Popen(cmd)
        PROCESS_REFERENCES[list_id] = process
        print(f"🟢 Avviato scraping {label}")

    def stop_scraping(self, list_id, label, instance):
        proc = PROCESS_REFERENCES.get(list_id)
        if proc and proc.poll() is None:
            proc.terminate()
            print(f"🔴 Arrestato scraping {label}")

    def update_logs(self, *args):
        try:
            logs = [os.path.join(LOG_DIR, f) for f in os.listdir(LOG_DIR) if f.endswith(".log")]
            latest_log = max(logs, key=os.path.getctime)
            with open(latest_log, encoding="utf-8") as f:
                lines = f.readlines()[-100:]
            self.log_area.text = ''.join(lines)
        except Exception as e:
            self.log_area.text = f"Errore lettura log: {e}"

    def export_excel(self, list_name, instance):
        try:
            import pandas as pd
            import sqlite3

            conn = sqlite3.connect("linkedin_data.db")
            query_sql = f"""
                SELECT
                    c.name AS "Nome",
                    c.lastname AS "Cognome",
                    c.role AS "Ruolo",
                    c.email AS "Email",
                    a.name AS "Azienda",
                    a.industry AS "Tipo industria",
                    a.revenue AS "Fatturato",
                    a.country AS "Paese",
                    a.city AS "Città",
                    c.created_at AS "Data creazione"
                FROM contacts AS c
                LEFT JOIN companies AS a ON c.company_id = a.id
                WHERE a.type_company = '{list_name}';
            """
            df = pd.read_sql_query(query_sql, conn)

            export_name = f"export_{list_name.replace(' ', '_').lower()}.xlsx"
            df.to_excel(export_name, index=False)
            print(f"✅ Esportato: {export_name}")
        except Exception as e:
            print(f"❌ Errore esportazione: {e}")

class ScrapingApp(App):
    def build(self):
        return MainLayout()

if __name__ == '__main__':
    ScrapingApp().run()