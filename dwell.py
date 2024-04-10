from pynput.mouse import Listener, Controller, Button
from threading import Timer
import logging

logging.basicConfig(level=logging.INFO)

class DwellClicker:
    def __init__(self, dwell_time=0.5):
        self.dwell_time = dwell_time
        self.mouse_controller = Controller()
        self.dwell_timer = None
        self.last_position = None

    def on_move(self, x, y):
        if self.last_position != (x, y):
            self.reset_timer()
        self.last_position = (x, y)

    def on_click(self, x, y, button, pressed):
        if pressed:
            self.reset_timer(cancel_only=True)

    def reset_timer(self, cancel_only=False):
        if self.dwell_timer is not None:
            self.dwell_timer.cancel()

        if not cancel_only:
            self.dwell_timer = Timer(self.dwell_time, self.perform_click)
            self.dwell_timer.start()

    def perform_click(self):
        logging.info("Performing click")
        self.mouse_controller.click(Button.left)

    def run(self):
        with Listener(on_move=self.on_move, on_click=self.on_click) as listener:
            listener.join()

if __name__ == "__main__":
    dwell_time = 2  # Dwell time in seconds
    clicker = DwellClicker(dwell_time=dwell_time)
    clicker.run()
