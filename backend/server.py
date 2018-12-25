from flask import Flask
from flask_socketio import SocketIO, emit
import logging
from machine_simulator import MachineSimulator

logger = logging.getLogger()
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

app = Flask(__name__)
socketio = SocketIO(app)

def send_update(status):
    status["ordered_cups"] = 0
    logger.info("Sending update: " + str(status))
    socketio.emit("update", status, broadcast=True, json=True, ignore_queue=True)

@socketio.on("connect")
def test_connect():
    logger.info("Client connected")

@socketio.on("disconnect")
def test_disconnect():
    logger.info("Client disconnected")

@socketio.on("turn_on")
def turn_on(message):
    machine_thread.commands.put("power")

@socketio.on("turn_off")
def turn_off(message):
    machine_thread.commands.put("power")

@socketio.on("stop")
def stop(message):
    machine_thread.commands.put("power")

@socketio.on("brew_one")
def brew_one(message):
    machine_thread.commands.put("brew_one")

@socketio.on("brew_two")
def brew_two(message):
    machine_thread.commands.put("brew_two")

if __name__ == "__main__":
    machine_thread = MachineSimulator(send_update)
    machine_thread.start()
    socketio.run(app, host='0.0.0.0')
