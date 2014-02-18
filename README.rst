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

``Purple`` is a Python library and command-line utility for simulating the `PURPLE
Machine`_, a cipher machine used by the Japanese Foreign Office before and
during the Second World War. PURPLE was the code name given to machine by U.S.
cryptanalysts. The Japanese called the machine 97-shiki ōbun inji-ki (System 97
Printing Machine for European Characters), and Angōki B-kata (Type B Cipher
Machine). The machine was used for secure diplomatic communications and was an
electromechanical stepping-switch device.

This project is a Python 3 library and command-line utility for encrypting and
decrypting text by simulating the operation of an actual PURPLE machine.


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

(TODO: Text goes here explaining the switches and alphabet settings)

If you are going to be working with the same initial switch settings and
plugboard alphabet it may be more convenient to specify them as environment
variables instead of repeatedly using the command-line arguments ``-s`` and
``-a``.  The examples below assume these statements have been executed::

   $ export PURPLE97_SWITCHES=9-1,24,6-23
   $ export PURPLE97_ALPHABET=NOKTYUXEQLHBRMPDICJASVWGZF

The ``purple`` command operates in two modes, either encrypt (specified with
``-e`` or ``--encrypt``) or decrypt (``-d`` or ``--decrypt``). Input text can
be specified on the command-line with the ``-t`` or ``--text`` option, or
a read from a file (``-i`` or ``--input``).

When encrypting text, the ``purple`` machine only accepts the letters A-Z, but
also allows for "garble" letters to be indicated by using the ``-`` (dash)
character. This means all punctuation and spaces must be either be omitted or
input via some other convention. The ``-f`` or ``--filter`` flag, when present,
relaxes these restrictions a bit. When this flag is on, all lowercase letters
will be converted to uppercase, digits will be converted to words (e.g.
5 becomes FIVE), and all other characters will be ignored.

A simple encrypt example using the ``-f`` flag is given below::

   $ purple -e -t "The PURPLE machine is now online" -f
   OGIVT SIAAH MWMHT VIBYY JUOJF UE

By default ``purple`` prints the output in 5-letter groups. This can be
disabled or customized with the ``--group`` and ``--width`` options.

To decrypt this message::

   $ purple -d -t "OGIVT SIAAH MWMHT VIBYY JUOJF UE"
   THEPU RPLEM ACHIN EISNO WONLI NE

Note that spaces are ignored on input. Again the output is produced in 5-letter
groups and wrapped at 70 letters per line. Here is the output again with
grouping disabled::

   $ purple -d -t "OGIVT SIAAH MWMHT VIBYY JUOJF UE" -g 0
   THEPURPLEMACHINEISNOWONLINE

Of course you can use file redirection to capture output in a file::

   $ purple -e -t "The PURPLE machine is now online" -f > secret.txt
   $ purple -d -i secret.txt
   THEPU RPLEM ACHIN EISNO WONLI NE


Library Usage
#############


Support
#######


References
##########


.. _PURPLE Machine: http://en.wikipedia.org/wiki/Purple_(cipher_machine)
.. _Python: http://www.python.org
.. _Python Package Index: http://pypi.python.org/pypi/m209/
.. _virtualenv: http://www.virtualenv.org/
.. _pip: http://www.pip-installer.org
.. _Purple Bitbucket page: https://bitbucket.org/bgneal/purple/
.. _Mercurial: http://mercurial.selenic.com/
