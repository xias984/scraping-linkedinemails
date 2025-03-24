@echo off
setlocal

echo 🔍 Controllo versione Python...
where python >nul 2>&1
IF ERRORLEVEL 1 (
    echo ❌ Python non trovato. Installa Python 3.12 prima di continuare.
    pause
    exit /b
)

REM Ottieni la versione e verifica >= 3.12
for /f "tokens=2 delims==" %%v in ('python -c "import sys; print(f'version=={sys.version_info.major}.{sys.version_info.minor}')"') do set VERSION=%%v

echo ✅ Trovato Python versione: %VERSION%

IF NOT EXIST env (
    echo 🧪 Creo virtualenv 'env'...
    python -m venv env
) ELSE (
    echo ℹ️ Virtualenv 'env' già presente.
)

echo ▶️ Attivo virtualenv...
call env\Scripts\activate.bat

echo 📦 Installo dipendenze...
pip install --upgrade pip
pip install -r requirements.txt

echo ✅ Ambiente pronto.
pause
