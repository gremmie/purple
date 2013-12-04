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
    def __init__(self, dec_wiring, enc_wiring=None, init_pos=0):
        """Construct a SteppingSwitch.

        dec_wiring is the decrypt wiring table, which must be a list
        of lists (one list per input level). Each inner list is a list of
        integers representing the output contacts.

        enc_wiring is the encrypt wiring table. If None, a reciprocal table is
        built from the dec_wiring parameter.

        init_pos is the initial position of the switch; this defaults to 0.

        """
        self.dec_wiring = dec_wiring
        self.num_positions = len(dec_wiring)
        self.num_levels = len(dec_wiring[0])

        if not all(self.num_levels == len(level) for level in self.dec_wiring):
            raise SteppingSwitchError("Invalid decrypt wiring dimensions")

        self.enc_wiring = (enc_wiring if enc_wiring else
                data.build_encrypt_wiring(dec_wiring))

        if self.num_positions != len(self.enc_wiring):
            raise SteppingSwitchError("Encrypt/Decrypt positions mismatch")

        if not all(self.num_levels == len(level) for level in self.enc_wiring):
            raise SteppingSwitchError("Invalid encrypt wiring dimensions")

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

    def decrypt(self, level):
        """This method is how to determine the output signal from the stepping
        switch for the decrypt path. The parameter 'level' is the integer input
        level for the incoming signal. The integer outgoing contact level is
        returned.

        """
        return self.dec_wiring[self.pos][level]

    def encrypt(self, level):
        """This method is how to determine the output signal from the stepping
        switch for the encrypt path. The parameter 'level' is the integer input
        level for the incoming signal. The integer outgoing contact level is
        returned.

        """
        return self.enc_wiring[self.pos][level]


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
    if switch_type not in [SIXES, TWENTIES_1, TWENTIES_2, TWENTIES_3]:
        raise ValueError("illegal switch type")

    return SteppingSwitch(dec_wiring=data.DECRYPT_DATA[switch_type],
            enc_wiring=data.ENCRYPT_DATA[switch_type],
            init_pos=init_pos)
