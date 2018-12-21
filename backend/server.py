from os.path import abspath
from flask import Flask
from flask_socketio import SocketIO, send, emit
from time import sleep
import logging

logger = logging.getLogger()
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

app = Flask(__name__)
socketio = SocketIO(app)

handlers = {}
def handler(function):
    handlers[function.__name__] = function
    return function


@socketio.on("command")
def receive_message(message):
    logger.info("Received command: " + message)
    if message in handlers:
        handlers[message]()

@socketio.on("connect")
def test_connect():
    logger.info("Client connected")
    send_update("off", 0, False)

@socketio.on("disconnect")
def test_disconnect():
    logger.info("Client disconnected")

status = "off"
ordered_cups = 0
led = False

def send_update(status_, ordered_cups_, led_):
    global status
    global ordered_cups
    global led
    status = status_
    ordered_cups = ordered_cups_
    led = led_
    logger.info("Sending update: " + status + ", ordered_cups = " + str(ordered_cups) + ", led = " + str(led))
    socketio.emit("update", {
        "status": status,
        "ordered_cups": ordered_cups,
        "led": led
    }, broadcast=True, json=True, ignore_queue=True)

threads = []

def def_and_send_thread(duration, status, ordered_cups, led):
    socketio.sleep(duration)
    send_update(status, ordered_cups, led)

def wait_and_send(duration, status, ordered_cups, led):
    t = socketio.start_background_task(def_and_send_thread, duration, status, ordered_cups, led)
    threads.append(t)

delay = 2

@handler
def turn_on():
    send_update("heating", 0, True)
    wait_and_send(delay, "ready", 0, True)

@handler
def turn_off():
    send_update("off", 0, False)

@handler
def stop():
    send_update("ready", 0, True)

@handler
def brew_one():
    if status != "ready":
        send_update("heating", 1, True)
        wait_and_send(delay, "brewing", 1, True)
        wait_and_send(2 * delay, "ready", 0, True)
    else:
        send_update("brewing", 1, True)
        wait_and_send(delay, "ready", 0, True)

@handler
def brew_two():
    if status != "ready":
        send_update("heating", 2, True)
        wait_and_send(delay, "brewing", 2, True)
        wait_and_send(2 * delay, "ready", 0, True)
    else:
        send_update("brewing", 2, True)
        wait_and_send(delay, "ready", 0, True)

socketio.run(app, host='0.0.0.0')
