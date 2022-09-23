import socket
import threading
import time
from vendor.stats import Stats

class TelloController:
    def __init__(self):
        self.local_ip = '0.0.0.0'
        self.local_port = 8889
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # socket for sending cmd
        self.socket.bind((self.local_ip, self.local_port))

        # thread for receiving cmd ack
        self.receive_thread = threading.Thread(target=self._receive_thread)
        self.receive_thread.daemon = True
        self.receive_thread.start()

        self.tello_ip = '192.168.10.1'
        self.tello_port = 8889
        self.tello_address = (self.tello_ip, self.tello_port)
        self.log = []

        self.MAX_TIME_OUT = 15.0
        self.MAX_CMS_MOVEMENT = 40

    def send_command(self, command):
        """
        Send a command to the ip address. Will be blocked until
        the last command receives an 'OK'.
        If the command fails (either b/c time out or error),
        will try to resend the command
        :param command: (str) the command to send
        :param ip: (str) the ip of Tello
        :return: The latest command response
        """
        self.log.append(Stats(command, len(self.log)))

        self.socket.sendto(command.encode('utf-8'), self.tello_address)
        print('sending command: %s to %s' % (command, self.tello_ip))

        start = time.time()
        while not self.log[-1].got_response():
            now = time.time()
            diff = now - start
            if diff > self.MAX_TIME_OUT:
                print('Max timeout exceeded... command %s' % command)
                # TODO: is timeout considered failure or next command still get executed
                # now, next one got executed
                return
        print('Done!!! sent command: %s to %s' % (command, self.tello_ip))

    def _receive_thread(self):
        """Listen to responses from the Tello.

        Runs as a thread, sets self.response to whatever the Tello last returned.

        """
        while True:
            try:
                self.response, ip = self.socket.recvfrom(1024)
                print('from %s: %s' % (ip, self.response))

                self.log[-1].add_response(self.response)
            except Exception:
                print("Caught exception socket.error : %s")

    def on_close(self):
        pass
        # for ip in self.tello_ip_list:
        #     self.socket.sendto('land'.encode('utf-8'), (ip, 8889))
        # self.socket.close()

    def get_log(self):
        return self.log

    # Initial Order
    def start(self):
        self.send_command('command')

    ### COMMAND LIST

    def take_off(self):
        self.send_command('takeoff')

    def land(self):
        self.send_command('land')

    def move_left(self):
        self.send_command('left ' + str(self.MAX_CMS_MOVEMENT))

    def move_right(self):
        self.send_command('right ' + str(self.MAX_CMS_MOVEMENT))

    def move_forward(self):
        self.send_command('forward ' + str(self.MAX_CMS_MOVEMENT))

    def move_backward(self):
        self.send_command('back ' + str(self.MAX_CMS_MOVEMENT))

    def move_up(self):
        self.send_command('up ' + str(self.MAX_CMS_MOVEMENT))

    def move_down(self):
        self.send_command('down ' + str(self.MAX_CMS_MOVEMENT))

    def flip(self):
        self.send_command('flip ' + str(self.MAX_CMS_MOVEMENT))

# print ('Tello: command takeoff land flip forward back left right \r\n       up down cw ccw speed speed?\r\n')