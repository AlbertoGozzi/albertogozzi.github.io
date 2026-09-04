@echo off
echo Installazione dipendenze...
pip install -r requirements.txt pyinstaller
if errorlevel 1 goto error

echo Creazione dell'eseguibile...
pyinstaller --onefile --noconsole --name autoclicker autoclicker.py
if errorlevel 1 goto error

echo.
echo Fatto! Trovi autoclicker.exe nella cartella dist\
pause
exit /b 0

:error
echo.
echo Si e' verificato un errore. Controlla i messaggi sopra.
pause
exit /b 1
