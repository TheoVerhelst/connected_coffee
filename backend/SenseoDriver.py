from time import sleep, perf_counter
from gpiozero import LED, Button
from Queue import Queue

class SenseoDriver():
    def __init__(self, status_change_callback):
        # We keep track of the state of the machine, by looking at the current
        # state of the led:
        # led off -> "off"
        # led blinking -> "heating", "brewing" or "no_water"
        # lead on -> "ready"
        self.state = "off"

        # We keep track of the last order on the machine
        self.ordered_cups = 0

        # The function to call when the state of the machine changes
        self.status_change_callback = self.status_change_callback

        # We read the led, we don't set it, so it's used as a button
        self.led = Button(1)
        # Assign callbacks for when the led changes state
        self.led.when_pressed = self.on_led_change
        self.led.when_released = self.on_led_change

        # We send commands to the buttons so they're used as leds
        self.power_button = Led(2)
        self.one_button = Led(3)
        self.two_button = Led(4)

        # Number of led events we remember to determine if the led is blinking
        self.number_led_blinks = 3
        # Maximal period of time for the last three events if the led is blinking
        self.led_blink_period = self.number_led_blinks * 0.5 + 0.2
        # Queue of events
        self.past_led_changes = Queue(self.number_led_blinks)
        # State of the led: "blinking", "on" or "off"
        self.led_state = "off"

        # Number of seconds to wait for a button press
        self.button_push_time = 0.1

    def on_led_change(self):
        now = perf_counter()
        self.past_led_states.push(now)

        old_led_state = self.led_state
        # If the last three led events are near in time
        if now - self.past_led_states[0] < self.led_blink_period:
            # It's blinking
            self.led_state = "blinking"
            if old_led_state == "off":
                self.state = "heating"
            else:
                self.state = "brewing"

        elif self.led.is_pressed():
            self.led_state = "on"
            self.state = "ready"
            if self.ordered_cups > 0:
                # Brew a coffee or two when ordered, after heating
                # But wait a bit first, to avoid jamming state changes
                sleep(self.button_push_time)
                self.try_brew()
                self.ordered_cups = 0
        else:
            self.led_state = "off"
            self.state = "off"

        self.status_change_callback({
            "state": state,
            "ordered_cups": self.ordered_cups,
            "led": self.led.is_pressed()
        })

    def push(self, button):
        button.on()
        sleep(self.button_push_time)
        button.off()

    def turn_on(self):
        if self.state == "off":
            self.push(self.power_button)
            self.ordered_cups = 0

    def turn_off(self):
        if self.state != "off":
            self.push(self.power_button)
            self.ordered_cups = 0

    def stop(self):
        if self.state in ("brewing", "heating"):
            self.ordered_cups = 0
            if self.state == "brewing":
                # Have you tried turning it off and on again?
                self.push(self.power_button)
                sleep(self.button_push_time)
                self.push(self.power_button)

    def brew_one(self):
        self.ordered_cups = 1
        self.try_brew()

    def brew_two(self):
        self.ordered_cups = 2
        self.try_brew()

    def try_brew(self):
        if self.state == "off":
            self.push(self.power_button)
        elif self.state == "ready":
            self.push(self.one_button if self.ordered_cups == 1 else self.two_button)
