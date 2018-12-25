from threading import Thread
from queue import Queue, Empty
from functools import partial
from time import perf_counter

class MachineSimulator(Thread):
    def __init__(self, status_change_callback):
        super().__init__()
        self.state = "off"
        self.temperature = 0
        self.remaining_brew_time = 0
        self.led = False
        self.remaining_led_blink_time = 0

        self.heat_rate = 0.1
        self.off_cool_rate = 0.05
        self.brew_rate = 0.1
        self.brew_cool_rate = 0.05
        self.led_blink_period = 0.5
        self.sleep_time = 0.1

        self.state_change_callback = status_change_callback
        self.commands = Queue()
        self.handlers = {
            "power": self.power,
            "brew_one": partial(self.brew, 1),
            "brew_two": partial(self.brew, 2)
        }

    def run(self):
        last_time = perf_counter()
        while True:
            try:
                command = self.commands.get(block=True, timeout=self.sleep_time)
                self.handlers[command]()
            except Empty:
                pass
            current_time = perf_counter()
            dt = current_time - last_time
            last_time = current_time
            self.update(dt)

    def power(self):
        if self.state == "off":
            self.state = "heating"
            self.send_status()
        else:
            self.state = "off"
            self.remaining_brew_time = 0
            self.led = False
            self.send_status()

    def brew(self, quantity):
        if self.state == "ready":
            self.state = "brewing"
            self.remaining_brew_time = quantity
            self.send_status()

    def update(self, dt):
        if self.state == "heating":
            self.temperature += dt * self.heat_rate
            self.remaining_led_blink_time -= dt

            if self.remaining_led_blink_time <= 0:
                self.led = not self.led
                self.remaining_led_blink_time = self.led_blink_period
                self.send_status()

            if self.temperature >= 1:
                self.state = "ready"
                self.led = True
                self.send_status()

        elif self.state == "brewing":
            self.remaining_brew_time -= dt * self.brew_rate
            self.temperature -= dt * self.brew_cool_rate

            if self.remaining_brew_time <= 0:
                self.state = "heating"
                self.send_status()

        elif self.state == "off":
            self.temperature -= dt * self.off_cool_rate
            self.temperature = max(0, self.temperature)

    def send_status(self):
        self.state_change_callback({
            "state": self.state,
            "led": self.led
        })
