#!/usr/bin/env python
# -*- coding: utf-8 -*-

import serial
import time

def main():
    ser = serial.Serial()

    ser.baudrate = 2400
    ser.port = 0 # COM1
    ser.bytesize = serial.EIGHTBITS #number of bits per bytes
    ser.parity = serial.PARITY_NONE #set parity check: no parity
    ser.stopbits = serial.STOPBITS_ONE #number of stop bits

    #ser.timeout = None          #block read
    #ser.timeout = 0             #non-block read
    ser.timeout = 10              #timeout block read	

    ser.xonxoff = False
    ser.rtscts = False
    ser.dsrdtr = False

    ser.open()

    ser.setRTS(False)
    time.sleep(0.1) # maybe larger, depends on device
    #ser.write("some command") # and reading etc.	

    #for i in range(10):
    while(True):
        s = ser.read(14)
        print("%r" % s)
	
    ser.close()

if __name__ == '__main__':
    main()
