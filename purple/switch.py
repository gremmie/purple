# Copyright (C) 2013 by Brian Neal.
# This file is part of purple, the PURPLE (Cipher Machine 97) simulation.
# purple is released under the MIT License (see LICENSE.txt).

"""This module contains the SteppingSwitch class."""


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
        self.pos = init_pos

        if not all(self.num_levels == len(level) for level in wiring):
            raise SteppingSwitchError("Ragged wiring table")

        if not (0 <= self.pos < self.num_positions):
            raise SteppingSwitchError("Illegal initial position")

    def step(self):
        """Advance the stepping switch position."""
        self.pos = (self.pos + 1) % self.num_positions

    def __getitem__(self, level):
        """This method is how to determine the output signal from the stepping
        switch. The key parameter 'level' is the integer input level for the
        incoming signal. The integer outgoing contact level is returned.

        """
        return self.wiring[self.pos][level]
