from flask import Flask
from flask_socketio import SocketIO, emit
import logging
from SenseoDriver import SenseoDriver

logger = logging.getLogger()
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

app = Flask(__name__)
socketio = SocketIO(app, async_mode="threading")

def send_update(status):
    socketio.emit("update", status, broadcast=True, json=True, ignore_queue=True)

machine_driver = SenseoDriver(send_update)

@socketio.on("connect")
def test_connect():
    logger.info("Client connected")

@socketio.on("disconnect")
def test_disconnect():
    logger.info("Client disconnected")

@socketio.on("turn_on")
def turn_on():
    machine_driver.turn_on()

@socketio.on("turn_off")
def turn_off():
    machine_driver.turn_off()

@socketio.on("stop")
def stop():
    machine_driver.stop()

@socketio.on("brew_one")
def brew_one():
    machine_driver.brew_one()

@socketio.on("brew_two")
def brew_two():
    machine_driver.brew_two()

if __name__ == "__main__":
    machine_thread.start()
    socketio.run(app, host='0.0.0.0')
