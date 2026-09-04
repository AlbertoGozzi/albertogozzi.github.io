# Autoclicker

Autoclicker con interfaccia grafica per Windows, scritto in Python.

## Funzionalità

- Intervallo tra i click configurabile (ore / minuti / secondi / millisecondi)
- Pulsante del mouse: sinistro, destro o centrale
- Click singolo o doppio
- Click nella posizione corrente del cursore, oppure in una posizione fissa (con pulsante "Cattura posizione" che registra le coordinate dopo 3 secondi)
- Numero di click infinito oppure limitato a un numero specifico
- Hotkey globali: **F6** per avviare/fermare, **F9** per uscire (funzionano anche se la finestra non è in primo piano)
- Le impostazioni vengono salvate automaticamente in `autoclicker_config.json`

## Come ottenere autoclicker.exe (anche se non hai Python)

Non serve installare nulla a mano: scarica la cartella `autoclicker` sul tuo PC e fai doppio click su **`build_exe.bat`**.

- Se non hai Python, lo script prova a installarlo da solo tramite `winget` (il gestore pacchetti già integrato in Windows 10/11) senza bisogno del browser. Al termine ti chiederà di richiudere la finestra e rilanciare `build_exe.bat` una seconda volta (serve per aggiornare il PATH).
- Se hai già Python, o dopo l'installazione automatica, lo script installa le dipendenze e genera `dist\autoclicker.exe`, poi apre la cartella `dist` in automatico.

Se il tuo Windows non ha `winget` (versioni molto vecchie), lo script te lo segnala e ti indica di installare Python dal Microsoft Store (cerca "Python 3.12") prima di rilanciare `build_exe.bat`.

Nota: l'eseguibile va generato direttamente sul tuo PC Windows — io lavoro da un ambiente Linux e PyInstaller non permette di creare `.exe` da un altro sistema operativo, quindi non posso fornirtelo già pronto in questo repository.

## Eseguirlo senza creare l'exe (avanzato)

Se preferisci lanciarlo direttamente con Python, dopo averlo installato:

```
pip install -r requirements.txt
python autoclicker.py
```

## Nota

Alcuni antivirus segnalano gli autoclicker come potenzialmente indesiderati perché simulano input del mouse: è un falso positivo comune per questo tipo di tool. Usalo solo su software che ne consentono l'uso (molti giochi online vietano gli autoclicker nei loro regolamenti).
