"""Autoclicker per Windows con interfaccia grafica, intervallo configurabile,
posizione fissa o cursore corrente, e hotkey globale per avvio/stop."""

import json
import os
import threading
import time
import tkinter as tk
from tkinter import ttk, messagebox

from pynput import keyboard, mouse

CONFIG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "autoclicker_config.json")

DEFAULT_CONFIG = {
    "hours": 0,
    "minutes": 0,
    "seconds": 0,
    "milliseconds": 100,
    "button": "left",
    "click_type": "single",
    "position_mode": "cursor",
    "fixed_x": 0,
    "fixed_y": 0,
    "repeat_mode": "infinite",
    "repeat_count": 100,
    "toggle_hotkey": "f6",
    "quit_hotkey": "f9",
}

BUTTON_MAP = {
    "left": mouse.Button.left,
    "right": mouse.Button.right,
    "middle": mouse.Button.middle,
}


class AutoClicker:
    def __init__(self, root):
        self.root = root
        self.root.title("Autoclicker")
        self.root.resizable(False, False)

        self.config = self.load_config()

        self.mouse_ctl = mouse.Controller()
        self.running = False
        self.click_thread = None
        self.picking_position = False

        self.build_ui()
        self.start_hotkey_listener()

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def load_config(self):
        if os.path.exists(CONFIG_PATH):
            try:
                with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                    saved = json.load(f)
                cfg = dict(DEFAULT_CONFIG)
                cfg.update(saved)
                return cfg
            except (json.JSONDecodeError, OSError):
                pass
        return dict(DEFAULT_CONFIG)

    def save_config(self):
        try:
            with open(CONFIG_PATH, "w", encoding="utf-8") as f:
                json.dump(self.read_ui_values(), f, indent=2)
        except OSError:
            pass

    def build_ui(self):
        pad = {"padx": 8, "pady": 4}

        interval_frame = ttk.LabelFrame(self.root, text="Intervallo tra i click")
        interval_frame.grid(row=0, column=0, sticky="ew", **pad)

        self.hours_var = tk.IntVar(value=self.config["hours"])
        self.minutes_var = tk.IntVar(value=self.config["minutes"])
        self.seconds_var = tk.IntVar(value=self.config["seconds"])
        self.millis_var = tk.IntVar(value=self.config["milliseconds"])

        for i, (label, var, maxv) in enumerate([
            ("ore", self.hours_var, 23),
            ("min", self.minutes_var, 59),
            ("sec", self.seconds_var, 59),
            ("ms", self.millis_var, 999),
        ]):
            ttk.Label(interval_frame, text=label).grid(row=0, column=2 * i, padx=(6, 2))
            ttk.Spinbox(interval_frame, from_=0, to=maxv, width=5, textvariable=var).grid(
                row=0, column=2 * i + 1
            )

        click_frame = ttk.LabelFrame(self.root, text="Click")
        click_frame.grid(row=1, column=0, sticky="ew", **pad)

        ttk.Label(click_frame, text="Pulsante").grid(row=0, column=0, sticky="w")
        self.button_var = tk.StringVar(value=self.config["button"])
        ttk.Combobox(
            click_frame, textvariable=self.button_var, state="readonly", width=10,
            values=["left", "right", "middle"],
        ).grid(row=0, column=1, sticky="w")

        ttk.Label(click_frame, text="Tipo").grid(row=1, column=0, sticky="w")
        self.click_type_var = tk.StringVar(value=self.config["click_type"])
        ttk.Combobox(
            click_frame, textvariable=self.click_type_var, state="readonly", width=10,
            values=["single", "double"],
        ).grid(row=1, column=1, sticky="w")

        pos_frame = ttk.LabelFrame(self.root, text="Posizione")
        pos_frame.grid(row=2, column=0, sticky="ew", **pad)

        self.position_mode_var = tk.StringVar(value=self.config["position_mode"])
        ttk.Radiobutton(
            pos_frame, text="Posizione corrente del cursore", value="cursor",
            variable=self.position_mode_var,
        ).grid(row=0, column=0, columnspan=3, sticky="w")
        ttk.Radiobutton(
            pos_frame, text="Posizione fissa:", value="fixed",
            variable=self.position_mode_var,
        ).grid(row=1, column=0, sticky="w")

        self.fixed_x_var = tk.IntVar(value=self.config["fixed_x"])
        self.fixed_y_var = tk.IntVar(value=self.config["fixed_y"])
        ttk.Entry(pos_frame, textvariable=self.fixed_x_var, width=6).grid(row=1, column=1)
        ttk.Entry(pos_frame, textvariable=self.fixed_y_var, width=6).grid(row=1, column=2)
        self.pick_btn = ttk.Button(pos_frame, text="Cattura posizione (3s)", command=self.pick_position)
        self.pick_btn.grid(row=1, column=3, padx=6)

        repeat_frame = ttk.LabelFrame(self.root, text="Ripetizioni")
        repeat_frame.grid(row=3, column=0, sticky="ew", **pad)

        self.repeat_mode_var = tk.StringVar(value=self.config["repeat_mode"])
        ttk.Radiobutton(
            repeat_frame, text="Fino allo stop", value="infinite",
            variable=self.repeat_mode_var,
        ).grid(row=0, column=0, sticky="w")
        ttk.Radiobutton(
            repeat_frame, text="Numero di click:", value="count",
            variable=self.repeat_mode_var,
        ).grid(row=1, column=0, sticky="w")
        self.repeat_count_var = tk.IntVar(value=self.config["repeat_count"])
        ttk.Entry(repeat_frame, textvariable=self.repeat_count_var, width=8).grid(row=1, column=1)

        hotkey_frame = ttk.LabelFrame(self.root, text="Hotkey globali")
        hotkey_frame.grid(row=4, column=0, sticky="ew", **pad)
        ttk.Label(hotkey_frame, text=f"Avvia/ferma: {self.config['toggle_hotkey'].upper()}").grid(
            row=0, column=0, sticky="w"
        )
        ttk.Label(hotkey_frame, text=f"Esci: {self.config['quit_hotkey'].upper()}").grid(
            row=1, column=0, sticky="w"
        )

        action_frame = ttk.Frame(self.root)
        action_frame.grid(row=5, column=0, sticky="ew", **pad)
        self.toggle_btn = ttk.Button(action_frame, text="Avvia", command=self.toggle_clicking)
        self.toggle_btn.grid(row=0, column=0, padx=4)

        self.status_var = tk.StringVar(value="Fermo")
        ttk.Label(self.root, textvariable=self.status_var, foreground="blue").grid(
            row=6, column=0, sticky="w", **pad
        )

    def read_ui_values(self):
        return {
            "hours": self.hours_var.get(),
            "minutes": self.minutes_var.get(),
            "seconds": self.seconds_var.get(),
            "milliseconds": self.millis_var.get(),
            "button": self.button_var.get(),
            "click_type": self.click_type_var.get(),
            "position_mode": self.position_mode_var.get(),
            "fixed_x": self.fixed_x_var.get(),
            "fixed_y": self.fixed_y_var.get(),
            "repeat_mode": self.repeat_mode_var.get(),
            "repeat_count": self.repeat_count_var.get(),
            "toggle_hotkey": self.config["toggle_hotkey"],
            "quit_hotkey": self.config["quit_hotkey"],
        }

    def pick_position(self):
        if self.picking_position:
            return
        self.picking_position = True
        self.pick_btn.config(state="disabled")

        def countdown(n):
            if n > 0:
                self.pick_btn.config(text=f"Cattura tra {n}...")
                self.root.after(1000, countdown, n - 1)
            else:
                x, y = self.mouse_ctl.position
                self.fixed_x_var.set(int(x))
                self.fixed_y_var.set(int(y))
                self.position_mode_var.set("fixed")
                self.pick_btn.config(text="Cattura posizione (3s)", state="normal")
                self.picking_position = False

        countdown(3)

    def get_interval_seconds(self):
        values = self.read_ui_values()
        total = (
            values["hours"] * 3600
            + values["minutes"] * 60
            + values["seconds"]
            + values["milliseconds"] / 1000
        )
        return max(total, 0.01)

    def toggle_clicking(self):
        if self.running:
            self.stop_clicking()
        else:
            self.start_clicking()

    def start_clicking(self):
        if self.running:
            return
        values = self.read_ui_values()
        self.save_config()
        self.running = True
        self.toggle_btn.config(text="Ferma")
        self.status_var.set("In esecuzione...")
        self.click_thread = threading.Thread(target=self.click_loop, args=(values,), daemon=True)
        self.click_thread.start()

    def stop_clicking(self):
        self.running = False
        self.toggle_btn.config(text="Avvia")
        self.status_var.set("Fermo")

    def click_loop(self, values):
        interval = self.get_interval_seconds()
        button = BUTTON_MAP[values["button"]]
        clicks = 2 if values["click_type"] == "double" else 1
        limited = values["repeat_mode"] == "count"
        remaining = values["repeat_count"] if limited else None

        while self.running:
            if values["position_mode"] == "fixed":
                self.mouse_ctl.position = (values["fixed_x"], values["fixed_y"])
            self.mouse_ctl.click(button, clicks)

            if limited:
                remaining -= 1
                if remaining <= 0:
                    self.root.after(0, self.stop_clicking)
                    break

            time.sleep(interval)

    def start_hotkey_listener(self):
        def on_press(key):
            name = self.key_name(key)
            if name == self.config["toggle_hotkey"]:
                self.root.after(0, self.toggle_clicking)
            elif name == self.config["quit_hotkey"]:
                self.root.after(0, self.on_close)

        self.listener = keyboard.Listener(on_press=on_press)
        self.listener.daemon = True
        self.listener.start()

    @staticmethod
    def key_name(key):
        if isinstance(key, keyboard.KeyCode):
            return None
        return key.name

    def on_close(self):
        self.running = False
        self.save_config()
        try:
            self.listener.stop()
        except Exception:
            pass
        self.root.destroy()


def main():
    root = tk.Tk()
    try:
        AutoClicker(root)
    except Exception as exc:
        messagebox.showerror("Errore", str(exc))
        raise
    root.mainloop()


if __name__ == "__main__":
    main()
