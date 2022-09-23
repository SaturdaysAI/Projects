from flask import Flask
import time
from tello_controller import TelloController

server = Flask(__name__)

@server.route('/drone/takeoff')
def droneTakeOff():
    print('taking off!!!!!!')
    drone_controller.take_off()
    return 'Drone Taking off!!!'

@server.route('/drone/landing')
def droneLanding():
    print('landing!!!!!!')
    drone_controller.land()
    return 'Drone landing!!!'

@server.route('/drone/left')
def droneMoveLeft():
    print('moving left!!!!!!')
    drone_controller.move_left()
    return 'Drone Moving Left!!!'

@server.route('/drone/right')
def droneMoveRight():
    print('moving right!!!!!!')
    drone_controller.move_right()
    return 'Drone Moving Right!!!'

@server.route('/drone/up')
def droneMoveUp():
    print('moving up!!!!!!')
    drone_controller.move_up()
    return 'Drone Moving Up!!!'

@server.route('/drone/down')
def droneMoveDown():
    print('moving up!!!!!!')
    drone_controller.move_down()
    return 'Drone Moving Up!!!'

if __name__ == "__main__":

    print("--init tello controller--")
    drone_controller = TelloController()
    drone_controller.start()
    print("--ready--")

    time.sleep(2)
    print('--taking off--')
    drone_controller.take_off()
    print('--running server--')
    server.run()
