# Scraping LinkedIn Emails

## Descrizione
Questo progetto permette di automatizzare il processo di scraping di dati aziendali e contatti da Koala utilizzando **Selenium**, **BeautifulSoup** e **Docker**. Il progetto è strutturato per essere eseguito in un ambiente Docker con **MySQL** e **phpMyAdmin**.

## 📦 Installazione

### 1️⃣ Clona il repository
```sh
git clone https://github.com/costarelliengit/scraping-linkedinemails.git
cd scraping-linkedinemails
```

### 2️⃣ Configura l'ambiente
Crea un file `.env` nella root del progetto e aggiungi le variabili d'ambiente necessarie:

```ini
EMAIL_KOALA=example@example.com
PASSWORD_KOALA=password
BASE_URL=https://app.getkoala.com
DB_HOST=mysql
DB_USER=root
DB_PASSWORD=rootpassword
DB_NAME=scraping_db
```

### 3️⃣ Costruisci i container Docker
Assicurati di avere **Docker** e **Docker Compose** installati, poi esegui:
```sh
docker-compose up --build -d
```
Questo avvierà **l'applicazione**, il **database MySQL** e **phpMyAdmin**.

### 4️⃣ Controlla lo stato dei container
```sh
docker ps
```
Dovresti vedere i container avviati per l'applicazione, MySQL e phpMyAdmin.

## 🚀 Avviare l'applicazione manualmente
Se vuoi avviare manualmente lo script Python dentro il container, esegui:
```sh
docker exec -it scraping_app bash
python app.py
```

## 🔧 Debug e Logs
Per visualizzare i log dell'applicazione in esecuzione:
```sh
docker logs -f scraping_app
```
Per accedere a **phpMyAdmin**, apri il browser e vai su:
```
http://localhost:8080
```
Usa le credenziali definite nel file `.env` per accedere a MySQL.

## 🛑 Arrestare i container
Se vuoi fermare tutti i servizi:
```sh
docker-compose down
```

---
Se hai problemi o suggerimenti, apri una **Issue** nel repository GitHub! 😊