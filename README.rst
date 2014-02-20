======
Purple
======

A historically accurate PURPLE simulator written in Python 3
------------------------------------------------------------

:Author: Brian Neal <bgneal@gmail.com>
:Version: 0.1
:Date: February 17, 2013
:Home Page: https://bitbucket.org/bgneal/purple/
:License: MIT License (see LICENSE.txt)
:Documentation: This file
:Support: https://bitbucket.org/bgneal/purple/issues

``Purple`` is a Python library and command-line utility for simulating the
`PURPLE Machine`_, a cipher machine used by the Japanese Foreign Office before
and during the Second World War. PURPLE was the code name given to the machine
by U.S.  cryptanalysts. The Japanese called the machine *97-shiki ōbun inji-ki*
(System 97 Printing Machine for European Characters), and *Angōki B-kata* (Type
B Cipher Machine). The machine was used for secure diplomatic communications
and was implemented as an electromechanical stepping-switch device.

This project is a Python 3 library and command-line utility for encrypting and
decrypting text by simulating the operation of an actual PURPLE machine.

If you are brand new to the ``Purple`` cipher machine, please skip down to the
references section and familiarize yourself with the device. This will help you
understand the terminology used in the documentation, below.


Requirements
############

``Purple`` was written in Python_ 3, specifically 3.3.2, and has no other external
dependencies.


Installation
############

``Purple`` is available on the `Python Package Index`_ (PyPI). There are
a number of ways to install to ``Purple``, detailed below. The author
recommends you install into a virtualenv_. Setting up a virtualenv is not hard,
but describing it is out of scope for this document. Please see the virtualenv_
documentation for more information.

You can install it using pip_::

   $ pip install purple                # install
   $ pip install --upgrade purple      # upgrade

You can also visit the the `Purple Bitbucket page`_ and download an archive
file of the latest code. Alternatively, if you use Mercurial_, you can clone
the repository with the following command::

   $ hg clone https://bitbucket.org/bgneal/purple

If you did not use pip_ (you downloaded or cloned the code yourself), you can
install with::

   $ cd where-you-extracted-purple
   $ python setup.py install

To run the unit tests::

   $ cd where-you-extracted-purple
   $ python -m unittest discover


Initial Settings Syntax
#######################

In order to exchange messages, each message recipient must use the same initial
machine settings. For the ``Purple`` machine, these settings are the initial
switch positions for the "sixes" and three "twenties" stepping switches, the
switch motion order (which twenties switch is the fast switch, which is the
middle switch, and which is the slow switch), and finally the plugboard
alphabet mapping.

The ``Purple`` simulation uses the following syntax in both its command-line
application and library code.

For the switches, we borrow the notation used by U.S. cryptanalysts, for
example::

   9-1,24,6-23

Here the first number before leading dash, 9, indicates the starting position
of the sixes switch. The next three numbers are the starting positions for the
three twenties switches numbered 1, 2, and 3. Each switch position is a number
from 1 through 25, inclusive. Finally, after the last dash are two digits which
indicate the switch stepping motion. The first number, in this case 2,
indicates that the twenties switch #2 is the fast switch. The second number, 3,
indicates twenties switch #3 is the middle switch. Thus the slow switch, which
is never listed, is in this case twenties switch #1. When using this syntax, do
not insert space characters.

The plugboard alphabet setting describes how the input typewriters are wired to
the plugboard. We represent this setting as a string of the 26 uppercase
alphabet letters where the first six letters are the wiring to the sixes
switch, and the remaining 20 are wired to the first stage of the twenties
switches. For example::

   AEIOUYBCDFGHJKLMNPQRSTVWXZ

For the alphabet setting to be valid, do not insert spaces, and ensure all 26
letters are used exactly once.


Command-line Usage
##################

To get help on the command-line ``Purple`` utility, execute the ``purple``
command with the ``--help`` option::

   $ purple --help
   usage: purple [-h] [-e] [-d] [-f] [-s SWITCHES] [-a ALPHABET] [-t TEXT]
                 [-i FILE] [-g N] [-w N]

   PURPLE cipher machine simulator

   optional arguments:
     -h, --help            show this help message and exit
     -e, --encrypt         perform an encrypt operation
     -d, --decrypt         perform a decrypt operation
     -f, --filter          filter plaintext and provide useful substitutions
     -s SWITCHES, --switches SWITCHES
                           switch settings, e.g. 9-1,24,6-23
     -a ALPHABET, --alphabet ALPHABET
                           plugboard wiring string, 26-letters; e.g.
                           AEIOUYBCDFGHJKLMNPQRSTVWXZ
     -t TEXT, --text TEXT  input text to encrypt/decrypt
     -i FILE, --input FILE
                           file to read input text from, - for stdin
     -g N, --group N       if non-zero, group output in N-letter groups [default:
                           5]
     -w N, --width N       wrap output text to N letters; a value of 0 means do
                           not wrap [default: 70]

   Supply either -e or -d, but not both, to perform either an encrypt or decrypt.
   If the -s option is not supplied, the value of the environment variable
   PURPLE97_SWITCHES will be used. If the -a option is not supplied, the value of
   the environment variable PURPLE97_ALPHABET will be used. Input text is
   supplied either by the -t or by the -f options, but not both.

The ``purple`` command operates in two modes, either encrypt (specified with
``-e`` or ``--encrypt``) or decrypt (``-d`` or ``--decrypt``). Input text can
be specified on the command-line with the ``-t`` or ``--text`` option, or
a read from a file (``-i`` or ``--input``).

The ``-s`` (or ``--switches``) and ``-a`` (or ``--alphabet``) settings
determine the initial machine settings. They use the syntax described above in
the Initial Settings Syntax section.

If you are going to be working with the same initial switch settings and
plugboard alphabet over many command invocations it may be more convenient to
specify them as environment variables instead of repeatedly using the
command-line arguments. The examples below assume these statements have been
executed::

   $ export PURPLE97_SWITCHES=9-1,24,6-23
   $ export PURPLE97_ALPHABET=NOKTYUXEQLHBRMPDICJASVWGZF

If you do not specify initial settings, the ``purple`` machine will attempt to
read them from these two environment variables. Failing that, ``purple`` will
use the following initial settings:

* default switch settings: 1-1,1,1-12
* default alphabet: AEIOUYBCDFGHJKLMNPQRSTVWXZ

When encrypting text, the ``purple`` machine only accepts the letters A-Z, but
also allows for "garble" letters to be indicated by using the ``-`` (dash)
character. This means all punctuation and spaces must be either be omitted or
input via some other convention. The ``-f`` or ``--filter`` flag, when present,
relaxes these restrictions a bit. When this flag is on, all lowercase letters
will be converted to uppercase, digits will be converted to words (e.g.
5 becomes FIVE), and all other characters will be ignored.

A simple encrypt example using the ``-f`` flag is given below::

   $ purple --encrypt -t "The PURPLE machine is now online" -f
   OGIVT SIAAH MWMHT VIBYY JUOJF UE

By default ``purple`` prints the output in 5-letter groups. This can be
disabled or customized with the ``--group`` and ``--width`` options.

To decrypt this message::

   $ purple --decrypt -t "OGIVT SIAAH MWMHT VIBYY JUOJF UE"
   THEPU RPLEM ACHIN EISNO WONLI NE

Note that spaces are ignored on input. Again the output is produced in 5-letter
groups and wrapped at 70 letters per line. Here is the output again with
grouping disabled::

   $ purple -d -t "OGIVT SIAAH MWMHT VIBYY JUOJF UE" -g 0
   THEPURPLEMACHINEISNOWONLINE

You can use file redirection to capture output in a file::

   $ purple -e -t "The PURPLE machine is now online" -f > secret.txt
   $ purple -d -i secret.txt
   THEPU RPLEM ACHIN EISNO WONLI NE


Library Usage
#############

To use ``Purple`` from within Python code you must first construct
a ``Purple97`` object, which represents a single PURPLE cipher machine. The
constructor is given below::

   class Purple97(switches_pos=None, fast_switch=1, middle_switch=2,
                  alphabet=None)

The ``switches_pos`` argument, when not ``None``, must be a 4-tuple or list of
4 integers that describe the initial switch positions. Element 0 is the sixes
initial position, and the remaining elements are the initial positions of the
three twenties switches. These values must be in the range 0-24, inclusive.
If ``None`` then switch positions of all zeroes is assumed.

The ``fast_switch`` argument indicates which twenties switch (numbered 1-3) is
the fast switch. Likewise, ``middle_switch`` indicates which switch is the
middle switch. The slow switch is inferred. It is an error to give the
``fast_switch`` and ``middle_switch`` arguments the same value.

The ``alphabet`` argument is the plugboard alphabet mapping. It is expected to
be a 26-letter uppercase string. If ``None``, a mapping of
``AEIOUYBCDFGHJKLMNPQRSTVWXZ`` is assumed.

For convenience, another constructor is provided that allows you to specify
initial settings in the syntax described above::

   classmethod Purple97.from_key_sheet(switches, alphabet=None)

Here ``switches`` is a string in the syntax described above, e.g.
``'9-1,24,6-23'``.

The ``alphabet`` argument is as described in the first constructor.

Once constructed, you can use the ``Purple97`` object to perform encrypt and
decrypt operations. For example::

   from purple.machine import Purple97

   purple = Purple97.from_key_sheet(
          switches='9-1,24,6-23',
          alphabet='NOKTYUXEQLHBRMPDICJASVWGZF')

   ciphertext = purple.encrypt('THEPURPLEMACHINEISONLINE')

   purple = Purple97([8, 0, 23, 5], fast_switch=2, middle_switch=3,
                     alphabet='NOKTYUXEQLHBRMPDICJASVWGZF')

   plaintext = purple.decrypt(ciphertext)

For more information, please review the docstrings in the code.


Support
#######

To report a bug or suggest a feature, please use the issue tracker at the
`Purple Bitbucket page`_. You can also email the author using the address at
the top of this file.


References
##########

#. *PURPLE Revealed: Simulation and Computer-aided Cryptanalysis of Angooki
   Taipu B*, by Wes Freeman, Geoff Sullivan, and Frode Weierud. This paper
   was published in Cryptologia, Volume 27, Issue 1, January, 2003, pp. 1-43.
#. Frode Weierud's CryptoCellar page: `The PURPLE Machine`_
#. Wikipedia Article: `PURPLE Machine`_

The paper in reference 1 is also available here:
http://cryptocellar.web.cern.ch/cryptocellar/pubs/PurpleRevealed.pdf

This simulator would not have been possible without Frode Weierud's
CryptoCellar page and the detailed explanations and analysis found in reference
1. The author is also deeply grateful for email discussions with Frode Weierud
and Geoff Sullivan who provided me with plaintext, advice, and encouragement.

The ``Purple`` simulator's operation was checked against the simulator found in
reference 2.


.. _PURPLE Machine: http://en.wikipedia.org/wiki/Purple_(cipher_machine)
.. _Python: http://www.python.org
.. _Python Package Index: http://pypi.python.org/pypi/purple/
.. _virtualenv: http://www.virtualenv.org/
.. _pip: http://www.pip-installer.org
.. _Purple Bitbucket page: https://bitbucket.org/bgneal/purple/
.. _Mercurial: http://mercurial.selenic.com/
.. _The PURPLE Machine: http://cryptocellar.web.cern.ch/cryptocellar/simula/purple/
