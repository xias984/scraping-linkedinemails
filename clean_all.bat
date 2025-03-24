@echo off
setlocal

echo 🧯 Chiudo eventuali processi Python...
taskkill /f /im python.exe >nul 2>&1

echo 🧹 Rimozione cartelle virtualenv e Python locale...
rmdir /s /q env
rmdir /s /q python312

echo 🧼 Pulizia build PyInstaller...
rmdir /s /q build
rmdir /s /q dist
rmdir /s /q release
del /q *.spec

echo 🔥 Pulizia cache Python...
for /r %%i in (*.pyc *.pyo *.zip) do del /q "%%i"
for /d /r %%d in (__pycache__) do rmdir /s /q "%%d"

echo ✅ Tutto pulito.
pause
