from flask import Flask
from mambo_controller import MamboController
import time
server = Flask(__name__)


@server.route('/drone/takeoff')
def droneTakeOff():

    controller.takeOff()
    return 'Drone Taking off!!!'

@server.route('/drone/landing')
def droneLanding():
    #controller.safeLand()
    return 'Drone landing!!!'

@server.route('/drone/moveleft')
def droneMoveLeft():
    #controller.moveLeft()
    return 'Drone Moving Left!!!'

@server.route('/drone/moveright')
def droneMoveRight():
    #controller.moveRight()
    return 'Drone Moving Right!!!'

@server.route('/drone/rotateleft')
def droneRotateLeft():
    #controller.rotateLeft()
    return 'Drone Rotating Left!!!'

@server.route('/drone/rotateright')
def droneRotateRight():
    #controller.rotateRight()
    return 'Drone Rotating Right!!!'

@server.route('/drone/fire')
def droneFire():
    #controller.fire
    return 'Drone firing!!!'


if __name__ == "__main__":

    print("main")
    controller = MamboController()
    controller.start()

    time.sleep(5)

    server.run()
