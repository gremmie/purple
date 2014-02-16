# Copyright (C) 2013 - 2014 by Brian Neal.
# This file is part of purple, the PURPLE (Cipher Machine 97) simulation.
# purple is released under the MIT License (see LICENSE.txt).

"""This module contains the Purple97 class, the top level class in the PURPLE
simulation.

The reference for this simulation is the paper "PURPLE Revealed: Simulation and
Computer-aided Cryptanalysis of Angooki Taipu B", by Wes Freeman, Geoff
Sullivan, and Frode Weierud. This paper was published in Cryptologia, Volume 27,
Issue 1, January, 2003, pp. 1-43.

The paper is also available at:
http://cryptocellar.web.cern.ch/cryptocellar/pubs/PurpleRevealed.pdf

"""
from collections import Counter
import string

import purple.switch as switch


class Purple97Error(Exception):
    """Exception class for all Purple97 errors"""


class Purple97:
    """This class simulates the top-level behavior of the PURPLE cipher
    machine.

    """
    VALID_KEYS = set(string.ascii_uppercase)
    STRAIGHT_PLUGBOARD = 'AEIOUYBCDFGHJKLMNPQRSTVWXZ'

    def __init__(self, switches_pos=None, fast_switch=1, middle_switch=2,
            alphabet=None):
        """Build a PURPLE (Cipher Machine 97) instance. Initial settings can be
        optionally supplied.

        switches_pos: If not None, must be a 4-element list or tuple of integer
        starting switch positions. Each position must be in the range of 0-24,
        inclusive. If None, a list of all 0's is assumed. The first element in
        the list is the starting position for the sixes switch. The second
        through fourth elements are the starting positions for the three
        twenties switches, 1 through 3.

        fast_switch: this integer parameter names which twenties switch (1-3) is
        assuming the role of the fast switch.

        middle_switch: this integer parameter names which twenties switch (1-3)
        has been designated as the middle switch.

        Passing in the same value for both the fast and medium switches will
        raise a Purple97Error exception. The slow switch is assumed to be the
        remaining twenties switch that was not named.

        alphabet: this parameter must be a 26-letter sequence that represents
        the daily alphabet setting. It describes how the typewriters are wired
        to the plugboard. The first six characters are the mapping for the sixes
        switch, and the remaining 20 are for the input wiring for the first
        stage of the twenties switches. If None is supplied, a straight through
        mapping is assumed; i.e. STRAIGHT_PLUGBOARD.

        The alphabet parameter will accept either upper or lowercase letters.
        All 26 distinct letters must be present or else a Purple97Error
        exception will be raised.

        """
        # If no switch positions are supplied, default to all 0's
        if switches_pos is None:
            switches_pos = (0, 0, 0, 0)

        # Validate switch positions
        try:
            n = len(switches_pos)
        except TypeError:
            raise Purple97Error("switches_pos must be a sequence")
        if n != 4:
            raise Purple97Error("switches_pos must have length of 4")

        # Create switches with correct starting positions
        self.sixes = switch.create_switch(switch.SIXES, switches_pos[0])
        self.twenties = [
            switch.create_switch(switch.TWENTIES_1, switches_pos[1]),
            switch.create_switch(switch.TWENTIES_2, switches_pos[2]),
            switch.create_switch(switch.TWENTIES_3, switches_pos[3]),
        ]

        # Validate fast & middle switch parameters
        if not (1 <= fast_switch <= 3):
            raise Purple97Error("fast_switch out of range (1-3)")
        if not (1 <= middle_switch <= 3):
            raise Purple97Error("middle_switch out of range (1-3)")
        if fast_switch == middle_switch:
            raise Purple97Error("fast & middle switches cannot be the same")

        # Store references to the fast, middle, and slow switches
        self.fast_switch = self.twenties[fast_switch - 1]
        self.middle_switch = self.twenties[middle_switch - 1]

        # Pick the remaining switch as the slow switch
        switches = [1, 2, 3]
        switches.remove(fast_switch)
        switches.remove(middle_switch)
        self.slow_switch = self.twenties[switches[0] - 1]

        # Validate the alphabet
        if alphabet is None:
            alphabet = self.STRAIGHT_PLUGBOARD

        if len(alphabet) != 26:
            raise Purple97Error("invalid alphabet length")
        alphabet = alphabet.upper()

        # Count valid letters
        ctr = Counter(string.ascii_uppercase)
        for c in alphabet:
            if c in ctr:
                ctr[c] += 1

        # At this point if alphabet is legal, all keys in ctr must have a value
        # of 2. If any are 1, then alphabet was missing some letters. If any are
        # greater than 2, we had duplicate letters.

        if not all(v == 2 for v in ctr.values()):
            raise Purple97Error("invalid alphabet")

        self.alphabet = alphabet
        self.plugboard = {c : n for n, c in enumerate(alphabet)}

    @classmethod
    def from_key_sheet(cls, switches, alphabet=None):
        """This class method allows one to construct a Purple97 using
        a shorthand notation used by US codebreakers.

        switches: must be a string of the form 'a-b,c,d-ef' where
            a - starting position of the sixes switch (1-25)
            b - starting position of the twenties switch #1 (1-25)
            c - starting position of the twenties switch #2 (1-25)
            d - starting position of the twenties switch #3 (1-25)
            e - which switch is the fast switch (1-3)
            f - which switch is the middle switch (1-3)

        Example: '9-1,24,6-23'

        Note that the starting positions here are 1-based since that is the
        notation the US codebreakers seemed to have used.

        alphabet: the daily alphabet, same format as in the __init__ function

        """
        try:
            sixes, twenties, speed = switches.split('-')
        except ValueError:
            raise Purple97Error('invalid switches string (-)')

        twenties = twenties.split(',')
        if len(twenties) != 3:
            raise Purple97Error('invalid twenties position')

        try:
            switches_pos = [int(s) - 1 for s in [sixes] + twenties]
        except ValueError:
            raise Purple97Error('switch positions must be numeric')

        if len(speed) != 2:
            raise Purple97Error('invalid switch speed settings')

        try:
            fast_switch, middle_switch = int(speed[0]), int(speed[1])
        except ValueError:
            raise Purple97Error('switch speed settings must be numeric')

        return cls(switches_pos, fast_switch, middle_switch, alphabet)

    def decrypt(self, ciphertext):
        """Decrypts the given ciphertext message and returns the plaintext
        output.

        ciphertext must contain only the letters A-Z or '-' or else a
        Purple97Error exception is raised. A '-' is used to indicate a garble.
        When a '-' is encountered, a '-' is added to the plaintext output and
        the machine is stepped.

        """
        plaintext = []
        for i, c in enumerate(ciphertext):

            # Process a garble:
            if c == '-':
                plaintext.append('-')
                self.step()
                continue

            if c not in self.VALID_KEYS:
                raise Purple97Error("invalid input '{}' to decrypt".format(c))

            n = self.plugboard[c]

            if n < 6:
                # This input goes to the sixes switch
                x = self.sixes.decrypt(n)
            else:
                # This input goes to the chain of twenties switches
                n -= 6
                x = self.twenties[0].decrypt(self.twenties[1].decrypt(
                        self.twenties[2].decrypt(n)))
                x += 6

            plaintext.append(self.alphabet[x])

            # Now step the switches.
            self.step()

        return ''.join(plaintext)

    def encrypt(self, plaintext):
        """Encrypts the given plaintext message and returns the ciphertext
        output.

        plaintext must contain only the letters A-Z or else a Purple97Error
        exception is raised.

        """
        ciphertext = []
        for c in plaintext:
            if c not in self.VALID_KEYS:
                raise Purple97Error("invalid input '{}' to encrypt".format(c))

            n = self.plugboard[c]
            if n < 6:
                # This input goes to the sixes switch
                x = self.sixes.encrypt(n)
            else:
                # This input goes to the chain of twenties switches in reverse
                # order compared to decrypt.
                n -= 6
                x = self.twenties[2].encrypt(self.twenties[1].encrypt(
                        self.twenties[0].encrypt(n)))
                x += 6

            ciphertext.append(self.alphabet[x])

            # Now step the switches.
            self.step()

        return ''.join(ciphertext)

    def step(self):
        """Step the stepping switches."""
        # First read the sixes and middle switch
        # positions before stepping anything. Use these latched values in
        # the decision processes for stepping a twenties. This is crucial!
        sixes_pos = self.sixes.pos
        middle_pos = self.middle_switch.pos

        # Now we can step the sixes. It unconditionally steps after every
        # letter is processed.
        self.sixes.step()

        # Only 1 twenties switch steps at a time.
        #
        # Normally the fast switch advances every letter.
        #
        # However if the sixes is at the last position (24), the middle
        # switch steps instead.
        #
        # But if the sixes is at the second to last position (23) and the middle
        # switch is at the last position (24), the slow switch will step.  The
        # middle switch will step on the next letter in this case.

        if sixes_pos == 23 and middle_pos == 24:
            self.slow_switch.step()
        elif sixes_pos == 24:
            self.middle_switch.step()
        else:
            self.fast_switch.step()
