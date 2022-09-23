"""
Demo the trick flying for the python interface

Author: Amy McGovern
"""

# from pyparrot.Minidrone import Mambo
from vendor.Minidrone import Mambo


class MamboController:
    mamboAddrStatic = "e0:14:0c:71:3d:fc"

    def __init__(self):
        print("simple init")

    def start(self):
        print("start drone controller")
        self.verticalCount = 0
        self.horizontalCount = 0
        self.deepCount = 0
        self.mamboAddr = "e0:14:0c:71:3d:fc"
        #self.mambo = Mambo(self.mamboAddr, use_wifi=False)
        self.mambo = Mambo(self.mamboAddrStatic, use_wifi=False)
        self.success = self.mambo.connect(num_retries=3)

    def moveRight(self):
        print(f"/nmoveRight")
        print("horizontalCount: " + str(self.horizontalCount))
        if abs(self.horizontalCount) < 5:
            self.mambo.fly_direct(roll=15, pitch=0, yaw=0, vertical_movement=0, duration=1)
            self.horizontalCount = self.horizontalCount + 1
            self.mambo.smart_sleep(1)

    def takeOff(self):
        print(f"/ntakeOff")
        self.mambo.safe_takeoff(5)


    def safeLand(self):
        self.mambo.safe_land(5)
        print(f"/nsafeLand")


    def moveLeft(self):
        print(f"/nmoveLeft")
        print("horizontalCount: " + str(self.horizontalCount))
        if abs(self.horizontalCount) < 5:
            self.mambo.fly_direct(roll=-15, pitch=0, yaw=0, vertical_movement=0, duration=1)
            self.horizontalCount = self.horizontalCount - 1
            self.mambo.smart_sleep(1)

    def moveForward(self):
        print(f"/nmoveForward")
        print("deepCount: " + str(self.deepCount))
        if abs(self.deepCount) < 5:
            self.mambo.fly_direct(roll=0, pitch=20, yaw=0, vertical_movement=0, duration=1)
            self.deepCount = self.deepCount + 1
            self.mambo.smart_sleep(1)

    def moveBackward(self):
        print(f"/nmoveBackward")
        print("deepCount: " + str(self.deepCount))
        if abs(self.deepCount) < 5:
            self.mambo.fly_direct(roll=0, pitch=-20, yaw=-0, vertical_movement=0, duration=1)
            self.deepCount = self.deepCount + 1
            self.mambo.smart_sleep(1)

    def moveUp(self):
        print(f"/nmoveUp")
        print("verticalCount: " + str(self.verticalCount))
        if abs(self.verticalCount) < 5:
            self.mambo.fly_direct(roll=0, pitch=0, yaw=0, vertical_movement=10, duration=1)
            self.verticalCount = self.verticalCount + 1
            self.mambo.smart_sleep(1)

    def moveDown(self):
        print(f"/nmoveDown")

        print("verticalCount: " + str(self.verticalCount))
        if abs(self.verticalCount) < 5:
            self.mambo.fly_direct(roll=0, pitch=0, yaw=0, vertical_movement=-10, duration=1)
            self.verticalCount = self.verticalCount - 1
            self.mambo.smart_sleep(1)

    def rotateRight(self):
        print(f"/nrotateRight")
        self.mambo.fly_direct(roll=0, pitch=0, yaw=10, vertical_movement=0, duration=1)
        self.mambo.smart_sleep(1)

    def rotateLeft(self):
        print(f"/nrotateLeft")
        self.mambo.fly_direct(roll=0, pitch=0, yaw=-10, vertical_movement=0, duration=1)
        self.mambo.smart_sleep(1)

    def takeOff(self):
        self.mambo.safe_takeoff(5)
        print(f"/ntakeOff")

    def safeLand(self):
        self.mambo.safe_land(5)
        print(f"/nsafeLand")

    def fire(self):
        self.mambo.fire_gun()
        print(f"/nfire")
    

