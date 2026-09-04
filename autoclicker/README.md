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

## Come eseguirlo su Windows

1. Installa Python 3 da [python.org](https://www.python.org/downloads/) (durante l'installazione spunta "Add python.exe to PATH").
2. Apri il Prompt dei comandi (cmd) nella cartella `autoclicker`.
3. Installa la dipendenza:

   ```
   pip install -r requirements.txt
   ```

4. Avvia il programma:

   ```
   python autoclicker.py
   ```

## Creare un eseguibile .exe (opzionale)

Se preferisci un file `.exe` da avviare con doppio click, senza dover installare Python ogni volta:

```
pip install pyinstaller
pyinstaller --onefile --noconsole autoclicker.py
```

L'eseguibile verrà creato in `dist/autoclicker.exe`.

## Nota

Alcuni antivirus segnalano gli autoclicker come potenzialmente indesiderati perché simulano input del mouse: è un falso positivo comune per questo tipo di tool. Usalo solo su software che ne consentono l'uso (molti giochi online vietano gli autoclicker nei loro regolamenti).
