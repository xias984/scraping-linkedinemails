@echo on
setlocal

REM Attiva virtualenv
call env\Scripts\activate.bat

REM Avvia l'app
python main.py
