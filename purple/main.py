# Copyright (C) 2013 by Brian Neal.
# This file is part of purple, the PURPLE (Cipher Machine 97) simulation.
# purple is released under the MIT License (see LICENSE.txt).

"""This file contains the main routine for the command-line purple97 program."""

import argparse
import os
import string
import sys

from purple.machine import Purple97, Purple97Error
from purple.switch import SteppingSwitchError


DESC = """PURPLE cipher machine simulator"""

EPILOG = """\
Supply either -e or -d, but not both, to perform either an encrypt or decrypt. If
the -s option is not supplied, the value of the environment variable
PURPLE97_SWITCHES will be used. If the -a option is not supplied, the value of
the environment variable PURPLE97_ALPHABET will be used. Input text is supplied
either by the -t or by the -f options, but not both.
"""

DEFAULT_SWITCHES = '1-1,1,1-12'
DEFAULT_ALPHABET = Purple97.STRAIGHT_PLUGBOARD

LOWERCASE = set(string.ascii_lowercase)
DIGITS = {
    '0': 'ZERO',
    '1': 'ONE',
    '2': 'TWO',
    '3': 'THREE',
    '4': 'FOUR',
    '5': 'FIVE',
    '6': 'SIX',
    '7': 'SEVEN',
    '8': 'EIGHT',
    '9': 'NINE',
}


def filter_plaintext(source):
    """A generator to filter plaintext to ensure only valid input is fed to
    the purple cipher machine:

        * Uppercase letters A-Z are passed unchanged
        * Lowercase letters a-z are converted to uppercase
        * Digits are converted to words; e.g. 1 => ONE
        * All other input is ignored (filtered out)

    source can be anything that yields a line of text at a time.

    """
    for line in source:
        for c in line:
            if c in Purple97.VALID_KEYS:
                yield c
            elif c in LOWERCASE:
                yield c.upper()
            else:
                digit_name = DIGITS.get(c)
                if digit_name:
                    for d in digit_name:
                        yield d


def filter_whitespace(source):
    """A generator to filter out whitespace from text read from
    a file-like source.

    """
    for line in source:
        for c in line:
            if not c.isspace():
                yield c


def main(argv=None):
    """Entry point for the command-line purple97 simulation."""

    parser = argparse.ArgumentParser(description=DESC, epilog=EPILOG)
    parser.add_argument('-e', '--encrypt', action='store_true',
        help='encrypt text from files or the command-line')
    parser.add_argument('-d', '--decrypt', action='store_true',
        help='decrypt text from files or the command-line')
    parser.add_argument('-f', '--filter', action='store_true',
        help='filter plaintext and provide useful substitutions')
    parser.add_argument('-s', '--switches',
        help='switch settings, e.g. 9-1,24,6-23')
    parser.add_argument('-a', '--alphabet',
        help='plugboard wiring string, 26-letters')
    parser.add_argument('-t', '--text',
        help='input text to encrypt/decrypt')
    parser.add_argument('-i', '--input', metavar='FILE',
        help='file to read input text from, - for stdin')

    args = parser.parse_args(args=argv)

    if not args.encrypt and not args.decrypt:
        parser.print_help()
        parser.exit(1)
    if args.encrypt and args.decrypt:
        parser.error("Please supply either -e or -d, not both")
    if args.text and args.file:
        parser.error("Please supply either -t or -i, not both")
    if args.decrypt and args.filter:
        parser.error("The -f option only works with -e (encrypt)")

    # Get key settings
    if args.switches:
        switches = args.switches
    else:
        switches = os.environ.get('PURPLE97_SWITCHES', DEFAULT_SWITCHES)

    if args.alphabet:
        alphabet = args.alphabet
    else:
        alphabet = os.environ.get('PURPLE97_ALPHABET', DEFAULT_ALPHABET)

    # Create purple cipher machine object
    try:
        purple = Purple97.from_key_sheet(switches, alphabet)
    except (Purple97Error, SteppingSwitchError) as ex:
        parser.error(str(ex))


    if args.file:
        try:
            fp = sys.stdin if args.file == '-' else open(args.file, 'r')
        except IOError as ex:
            raise SystemExit(str(ex))

    if args.encrypt:
        action = purple.encrypt

        source = [args.text] if args.text else fp
        source = (filter_plaintext(source) if args.filter else
                                    filter_whitespace(source))
    else:
        action = purple.decrypt
        source = [args.text] if args.text else fp
        source = filter_whitespace(source)

    try:
        result = action(source)
    except (Purple97Error, SteppingSwitchError) as ex:
        parser.error(str(ex))

    print(result)


if __name__ == '__main__':
    main()
