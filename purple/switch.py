# Copyright (C) 2013 by Brian Neal.
# This file is part of purple, the PURPLE (Cipher Machine 97) simulation.
# purple is released under the MIT License (see LICENSE.txt).

"""This module contains the SteppingSwitch class and a factory function to
create the standard switches used on the PURPLE machine.

"""
import purple.data as data

# "Enum" to name the standard switches:
SIXES, TWENTIES_1, TWENTIES_2, TWENTIES_3 = range(4)


class SteppingSwitchError(Exception):
    """Exception class for all stepping switch errors"""


class SteppingSwitch:
    """This class simulates a stepping switch, the primary cryptographic element
    in the PURPLE cipher machine.

    """
    def __init__(self, wiring, init_pos=0):
        """Construct a SteppingSwitch from a wiring list, which must be a list
        of lists (one list per input level). Each inner list is a list of
        integers representing the output contacts. The initial position of the
        switch can also be set; this defaults to 0.

        The wiring lists are assumed to be 0-based.

        """
        self.wiring = wiring
        self.num_positions = len(wiring)
        self.num_levels = len(wiring[0])

        if not all(self.num_levels == len(level) for level in wiring):
            raise SteppingSwitchError("Ragged wiring table")

        self.set_pos(init_pos)

    def set_pos(self, pos):
        """Set the switch position to pos.
        Raises a SteppingSwitchError if pos is out of range.

        """
        if not (0 <= pos < self.num_positions):
            raise SteppingSwitchError("Illegal switch position")
        self.pos = pos

    def step(self):
        """Advance the stepping switch position.

        The new 0-based position of the switch is returned.

        """
        self.pos = (self.pos + 1) % self.num_positions
        return self.pos

    def __getitem__(self, level):
        """This method is how to determine the output signal from the stepping
        switch. The key parameter 'level' is the integer input level for the
        incoming signal. The integer outgoing contact level is returned.

        """
        return self.wiring[self.pos][level]


def create_switch(switch_type, init_pos=0):
    """Factory function for building a SteppingSwitch of the requested
    standard type. The initial position of the switch can be specified.

    The switch_type parameter must be one of the module level constants:
        * SIXES
        * TWENTIES_1
        * TWENTIES_2
        * TWENTIES_3

    A ValueError will be raised if switch_type is an illegal value.

    """
    wiring_map = {
        SIXES: data.SIXES_DATA,
        TWENTIES_1: data.TWENTIES_1_DATA,
        TWENTIES_2: data.TWENTIES_2_DATA,
        TWENTIES_3: data.TWENTIES_3_DATA,
    }
    wiring = wiring_map.get(switch_type)
    if not wiring:
        raise ValueError("illegal switch type")

    return SteppingSwitch(wiring, init_pos)
