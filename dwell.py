import tkinter as tk
from tkinter import simpledialog
from pynput.mouse import Listener, Controller, Button
from threading import Thread, Timer
import logging

logging.basicConfig(level=logging.INFO)

class DwellClicker:
    def __init__(self, gui_root, dwell_time=2.0, radius=5):
        self.dwell_time = dwell_time
        self.radius = radius
        self.mouse_controller = Controller()
        self.dwell_timer = None
        self.last_position = None
        self.listener = None
        self.gui_root = gui_root
        self.active = False

    def on_move(self, x, y):
        if self.last_position:
            dx = x - self.last_position[0]
            dy = y - self.last_position[1]
            if dx*dx + dy*dy > self.radius*self.radius:
                self.reset_timer()
                self.last_position = (x, y)
        else:
            self.last_position = (x, y)

    def on_click(self, x, y, button, pressed):
        if pressed:
            self.reset_timer(cancel_only=True)

    def reset_timer(self, cancel_only=False):
        if self.dwell_timer is not None:
            self.dwell_timer.cancel()
        if not cancel_only and self.active:
            self.dwell_timer = Timer(self.dwell_time, self.perform_click)
            self.dwell_timer.start()

    def perform_click(self):
        logging.info("Performing click")
        self.mouse_controller.click(Button.left)

    def toggle_listener(self, event=None):
        if self.active:
            self.active = False
            if self.listener is not None:
                self.listener.stop()
                self.listener = None
            self.update_status("Dwell Clicker stopped.")
        else:
            self.active = True
            self.listener = Listener(on_move=self.on_move, on_click=self.on_click)
            self.listener.start()
            self.update_status("Dwell Clicker running...")

    def update_status(self, text):
        self.gui_root.status_label.config(text=text)

    def update_dwell_time(self):
        time = simpledialog.askfloat("Input", "Set dwell time (seconds):",
                                     parent=self.gui_root.window,
                                     minvalue=0.1, maxvalue=10.0)
        if time is not None:
            self.dwell_time = time
            self.gui_root.dwell_label.config(text=f"Dwell Time: {self.dwell_time} seconds")

    def update_radius(self):
        radius = simpledialog.askinteger("Input", "Set ignore radius (pixels):",
                                         parent=self.gui_root.window,
                                         minvalue=1, maxvalue=50)
        if radius is not None:
            self.radius = radius
            self.gui_root.radius_label.config(text=f"Ignore Radius: {self.radius} pixels")

class GUI:
    def __init__(self, root):
        self.window = root
        self.window.title("Dwell Clicker GUI")

        self.start_button = tk.Button(self.window, text="Start / Stop", command=self.toggle_listener)
        self.start_button.pack(pady=20)

        self.dwell_button = tk.Button(self.window, text="Set Dwell Time", command=self.update_dwell_time)
        self.dwell_button.pack(pady=20)

        self.dwell_label = tk.Label(self.window, text="Dwell Time: 2.0 seconds")
        self.dwell_label.pack(pady=10)

        self.radius_button = tk.Button(self.window, text="Set Ignore Radius", command=self.update_radius)
        self.radius_button.pack(pady=20)

        self.radius_label = tk.Label(self.window, text="Ignore Radius: 5 pixels")
        self.radius_label.pack(pady=10)

        self.status_label = tk.Label(self.window, text="Dwell Clicker stopped.")
        self.status_label.pack(pady=10)

        self.clicker = DwellClicker(self)

    def toggle_listener(self):
        self.clicker.toggle_listener()

    def update_dwell_time(self):
        self.clicker.update_dwell_time()

    def update_radius(self):
        self.clicker.update_radius()

def main():
    root = tk.Tk()
    gui = GUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()