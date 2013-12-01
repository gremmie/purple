# Copyright (C) 2013 by Brian Neal.
# This file is part of purple, the PURPLE (Cipher Machine 97) simulation.
# purple is released under the MIT License (see LICENSE.txt).

import string
import unittest

from purple.machine import Purple97, Purple97Error
from purple.switch import SteppingSwitchError


class Purple97TestCase(unittest.TestCase):

    def test_construction(self):

        Purple97()
        Purple97([0, 1, 2, 3])
        Purple97([0, 1, 2, 3], 1)
        Purple97([0, 1, 2, 3], 2, 1)
        Purple97((0, 1, 2, 3), 2, 1, string.ascii_uppercase)
        Purple97((0, 1, 2, 3), 2, 1, string.ascii_lowercase)
        Purple97(alphabet=string.ascii_lowercase)
        Purple97(fast_switch=3, middle_switch=1)

    def test_construct_bad_positions(self):

        self.assertRaises(Purple97Error, Purple97, [])
        self.assertRaises(Purple97Error, Purple97, [1])
        self.assertRaises(Purple97Error, Purple97, [1, 1, 1, 1, 1])
        self.assertRaises(SteppingSwitchError, Purple97, [1, 1, 1, 100])

    def test_construct_bad_switches(self):

        self.assertRaises(Purple97Error, Purple97, fast_switch=0)
        self.assertRaises(Purple97Error, Purple97, fast_switch=4)
        self.assertRaises(Purple97Error, Purple97, fast_switch=-1)

        self.assertRaises(Purple97Error, Purple97, middle_switch=0)
        self.assertRaises(Purple97Error, Purple97, middle_switch=4)
        self.assertRaises(Purple97Error, Purple97, middle_switch=-1)

        self.assertRaises(Purple97Error, Purple97, fast_switch=2)
        self.assertRaises(Purple97Error, Purple97, fast_switch=1, middle_switch=1)
        self.assertRaises(Purple97Error, Purple97, fast_switch=2, middle_switch=2)
        self.assertRaises(Purple97Error, Purple97, fast_switch=3, middle_switch=3)

        self.assertRaises(Purple97Error, Purple97, fast_switch=0, middle_switch=1)
        self.assertRaises(Purple97Error, Purple97, fast_switch=0, middle_switch=0)
        self.assertRaises(Purple97Error, Purple97, fast_switch=0, middle_switch=4)

    def test_construct_bad_alphabet(self):

        alpha = ''
        self.assertRaises(Purple97Error, Purple97, alphabet=alpha)
        alpha = '1'
        self.assertRaises(Purple97Error, Purple97, alphabet=alpha)
        alpha = '!' * 26
        self.assertRaises(Purple97Error, Purple97, alphabet=alpha)
        alpha = string.ascii_uppercase[3:]
        self.assertRaises(Purple97Error, Purple97, alphabet=alpha)
        alpha = string.ascii_uppercase + string.ascii_uppercase[4:10]
        self.assertRaises(Purple97Error, Purple97, alphabet=alpha)
        alpha = string.ascii_uppercase[:13] + string.ascii_uppercase[:13]
        self.assertRaises(Purple97Error, Purple97, alphabet=alpha)
        alpha = 'M' * 26
        self.assertRaises(Purple97Error, Purple97, alphabet=alpha)

    def test_from_key_sheet(self):

        Purple97.from_key_sheet('9-1,2,3-23')
        Purple97.from_key_sheet('1-1,1,1-13')
        Purple97.from_key_sheet('25-25,25,25-31')
        Purple97.from_key_sheet('5-20,7,18-21', alphabet=string.ascii_uppercase)

    def test_bad_from_key_sheet(self):

        self.assertRaises(SteppingSwitchError, Purple97.from_key_sheet, '0-1,2,3-13')
        self.assertRaises(SteppingSwitchError, Purple97.from_key_sheet, '26-1,2,3-13')
        self.assertRaises(SteppingSwitchError, Purple97.from_key_sheet, '1-1,0,3-13')
        self.assertRaises(SteppingSwitchError, Purple97.from_key_sheet, '1-1,2,26-13')
        self.assertRaises(SteppingSwitchError, Purple97.from_key_sheet, '1-1,2,26-03')
        self.assertRaises(SteppingSwitchError, Purple97.from_key_sheet, '1-1,2,26-00')
        self.assertRaises(SteppingSwitchError, Purple97.from_key_sheet, '1-1,2,26-14')

        self.assertRaises(Purple97Error, Purple97.from_key_sheet, 'bad string')
        self.assertRaises(Purple97Error, Purple97.from_key_sheet, '1-2-1,2,26-14')
        self.assertRaises(Purple97Error, Purple97.from_key_sheet, 'a-9,2,20-13')
        self.assertRaises(Purple97Error, Purple97.from_key_sheet, '1-a,2,20-13')
        self.assertRaises(Purple97Error, Purple97.from_key_sheet, '1-9,a,20-13')
        self.assertRaises(Purple97Error, Purple97.from_key_sheet, '1-9,2,a-13')
        self.assertRaises(Purple97Error, Purple97.from_key_sheet, '1-9,2,20-a3')
        self.assertRaises(Purple97Error, Purple97.from_key_sheet, '1-9,2,20-1a')
        self.assertRaises(Purple97Error, Purple97.from_key_sheet, '1-9,2,20-123')
