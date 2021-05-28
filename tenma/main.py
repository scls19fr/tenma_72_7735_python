#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

Python software for Tenma 72-7735 multimeter

http://fr.farnell.com/tenma/72-7735/multimetre-numerique/dp/7430590
Serial protocol: http://www.element14.com/community/docs/DOC-42352/l/software-for-tenma-72-7735-for-windows7-rs232-protocol-information-flie

This software is a personal work. It wasn't developed by Tenma.
Use it at your own risk.

Copyright (C) 2014 Sébastien Celles

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

=====================================================================

AUTO RS232 DIODE BUZZER HOLD TRIANGLE BATTERY
DC
AC
       #####   #####   #####   #####
       #   #   #   #   #   #   #   #
       #   #   #   #   #   #   #   #
####   #####   #####   #####   #####
       #   #   #   #   #   #   #   #
       #   #   #   #   #   #   #   #
       ##### # ##### # ##### # #####

KILO MEGA OHM Hz
n %
micro milli F V A

"""

__author__ = 'Sébastien Celles <s.celles@gmail.com>'
__date__ = '$Date: 2014/10/03 09:06:00 $'
__version__ = '$Revision: 0.1 $'

#import click
from bitarray import bitarray
import binascii
from seven_segments import SevenSegmentsDisplay
import serial
import time
import os

from decimal import Decimal

#class Tenma_Multimeter_LCD_Display:


class Tenma_72_7735_LCD_Display:
    def __init__(self, default_dat='1'):
        self.init_constants()
        self.init_lcd_disp()
        self.init_7_segments()
        self.init_dat(default_dat)

        #print('')
        #print(self.lst_lcd_disp)
        #print('')
        #print(self.d_lcd_disp)

    def init_constants(self):
        self.digits = 4
        self.undef_character = '?'

    def init_7_segments(self):
        self.seven_segments_disp = SevenSegmentsDisplay()

    def init_lcd_disp(self):
        self.init_lcd_disp_list()
        self.init_lcd_disp_dict()

    def init_lcd_disp_list(self):
        self.lst_lcd_disp = [
            ['RS232', 'AUTO', 'DC', 'AC'],
            ['a1', 'a6', 'a5','s'],
            ['a2', 'a7', 'a3','a4'],
            ['b1', 'b6', 'b5','p1'],
            ['b2', 'b7', 'b3','b4'],
            ['c1', 'c6', 'c5','p2'],
            ['c2', 'c7', 'c3','c4'],
            ['d1', 'd6', 'd5','p3'],
            ['d2', 'd7', 'd3','d4'],
            ['DIODE', 'K', 'n','micro'],
            ['BUZZER', 'M', '%','m'],
            ['HOLD', 'TRIANGLE', 'Ohm','F'],
            ['BATTERY', 'Hz', 'V','A'],
            ['0_0', '0_1', '1_0','1_1'] # C2_C1
        ]

        self.d_digits_letter = {
            1: 'a',
            2: 'b',
            3: 'c',
            4: 'd',
        }

    def init_lcd_disp_dict(self):
        self.d_lcd_disp = {}
        for j, com in enumerate(self.lst_lcd_disp):
            for i, disp_str in enumerate(com):
                self.d_lcd_disp[disp_str] = (i, j)

    def init_dat(self, default_dat):
        self.dat = 14 * 4 * bitarray(default_dat)

    def clear_dat(self):
        self.init_dat('0')

    def overwrite_dat(self):
        self.init_dat('1')

    def update_data(self, dat):
        self.dat = dat

    def get_state(self, disp_str):
        (i, j) = self.d_lcd_disp[disp_str]
        n = i + 4 * j
        return(self.dat[n])

    def set_state(self, disp_str, state):
        (i, j) = self.d_lcd_disp[disp_str]
        n = i + 4 * j
        self.dat[n] = state

    def get_states(self, lst_disp_str):
        return([self.get_state(disp_str) for disp_str in lst_disp_str])

    def set_states(self, lst_disp_str, lst_state):
        for i, disp_str in enumerate(lst_disp_str):
            state = lst_disp_str[i]
            self.set_state(self.dat, disp_str, state)

    def disp(self, disp_str):
        if disp_str=='micro':
            return('u')
        elif disp_str=='s': # sign (minus)
            return('-')
        elif disp_str in ['p1', 'p2', 'p3']: # dot
            return('.')
        else:
            return(disp_str)

    def get_str_state(self, disp_str):
        b = self.get_state(disp_str)
        s = self.disp(disp_str)
        if b:
            return(s)
        else:
            return(" "*len(s))

    def get_byte_7_segments(self, digit):
        if digit not in range(1, self.digits + 1):
            raise(NotImplementedError)

    def get_lst_7_segm(self, digit):
        letter = self.d_digits_letter[digit]
        lst_7_segm = [letter+str(i) for i in range(1,8)]
        return(lst_7_segm)

    def get_str_digit(self, digit):
        try:
            lst_7_segm = self.get_lst_7_segm(digit)
            character = self.seven_segments_disp.character(bitarray(self.get_states(lst_7_segm)))
            return(character)
        except:
            return(self.undef_character)

    def set_str_character(self, digit, character):
        lst_7_segm = self.get_lst_7_segm(digit)
        a_bit = self.seven_segments_disp.bitarray(character)
        for i, segment_name in enumerate(lst_7_segm):
            self.set_state(segment_name, a_bit[i])

    """
    def get_decimal_prefix(self):
        states = self.get_states(['M', 'K', 'm', 'micro', 'n'])

        if states == [True, False, False, False, False]: # M
            return(Decimal('1E6'))
        elif states == [False, True, False, False, False]: # K
            return(Decimal('1E3'))
        elif states == [False, False, True, False, False]: # m
            return(Decimal('1E-3'))
        elif states == [False, False, False, True, False]: # u
            return(Decimal('1E-6'))
        elif states == [False, False, False, False, True]: # n
            return(Decimal('1E-9'))
        elif states == [False, False, False, False, False]: # 1
            return(Decimal('1'))
        else:
            raise(NotImplementedError)

    def get_unit(self):
        states = self.get_states(['Ohm', 'Hz', '%', 'F', 'V', 'A'])

        if states == [True, False, False, False, False, False]:
            return('Ohm')
        elif states == [False, True, False, False, False, False]:
            return('Hz')
        elif states == [False, False, True, False, False, False]:
            return('%')
        elif states == [False, False, False, True, False, False]:
            return('F')
        elif states == [False, False, False, False, True, False]:
            return('V')
        elif states == [False, False, False, False, False, True]:
            return('A')
        else:
            raise(NotImplementedError)

    def get_current_type(self):
        states = self.get_states(['AC', 'DC'])

        if states == [True, False]:
            return('AC')
        elif states == [False, True]:
            return('DC')
        else:
            raise(NotImplementedError)
    """

    def get_unique_mode(self, lst, lst_result=None, default_val=None):
        states = bitarray(self.get_states(lst))
        if states.count()<=1:
            for i, disp_str in enumerate(lst):
                states_ref = bitarray('0'*len(lst))
                states_ref[i] = 1
                if states == states_ref:
                    if lst_result is None:
                        return(disp_str)
                    else:
                        return(lst_result[i])
            if default_val is None:
                raise(NotImplementedError)
            else:
                return(default_val)
        else:
            raise(NotImplementedError)

    def get_unit(self):
        lst = ['Ohm', 'Hz', '%', 'F', 'V', 'A']
        return(self.get_unique_mode(lst))

    def get_current_type(self):
        lst = ['AC', 'DC']
        return(self.get_unique_mode(lst))

    def get_decimal_prefix(self):
        lst = ['M', 'K', 'm', 'micro', 'n']
        lst_result = [Decimal('1E6'), Decimal('1E3'),
            Decimal('1E-3'), Decimal('1E-6'), Decimal('1E-9')]
        default_val = Decimal('1')
        val = self.get_unique_mode(lst, lst_result, default_val)
        return(val)

    def get_decimal_no_prefix(self):
        s = self.get_str_digits()
        s = s.replace(' ', '')
        return(Decimal(s))

    def get_decimal(self):
        return(self.get_decimal_no_prefix()*self.get_decimal_prefix())

    def get_str_digits(self):
        s = self.get_str_state("s") + " " + self.get_str_digit(1) \
            + self.get_str_state("p1") + self.get_str_digit(2) \
            + self.get_str_state("p2") + self.get_str_digit(3) \
            + self.get_str_state("p3") + self.get_str_digit(4)
        return(s)

    def __str__(self):
        s = self.get_str_state("AUTO") \
            + " " + self.get_str_state("RS232") \
            + " " + self.get_str_state("DIODE") \
            + " " + self.get_str_state("BUZZER") \
            + " " + self.get_str_state("HOLD") \
            + " " + self.get_str_state("TRIANGLE") \
            + " " + self.get_str_state("BATTERY") \
            + '\n' \
            + self.get_str_state("DC") \
            + '\n' + self.get_str_state("AC") \
            + '\n' \
            + '\n' + self.get_str_digits() \
            + '\n' \
            + '\n' \
            + self.get_str_state("K") \
            + " " + self.get_str_state("M") \
            + " " + self.get_str_state("Ohm") \
            + " " + self.get_str_state("Hz") \
            + '\n' \
            + self.get_str_state("n") \
            + " " + self.get_str_state("%") \
            + '\n' \
            + self.get_str_state("micro") \
            + " " + self.get_str_state("m") \
            + " " + self.get_str_state("F") \
            + " " + self.get_str_state("V") \
            + " " + self.get_str_state("A")
        return(s)

    def display(self):
        print(self)

def transform_data(dat):
    new_dat = bitarray()
    dat.reverse()
    length = 4
    offset = 0
    for seg in range(13,-1,-1):
        dat_part = dat[seg*8+offset:seg*8+offset+length]
        new_dat += dat_part
    return(new_dat)

def clear_term():
    os.system('cls' if os.name == 'nt' else 'clear')

def display_sample_set(disp):
    disp.clear_dat()

    disp.set_state('AUTO', True)
    disp.set_state('RS232', True)
    disp.set_state('HOLD', True)

    disp.set_state('DC', True)
    #disp.set_state('AC', True)

    disp.set_state('s', True)
    disp.set_str_character(1, '0')

    disp.set_state('p1', True)
    #disp.set_state('p2', True)
    #disp.set_state('p3', True)

    disp.set_str_character(2, '1')
    disp.set_str_character(3, '2')
    disp.set_str_character(4, '4')

    #disp.set_state('M', True)
    #disp.set_state('K', True)
    disp.set_state('m', True)
    #disp.set_state('micro', True)

    #disp.set_state('V', True)
    #disp.set_state('Ohm', True)
    disp.set_state('A', True)

    print("")
    disp.display()
    print("")

def display_sample_raw(disp):
    #                01234567890123456789012345678901234567890123456789012345
    #dat = bitarray('00000000000000000000000000000000000000000000000000000000')
    #dat = bitarray('10000000000000000000000000000000000000000000000000000000')
    #dat = bitarray('10001111100111101010000010111000110000001101010011101000')
    dat = bitarray('0001011100100111001111010100011101011101011001110111111010001010100101111010000010111000110000001101010011101000')
    #-> bitarray('11101110101111101011111001110101111000000001000000100001')
    # 17273D475D677E8A97A0B8C0D4E8 -> EEBEBE75E01021

    #dat = bitarray('0001001100100000001100000100011101011101011011100111100010000000100100001010000010110010110001001101000011101000')
    new_dat = transform_data(dat)
    print(dat)
    print(binascii.hexlify(dat).upper())
    print(new_dat)
    print(binascii.hexlify(new_dat).upper())
    disp.update_data(new_dat)

    print("")
    disp.display()
    print("")

def display_values(disp):
    s_disp_error = '?' * 5

    try:
        value = disp.get_decimal_no_prefix()
    except:
        value = s_disp_error
    print("value_no_prefix: %r" % value)

    try:
        value = disp.get_decimal_prefix()
    except:
        value = s_disp_error
    print("value_decimal_prefix: %r" % value)


    try:
        value = disp.get_decimal()
    except:
        value = s_disp_error
    print("value: %r" % value)

    try:
        unit = disp.get_unit()
    except:
        unit = s_disp_error
    print("unit: %r" % unit)

    try:
        unit = disp.get_current_type()
    except:
        unit = s_disp_error
    print("current_type: %r" % unit)

def int2binstring(N, Nbits=8):
    if N<2**Nbits:
        return(bin(N)[2:].rjust(Nbits,'0'))
    else:
        raise(NotImplementedError)

def play_data(filename, blocksize, period):
    with open(filename, 'rb') as f:
    	block = f.read(blocksize)
        s_bin2 = ""
        for i, ch in enumerate(block):
            num = ord(ch)

            s_bin_num = int2binstring(num)

            s_bin2 += s_bin_num

            if (i % period) == period-1:
                yield(bitarray(s_bin2))
                s_bin2 = ''

def display_saved_data(disp):
    for dat in play_data('rev_eng/reads.dat', 1024, 14):
        print(dat)
        new_dat = transform_data(dat)
        print(new_dat)
        disp.update_data(new_dat)
        disp.display()
        display_values(disp)
        time.sleep(1)

def display_serial_data(disp):
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
    dat = bitarray()
    
    while(True):
        s = ser.read(14)
        dat.frombytes(s)
        #print(dat)
        new_dat = transform_data(dat)
        #print(new_dat)
        disp.update_data(new_dat)
        clear_term()
        disp.display()
        display_values(disp)
        #time.sleep(1)
	
    ser.close()
		

def main():
    print("Tenma 72-7735")

    disp = Tenma_72_7735_LCD_Display('0')

    print("")

    print("="*5)

    print("")

    dat = 14 * 4 * bitarray('1') # tous les bits à 1
    disp.update_data(dat)
    disp.display()
    print("")

    print("="*5)

    #dat = 14 * 4 * bitarray('0') # tous les bits à 0
    #dat = 14 * 4 * bitarray('1') # tous les bits à 1
    #print(dat)
    #disp.update_data(dat)

    #display_sample_raw(disp)
    #display_saved_data(disp)
    display_serial_data(disp)

    #display_values(disp)


if __name__ == '__main__':
    main()