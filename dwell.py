import tkinter as tk
from tkinter import simpledialog, messagebox
from pynput.mouse import Listener, Controller, Button
from threading import Thread, Timer
import logging

logging.basicConfig(level=logging.INFO)

# Constants for default values
DEFAULT_DWELL_TIME = 2.0
DEFAULT_RADIUS = 5
MIN_DWELL_TIME = 0.1
MAX_DWELL_TIME = 10.0
MIN_RADIUS = 1
MAX_RADIUS = 50

class DwellClicker:
    def __init__(self, gui_root, dwell_time=DEFAULT_DWELL_TIME, radius=DEFAULT_RADIUS):
        self.dwell_time = dwell_time
        self.radius = radius
        self.mouse_controller = Controller()
        self.dwell_timer = None
        self.last_position = None
        self.listener = None
        self.gui_root = gui_root
        self.active = False

    def on_move(self, x, y):
        try:
            if self.last_position:
                dx = x - self.last_position[0]
                dy = y - self.last_position[1]
                if dx*dx + dy*dy > self.radius*self.radius:
                    self.reset_timer()
                    self.last_position = (x, y)
            else:
                self.last_position = (x, y)
        except Exception as e:
            logging.error(f"Error in on_move: {e}")
            self.update_status(f"Error: {e}")

    def on_click(self, x, y, button, pressed):
        try:
            if pressed:
                self.reset_timer(cancel_only=True)
        except Exception as e:
            logging.error(f"Error in on_click: {e}")
            self.update_status(f"Error: {e}")

    def reset_timer(self, cancel_only=False):
        try:
            if self.dwell_timer is not None:
                self.dwell_timer.cancel()
            if not cancel_only and self.active:
                self.dwell_timer = Timer(self.dwell_time, self.perform_click)
                self.dwell_timer.start()
        except Exception as e:
            logging.error(f"Error in reset_timer: {e}")
            self.update_status(f"Error: {e}")

    def perform_click(self):
        try:
            logging.info("Performing click")
            self.mouse_controller.click(Button.left)
        except Exception as e:
            logging.error(f"Error in perform_click: {e}")
            self.update_status(f"Error: {e}")

    def toggle_listener(self, event=None):
        try:
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
        except Exception as e:
            logging.error(f"Error in toggle_listener: {e}")
            self.update_status(f"Error: {e}")

    def update_status(self, text):
        try:
            self.gui_root.status_label.config(text=text)
        except Exception as e:
            logging.error(f"Error in update_status: {e}")
            messagebox.showerror("Error", f"Failed to update status: {e}")

    def update_dwell_time(self):
        try:
            time = simpledialog.askfloat("Input", "Set dwell time (seconds):",
                                         parent=self.gui_root.window,
                                         minvalue=MIN_DWELL_TIME, maxvalue=MAX_DWELL_TIME)
            if time is not None:
                self.dwell_time = time
                self.gui_root.dwell_label.config(text=f"Dwell Time: {self.dwell_time} seconds")
        except Exception as e:
            logging.error(f"Error in update_dwell_time: {e}")
            messagebox.showerror("Error", f"Failed to update dwell time: {e}")

    def update_radius(self):
        try:
            radius = simpledialog.askinteger("Input", "Set ignore radius (pixels):",
                                             parent=self.gui_root.window,
                                             minvalue=MIN_RADIUS, maxvalue=MAX_RADIUS)
            if radius is not None:
                self.radius = radius
                self.gui_root.radius_label.config(text=f"Ignore Radius: {self.radius} pixels")
        except Exception as e:
            logging.error(f"Error in update_radius: {e}")
            messagebox.showerror("Error", f"Failed to update radius: {e}")

class GUI:
    def __init__(self, root):
        self.window = root
        self.window.title("Dwell Clicker GUI")

        try:
            self.start_button = tk.Button(self.window, text="Start / Stop", command=self.toggle_listener)
            self.start_button.pack(pady=20)

            self.dwell_button = tk.Button(self.window, text="Set Dwell Time", command=self.update_dwell_time)
            self.dwell_button.pack(pady=20)

            self.dwell_label = tk.Label(self.window, text=f"Dwell Time: {DEFAULT_DWELL_TIME} seconds")
            self.dwell_label.pack(pady=10)

            self.radius_button = tk.Button(self.window, text="Set Ignore Radius", command=self.update_radius)
            self.radius_button.pack(pady=20)

            self.radius_label = tk.Label(self.window, text=f"Ignore Radius: {DEFAULT_RADIUS} pixels")
            self.radius_label.pack(pady=10)

            self.status_label = tk.Label(self.window, text="Dwell Clicker stopped.")
            self.status_label.pack(pady=10)

            self.clicker = DwellClicker(self)
        except Exception as e:
            logging.error(f"Error in GUI initialization: {e}")
            messagebox.showerror("Error", f"Failed to initialize GUI: {e}")

    def toggle_listener(self):
        try:
            self.clicker.toggle_listener()
        except Exception as e:
            logging.error(f"Error in toggle_listener: {e}")
            messagebox.showerror("Error", f"Failed to toggle listener: {e}")

    def update_dwell_time(self):
        try:
            self.clicker.update_dwell_time()
        except Exception as e:
            logging.error(f"Error in update_dwell_time: {e}")
            messagebox.showerror("Error", f"Failed to update dwell time: {e}")

    def update_radius(self):
        try:
            self.clicker.update_radius()
        except Exception as e:
            logging.error(f"Error in update_radius: {e}")
            messagebox.showerror("Error", f"Failed to update radius: {e}")

def main():
    try:
        root = tk.Tk()
        gui = GUI(root)
        root.mainloop()
    except Exception as e:
        logging.error(f"Error in main: {e}")
        messagebox.showerror("Error", f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()