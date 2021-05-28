#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Nosetest for seven_segments.py
Generate (or parse) 7 segment display characters
$ nosetests -v --nocapture

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

"""

from seven_segments import SevenSegmentsDisplay
from bitarray import bitarray

def test_8_to_bitarray():
    seven_segments_disp = SevenSegmentsDisplay()
    assert(seven_segments_disp.bitarray('8')==bitarray('1111111'))

def test_0_to_bitarray():
    seven_segments_disp = SevenSegmentsDisplay()
    assert(seven_segments_disp.bitarray('0')==bitarray('1111110'))

def test_read_bitarray_8():
    seven_segments_disp = SevenSegmentsDisplay()
    assert(seven_segments_disp.character(bitarray('1111111'))=='8')

def test_read_bitarray_0():
    seven_segments_disp = SevenSegmentsDisplay()
    assert(seven_segments_disp.character(bitarray('1111110'))=='0')

def test_read_bitarray_A():
    seven_segments_disp = SevenSegmentsDisplay()
    assert(seven_segments_disp.character(bitarray('1110111'))=='A')
