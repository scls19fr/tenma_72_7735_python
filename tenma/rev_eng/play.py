#!/usr/bin/env python
# -*- coding: utf-8 -*-

import click
import time
from bitarray import bitarray

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

#def transform_data(dat):
#    length = 4
#    offset = 4
#    new_dat = bitarray()
#    for seg in range(14):
#        dat_part = dat[seg*8+offset:seg*8+offset+length]
#        dat_part.reverse()
#        new_dat += dat_part
#    return(new_dat)

def transform_data(dat):
    new_dat = bitarray()
    dat.reverse()
    length = 4
    offset = 0
    for seg in range(13,-1,-1):
        dat_part = dat[seg*8+offset:seg*8+offset+length]
        print(dat_part)
        new_dat += dat_part
    return(new_dat)

@click.command()
@click.option('--filename', help="binary filename", default="reads.dat")
@click.option('--blocksize', help="blocksize", default=1024)
@click.option('--period', help="period", default=14)
def main(filename, blocksize, period):
    for data in play_data(filename, blocksize, period):
        print(data)
        new_data = transform_data(data)
        print(new_data)
        time.sleep(1)


if __name__ == '__main__':
    main()