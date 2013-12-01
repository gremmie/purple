# Copyright (C) 2013 by Brian Neal.
# This file is part of purple, the PURPLE (Cipher Machine 97) simulation.
# purple is released under the MIT License (see LICENSE.txt).

import unittest

from purple.switch import SteppingSwitch, SteppingSwitchError, create_switch
import purple.switch


class SwitchTestCase(unittest.TestCase):

    def test_construction(self):

        bad_wiring = [
            [1, 2, 0],
            [2, 1],
            [0, 1, 2]
        ]
        good_wiring = [
            [1, 2, 0],
            [2, 1, 0],
            [0, 1, 2]
        ]
        self.assertRaises(SteppingSwitchError, SteppingSwitch, bad_wiring)
        self.assertRaises(SteppingSwitchError, SteppingSwitch, bad_wiring, 0)
        self.assertRaises(SteppingSwitchError, SteppingSwitch, good_wiring, -1)
        self.assertRaises(SteppingSwitchError, SteppingSwitch, good_wiring, 3)
        self.assertRaises(SteppingSwitchError, SteppingSwitch, bad_wiring, 3)

    def test_bad_set_pos(self):

        switch = create_switch(purple.switch.SIXES)
        self.assertRaises(SteppingSwitchError, switch.set_pos, -1)
        self.assertRaises(SteppingSwitchError, switch.set_pos, 25)
        self.assertRaises(SteppingSwitchError, switch.set_pos, 26)

    def test_set_pos(self):

        switch = create_switch(purple.switch.SIXES)
        for pos in range(25):
            switch.set_pos(pos)

    def test_step(self):

        switch = create_switch(purple.switch.SIXES)
        for n in range(25 * 2 + 1):
            pos = n % 25
            self.assertEqual(switch.pos, pos)
            new_pos = switch.step()
            self.assertEqual((pos + 1) % 25, new_pos)

    def test_output(self):

        switch = create_switch(purple.switch.SIXES)
        switch.set_pos(0)
        self.assertEqual(switch[0], 1)
        self.assertEqual(switch[1], 0)
        self.assertEqual(switch[2], 2)
        self.assertEqual(switch[3], 4)
        self.assertEqual(switch[4], 3)
        self.assertEqual(switch[5], 5)

        switch.step()
        self.assertEqual(switch[0], 5)
        self.assertEqual(switch[1], 2)
        self.assertEqual(switch[2], 4)
        self.assertEqual(switch[3], 1)
        self.assertEqual(switch[4], 0)
        self.assertEqual(switch[5], 3)

        switch.set_pos(24)
        self.assertEqual(switch[0], 4)
        self.assertEqual(switch[1], 1)
        self.assertEqual(switch[2], 3)
        self.assertEqual(switch[3], 2)
        self.assertEqual(switch[4], 5)
        self.assertEqual(switch[5], 0)

    def test_bad_create_switch(self):

        self.assertRaises(ValueError, create_switch, -1)
        self.assertRaises(ValueError, create_switch, 4)
        self.assertRaises(ValueError, create_switch, 99)
