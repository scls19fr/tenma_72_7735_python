#!/usr/bin/env python
# -*- coding: utf-8 -*-

import click

from bitarray import bitarray

def int2binstring(N, Nbits=8):
    if N<2**Nbits:
        return(bin(N)[2:].rjust(Nbits,'0'))
    else:
        raise(NotImplementedError)

@click.command()
@click.option('--filename', help="binary filename", default="reads.dat")
@click.option('--blocksize', help="blocksize", default=1024)
@click.option('--period', help="period", default=14)
def main(filename, blocksize, period):

    with open(filename, 'rb') as f:
    	block = f.read(blocksize)
        s_bin = ""
        s_hex = ""
        s_bin2 = ""
        for i, ch in enumerate(block):
            if (i % period) == 0:
                line_label = str(i/period + 1).rjust(3, '0')
                s_bin += line_label + ' : '
                s_hex += line_label + ' : '

            num = ord(ch)

            s_bin_num = int2binstring(num)
            s_bin += s_bin_num + " "
            s_hex += hex(num)[2:].upper() + " "
            s_bin2 += s_bin_num

            if (i % period) == period-1:
                s_bin += '\n'
                s_hex += '\n'
                print(bitarray(s_bin2))
                s_bin2 = ''

    	print s_hex
    	print s_bin

if __name__ == '__main__':
    main()