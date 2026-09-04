@echo off
setlocal

where python >nul 2>nul
if %errorlevel%==0 goto haspython

echo Python non trovato sul PC. Provo a installarlo automaticamente con winget...
where winget >nul 2>nul
if not %errorlevel%==0 goto nowinget

winget install -e --id Python.Python.3.12 --accept-source-agreements --accept-package-agreements
if not %errorlevel%==0 goto nowinget

echo.
echo Python e' stato installato. Ora CHIUDI questa finestra e fai di nuovo doppio click su build_exe.bat
echo (serve riaprire il terminale perche' Windows aggiorni il PATH).
pause
exit /b 0

:nowinget
echo.
echo Non sono riuscito a installare Python automaticamente.
echo Installalo tu da Microsoft Store (cerca "Python 3.12") oppure da python.org,
echo poi rilancia questo file con doppio click.
pause
exit /b 1

:haspython
echo Python trovato. Installazione dipendenze...
python -m pip install -r requirements.txt pyinstaller
if errorlevel 1 goto error

echo Creazione dell'eseguibile...
python -m PyInstaller --onefile --noconsole --name autoclicker autoclicker.py
if errorlevel 1 goto error

echo.
echo Fatto! Trovi autoclicker.exe nella cartella dist\
start "" explorer dist
pause
exit /b 0

:error
echo.
echo Si e' verificato un errore. Controlla i messaggi sopra.
pause
exit /b 1
