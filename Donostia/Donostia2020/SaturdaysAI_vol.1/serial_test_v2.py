#!/usr/bin/env python
# coding: utf-8


import serial
import time

'''

Not permanent $sudo chmod a+rw /dev/ttyACM1
Give always permissions to /dev
https://askubuntu.com/questions/58119/changing-permissions-on-serial-port 
'''
ser=serial.Serial('/dev/ttyACM0',115200, bytesize = 8, stopbits = 1,
                  timeout = 0, parity='N')
def preprocess(data):
    aux = data.decode('UTF-8').split(',')
    sens.append(float(aux[0]) / 10)
    sens.append(float(aux[1]) / 10)
    sens.append(float(aux[2].split(';')[0]) / 10)

    return sens


print(ser.name)         # check which port was really used
try:
    sens = []
    while True:
        cmd = input("Send Cmmds: ")
        if(cmd == 'ALRM'):
            ser.write(b'ALRM')
        elif (cmd == 'SEND'):

            ser.write(b'SEND')
            while True:

                data = ser.read()           # Wait forever for anything
                time.sleep(0.01)              # Sleep (or inWaiting() doesn't give the correct value)
                data_left = ser.inWaiting()  # Get the number of characters ready to be read
                data += ser.read(data_left) # Do the read and combine it with the first character
                # INFO: https://stackoverflow.com/questions/13017840/using-pyserial-is-it-possible-to-wait-for-data

                # Just in case
                if len(data) >= 14:
                    break
            sens = preprocess(data)
            if (sens[2] < 5.0):
                ser.write(b'ALRM')
                print('Impurity is not acceptable!!')
            
            #print(sens)

            sens = []



except serial.SerialException:
    print('\n*** Serial port closed ***')
    ser.close()
except KeyboardInterrupt:
    print('\n*** Serial port closed ***')
    ser.close()
