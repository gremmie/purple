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
        self.assertRaises(SteppingSwitchError, SteppingSwitch, bad_wiring,
                init_pos=0)
        self.assertRaises(SteppingSwitchError, SteppingSwitch, good_wiring,
                init_pos=-1)
        self.assertRaises(SteppingSwitchError, SteppingSwitch, good_wiring,
                init_pos=3)
        self.assertRaises(SteppingSwitchError, SteppingSwitch, bad_wiring,
                init_pos=3)

    def test_wiring_table_mismatch_in_dimensions(self):

        wiring_1 = [
            [1, 2, 0],
            [2, 1, 0],
            [0, 1, 2],
        ]
        wiring_2 = [
            [1, 2, 3, 0],
            [1, 2, 3, 0],
            [1, 2, 3, 0],
        ]
        wiring_3 = [
            [1, 2, 3, 0],
            [1, 2, 3, 0],
            [1, 2, 3, 0],
            [1, 2, 3, 0],
        ]
        bad_wiring = [
            [1, 2, 0],
            [2, 1],
            [0, 1, 2]
        ]
        self.assertRaises(SteppingSwitchError, SteppingSwitch, wiring_1,
                wiring_2)
        self.assertRaises(SteppingSwitchError, SteppingSwitch, wiring_2,
                wiring_1)
        self.assertRaises(SteppingSwitchError, SteppingSwitch, wiring_1,
                bad_wiring)
        self.assertRaises(SteppingSwitchError, SteppingSwitch, wiring_2,
                wiring_3)
        self.assertRaises(SteppingSwitchError, SteppingSwitch, wiring_3,
                wiring_2)

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

    def test_decrypt(self):

        switch = create_switch(purple.switch.SIXES)
        switch.set_pos(0)
        self.assertEqual(switch.decrypt(0), 1)
        self.assertEqual(switch.decrypt(1), 0)
        self.assertEqual(switch.decrypt(2), 2)
        self.assertEqual(switch.decrypt(3), 4)
        self.assertEqual(switch.decrypt(4), 3)
        self.assertEqual(switch.decrypt(5), 5)

        switch.step()
        self.assertEqual(switch.decrypt(0), 5)
        self.assertEqual(switch.decrypt(1), 2)
        self.assertEqual(switch.decrypt(2), 4)
        self.assertEqual(switch.decrypt(3), 1)
        self.assertEqual(switch.decrypt(4), 0)
        self.assertEqual(switch.decrypt(5), 3)

        switch.set_pos(24)
        self.assertEqual(switch.decrypt(0), 4)
        self.assertEqual(switch.decrypt(1), 1)
        self.assertEqual(switch.decrypt(2), 3)
        self.assertEqual(switch.decrypt(3), 2)
        self.assertEqual(switch.decrypt(4), 5)
        self.assertEqual(switch.decrypt(5), 0)

    def test_encrypt(self):

        switch = create_switch(purple.switch.SIXES)
        switch.set_pos(0)
        self.assertEqual(switch.encrypt(0), 1)
        self.assertEqual(switch.encrypt(1), 0)
        self.assertEqual(switch.encrypt(2), 2)
        self.assertEqual(switch.encrypt(3), 4)
        self.assertEqual(switch.encrypt(4), 3)
        self.assertEqual(switch.encrypt(5), 5)

        switch.step()
        self.assertEqual(switch.encrypt(0), 4)
        self.assertEqual(switch.encrypt(1), 3)
        self.assertEqual(switch.encrypt(2), 1)
        self.assertEqual(switch.encrypt(3), 5)
        self.assertEqual(switch.encrypt(4), 2)
        self.assertEqual(switch.encrypt(5), 0)

        switch.set_pos(24)
        self.assertEqual(switch.encrypt(0), 5)
        self.assertEqual(switch.encrypt(1), 1)
        self.assertEqual(switch.encrypt(2), 3)
        self.assertEqual(switch.encrypt(3), 2)
        self.assertEqual(switch.encrypt(4), 0)
        self.assertEqual(switch.encrypt(5), 4)

    def test_bad_create_switch(self):

        self.assertRaises(ValueError, create_switch, -1)
        self.assertRaises(ValueError, create_switch, 4)
        self.assertRaises(ValueError, create_switch, 99)
