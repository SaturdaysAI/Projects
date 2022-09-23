from vendor.Minidrone import Mambo
from mambo_controller import MamboController


def main():
    print("init drone test")
    controller = MamboController()

    controller.start()
    controller.takeOff()
    controller.safeLand()


if __name__ == "__main__":
    main()
