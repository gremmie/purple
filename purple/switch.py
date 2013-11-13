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

        """
        self.wiring = wiring
        self.num_contacts = len(wiring)
        self.num_levels = len(wiring[0])
        self.pos = init_pos

        if not all(self.num_levels == len(level) for level in wiring):
            raise SteppingSwitchError("Ragged wiring table")

        if not (0 <= self.pos < self.num_contacts):
            raise SteppingSwitchError("Illegal initial position")

    def step(self):
        """Advance the stepping switch position."""
        self.pos = (self.pos + 1) % self.num_contacts

    def __getitem__(self, level):
        """This method is how to determine the output signal from the stepping
        switch. The key parameter 'level' is the integer input level for the
        incoming signal. The integer outgoing contact level is returned.

        """
        return self.wiring[self.pos][level]


SIXES_DATA = [
    [2, 1, 3, 5, 4, 6],
    [6, 3, 5, 2, 1, 4],
    [1, 5, 4, 6, 2, 3],
    [4, 3, 2, 1, 6, 5],
    [3, 6, 1, 4, 5, 2],
    [2, 1, 6, 5, 3, 4],
    [6, 5, 4, 2, 1, 3],
    [3, 6, 1, 4, 5, 2],
    [5, 4, 2, 6, 3, 1],
    [4, 5, 3, 2, 1, 6],
    [2, 1, 4, 5, 6, 3],
    [5, 4, 6, 3, 2, 1],
    [3, 1, 2, 6, 4, 5],
    [4, 2, 5, 1, 3, 6],
    [1, 6, 2, 3, 5, 4],
    [5, 4, 3, 6, 1, 2],
    [6, 2, 5, 3, 4, 1],
    [2, 3, 4, 1, 5, 6],
    [1, 2, 3, 5, 6, 4],
    [3, 1, 6, 4, 2, 5],
    [6, 5, 1, 2, 4, 3],
    [1, 3, 6, 4, 2, 5],
    [6, 4, 5, 1, 3, 2],
    [4, 6, 1, 2, 5, 3],
    [5, 2, 4, 3, 6, 1],
]
