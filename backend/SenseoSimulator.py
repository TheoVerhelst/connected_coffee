from threading import Thread
from queue import Queue, Empty
from functools import partial
from time import sleep, perf_counter

class SenseoSimulator():
    def __init__(self, status_change_callback):
        self.machine_thread = MachineThread(self.status_change_callback)
        self.machine_thread.start()

        self.ordered_cups = 0

        # The function to call when the state of the machine changes
        self.status_change_callback = status_change_callback

        self.wait_time = 0.1

    def send_status(self):
        self.status_change_callback({
            "state": self.machine_thread.state,
            "ordered_cups": self.ordered_cups,
            "led": self.machine_thread.led
        })

    def status_change_callback(self):
        if self.ordered_cups > 0 and self.machine_thread.state == "ready":
            sleep(self.wait_time)
            self.try_brew()
            self.ordered_cups = 0

        self.send_status()

    def turn_on(self):
        if self.machine_thread.state == "off":
            self.machine_thread.commands.put("power")
            self.ordered_cups = 0

    def turn_off(self):
        if self.machine_thread.state != "off":
            self.machine_thread.commands.put("power")
            self.ordered_cups = 0

    def stop(self):
        if self.machine_thread.state in ("brewing", "heating"):
            self.ordered_cups = 0
            if self.machine_thread.state == "brewing":
                # Have you tried turning it off and on again?
                self.machine_thread.commands.put("power")
                sleep(self.wait_time)
                self.machine_thread.commands.put("power")

    def brew_one(self):
        self.ordered_cups = 1
        self.try_brew()

    def brew_two(self):
        self.ordered_cups = 2
        self.try_brew()

    def try_brew(self):
        if self.machine_thread.state == "off":
            self.machine_thread.commands.put("power")
        elif self.machine_thread.state == "ready":
            self.machine_thread.commands.put("brew_" + ("one" if self.ordered_cups == 1 else "two"))


class MachineThread(Thread):
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

        self.status_change_callback = status_change_callback
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
            self.led = True
            self.status_change_callback()
        else:
            self.state = "off"
            self.remaining_brew_time = 0
            self.led = False
            self.status_change_callback()

    def brew(self, quantity):
        if self.state == "ready":
            self.state = "brewing"
            self.remaining_brew_time = quantity
            self.status_change_callback()

    def update(self, dt):
        if self.state in ("heating", "brewing") and self.remaining_led_blink_time <= 0:
                self.led = not self.led
                self.remaining_led_blink_time = self.led_blink_period
                self.status_change_callback()

        if self.state == "heating":
            self.temperature += dt * self.heat_rate
            self.remaining_led_blink_time -= dt

            if self.temperature >= 1:
                self.state = "ready"
                self.led = True
                self.status_change_callback()

        elif self.state == "brewing":
            self.remaining_brew_time -= dt * self.brew_rate
            self.temperature -= dt * self.brew_cool_rate

            if self.remaining_brew_time <= 0:
                self.state = "heating"
                self.status_change_callback()

        elif self.state == "off":
            self.temperature -= dt * self.off_cool_rate
            self.temperature = max(0, self.temperature)
