#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Generate (or parse) 7 segment display characters

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

__author__ = 'Sébastien Celles <s.celles@gmail.com>'
__date__ = '$Date: 2014/10/03 09:06:00 $'
__version__ = '$Revision: 0.1 $'

from bitarray import bitarray

class SevenSegmentsChar():
    def __init__(self, s_bits, character):
        self.a_bit = bitarray(s_bits)
        self.character = character

class SevenSegmentsDisplay():
    d_7_segments_bin_char = {}
    d_7_segments_char_bin = {}

    def __init__(self):
        self._append(SevenSegmentsChar('0000000', ' '))
        self._append(SevenSegmentsChar('1111110', '0'))
        self._append(SevenSegmentsChar('0110000', '1'))
        self._append(SevenSegmentsChar('1101101', '2'))
        self._append(SevenSegmentsChar('1111001', '3'))
        self._append(SevenSegmentsChar('0110011', '4'))
        self._append(SevenSegmentsChar('1011011', '5'))
        self._append(SevenSegmentsChar('1011111', '6'))
        self._append(SevenSegmentsChar('1110000', '7'))
        self._append(SevenSegmentsChar('1111111', '8'))
        self._append(SevenSegmentsChar('1111011', '9'))
        self._append(SevenSegmentsChar('1110111', 'A'))
        self._append(SevenSegmentsChar('0011111', 'B'))
        self._append(SevenSegmentsChar('1100110', 'C'))
        self._append(SevenSegmentsChar('0111101', 'D'))
        self._append(SevenSegmentsChar('1001111', 'E'))
        self._append(SevenSegmentsChar('1000111', 'F'))

    def _append(self, seven_segs_char):
        self.d_7_segments_char_bin[seven_segs_char.character] = seven_segs_char.a_bit
        self.d_7_segments_bin_char[seven_segs_char.a_bit.tobytes()] = seven_segs_char.character

    def bitarray(self, character):
        return(self.d_7_segments_char_bin[character])

    def character(self, a_bit):
        return(self.d_7_segments_bin_char[a_bit.tobytes()])
