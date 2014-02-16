# Copyright (C) 2013 - 2014 by Brian Neal.
# This file is part of purple, the PURPLE (Cipher Machine 97) simulation.
# purple is released under the MIT License (see LICENSE.txt).

import string
import unittest

from purple.machine import Purple97, Purple97Error
from purple.switch import SteppingSwitchError


# This is part 1 of the famous 14 part message. The ciphertext and plaintext are
# laid on top of each other, every other line, with blank lines inserted for
# clarity. Garbles are indicated by '-' characters.
#
part1 = """
ZTXODNWKCCMAVNZXYWEETUQTCIMNVEUVIWBLUAXRRTLVA
FOVTATAKIDASINIMUIMINOMOXIWOIRUBESIFYXXFCKZZR

RGNTPCNOIUPJLCIVRTPJKAUHVMUDTHKTXYZELQTVWGBUHFAWSH
DXOOVBTNFYXFAEMEMORANDUMFIOFOVOOMOJIBAKARIFYXRAICC

ULBFBHEXMYHFLOWD-KWHKKNXEBVPYHHGHEKXIOHQHUHWIKYJYH
YLFCBBCFCTHEGOVE-NMENTOFJAPANLFLPROMPTEDBYAGENUINE

PPFEALNNAKIBOOZNFRLQCFLJTTSSDDOIOCVT-ZCKQTSHXTIJCN
DESIRETOCOMETOANAMICABLEUNDERSTANDIN-WITHTHEGOVERN

WXOKUFNQR-TAOIHWTATWVHOTGCGAKVANKZANMUIN
MENTOFTHE-NITEDSTATESINORDERTHATTHETWOCO

YOYJFSRDKKSEQBWKIOORJAUWKXQGUWPDUDZNDRMDHVHYPNIZXB
UNTRIESBYTHEIRJOINTEFFORTSMAYSECURETHEPEACEOFTHEPA

GICXRMAWMFTIUDBXIENLONOQVQKYCOTVSHVNZZQPDLMXVNRUUN
CIFICAREAANDTHEREBYCONTRIBUTETOWARDTHEREALIZATIONO

QFTCDFECZDFGMXEHHWYONHYNJDOVJUNCSUVKKEIWOLKRBUUSOZ
FWORLDPEACELFLHASCONTINUEDNEGOTIATIONSWITHTHEUTMOS

UIGNISMWUOSBOBLJXERZJEQYQMTFTXBJNCMJKVRKOTSOPBOYMK
TSINCERITYSINCEAPRILLASTWITHTHEGOVERNMENTOFTHEUNIT

IRETINCPSQJAWVHUFKRMAMXNZUIFNOPUEMHGLOEJHZOOKHHEED
EDSTATESREGARDINGTHEADJUSTMENTANDADVANCEMENTOFJAPA

NIHXFXFXGPDZBSKAZABYEKYEPNIYSHVKFRFPVCJTPTOYCNEIQB
NESEVVFAMERICANRELATIONSANDTHESTABILIZATIONOFTHEPA

FEXMERMIZLGDRXZORLZFSQYPZFATZCHUGRNHWDDTAIHYOOCOOD
CIFICAREACFCCCFTHEJAPANESEQOVERNMENXHASTHEHONORTOS

UZYIWJROOJUMUIHRBEJFONAXGNCKAOARDIHCDZKIXPR--DIMUW
TATEFRANKLYITSVIEWSCONCERNINGTHECLAIMSTHEAM--VCANG

OMHLTJSOUXPFKGEPWJOMTUVKMWRKTACUPIGAFEDFVRKXFXLFGU
OVERNMENTHASUERSISTENTLYMAINTAINEDASWELLASTHEMEASU

RDETJIYOLKBHZKXOJDDOVRHMMUQBFOWRODMRMUWNAYKYPISDLH
RESTHEUNITEDSTATESANDGREATBRITAINHAVETAKENTOWARDJA

ECKINLJORKWNWXADAJOLONOEVMUQDFIDSPEBBPWROFBOPAZJEU
PANDURINGTHKSEEIGHTMONTHSCYCCCFLFCDDCFCITISTHEIMMU

USBHGIORCSUUQKIIEHPCTJRWSOGLETZLOUKKEOJOSMKJBWUCDD
TABLXPOLWCYOFTHEJAPANESEGOVERNMENTTOINSURETHESTABI

CPYUUWCSSKWWVLIUPKYXGKQOKAZTEZFHGVPJFEWEUBKLIZLWKK
LITYOFEASTASIAANDTOPROMOTEWORLZPEACELFLANDTHEREBYT

OBXLEPQPDATWUSUUPKYRHNWDZXXGTWDDNSHDCBCJXAOOEEPUBP
OEIABLEALLNATIONSTOFINDEACHITSPROPERPLACEINTHEWORL

WFRBQSFXSEZJJYAANMG-WLYMGWAQDGIVNOHKOUTIXYFOKNGGBF
DCFCCCFEVERSINCETHE-HINAAFFAIRBROKEOUTOWINGTOTHEFA

GANPWTUYLBEFFKUFLEXOIUUANVMMJEQUSFHFDOHQLAKWTBYYYL
ILUREONTHEPARTOFCHINATOCOMPREHENLJAPANVCFSTRUEYNTE

NTLYTSXCGKCEEWQRYAVGRKXIANPXNOFVXGKJFAVKLTHOCXCIVK
NTIONSLFLTWEJAPANESEGOVERNMENTHASSTRIVENFORTHEREST

OLXTJTUNCLQCICRUIIWQDDMOTPRVTJKKSKFHXFKMDIKIZWROGZ
ORATIONOFPEACEANDIMHASCONSISTENTLYEXERTEDITSBESTEF

JYMTMNOVMFJ-OKTEIVMYANOHNNYPDLEXCFRRNEBLMNYEBGNHCZ
FORTSTOPREV-NTTHEEXTENTIONOFWARVVFLIKEVISTURBANCES

ZCFNWGGRHRIUUTTILKLODUYZKQOZMMNHASXHLPVTNGHQDAJIUG
CFCNSIASALSOTOTHATENDTNATINSEPTEMBERLASTYEARJAPANC

OOSZ-----ZRTGWFBLKI--------YBDABJ-----WYOEANV---OM
ONCL-----HETRIPAITI--------THGERM-----DYTALYC---OV
"""

pt1_lines = part1.split()
PT1_CT = ''.join(pt1_lines[0::2])
PT1_PT = ''.join(pt1_lines[1::2])


class Purple97TestCase(unittest.TestCase):

    def test_construction(self):

        Purple97()
        Purple97([0, 1, 2, 3])
        Purple97([0, 1, 2, 3], 1)
        Purple97([0, 1, 2, 3], 2, 1)
        Purple97((0, 1, 2, 3), 2, 1, string.ascii_uppercase)
        Purple97((0, 1, 2, 3), 2, 1, string.ascii_lowercase)
        Purple97(alphabet=string.ascii_lowercase)
        Purple97(fast_switch=3, middle_switch=1)

    def test_construct_bad_positions(self):

        self.assertRaises(Purple97Error, Purple97, [])
        self.assertRaises(Purple97Error, Purple97, [1])
        self.assertRaises(Purple97Error, Purple97, [1, 1, 1, 1, 1])
        self.assertRaises(SteppingSwitchError, Purple97, [1, 1, 1, 100])

    def test_construct_bad_switches(self):

        self.assertRaises(Purple97Error, Purple97, fast_switch=0)
        self.assertRaises(Purple97Error, Purple97, fast_switch=4)
        self.assertRaises(Purple97Error, Purple97, fast_switch=-1)

        self.assertRaises(Purple97Error, Purple97, middle_switch=0)
        self.assertRaises(Purple97Error, Purple97, middle_switch=4)
        self.assertRaises(Purple97Error, Purple97, middle_switch=-1)

        self.assertRaises(Purple97Error, Purple97, fast_switch=2)
        self.assertRaises(Purple97Error, Purple97, fast_switch=1, middle_switch=1)
        self.assertRaises(Purple97Error, Purple97, fast_switch=2, middle_switch=2)
        self.assertRaises(Purple97Error, Purple97, fast_switch=3, middle_switch=3)

        self.assertRaises(Purple97Error, Purple97, fast_switch=0, middle_switch=1)
        self.assertRaises(Purple97Error, Purple97, fast_switch=0, middle_switch=0)
        self.assertRaises(Purple97Error, Purple97, fast_switch=0, middle_switch=4)

    def test_construct_bad_alphabet(self):

        alpha = ''
        self.assertRaises(Purple97Error, Purple97, alphabet=alpha)
        alpha = '1'
        self.assertRaises(Purple97Error, Purple97, alphabet=alpha)
        alpha = '!' * 26
        self.assertRaises(Purple97Error, Purple97, alphabet=alpha)
        alpha = string.ascii_uppercase[3:]
        self.assertRaises(Purple97Error, Purple97, alphabet=alpha)
        alpha = string.ascii_uppercase + string.ascii_uppercase[4:10]
        self.assertRaises(Purple97Error, Purple97, alphabet=alpha)
        alpha = string.ascii_uppercase[:13] + string.ascii_uppercase[:13]
        self.assertRaises(Purple97Error, Purple97, alphabet=alpha)
        alpha = 'M' * 26
        self.assertRaises(Purple97Error, Purple97, alphabet=alpha)

    def test_from_key_sheet(self):

        Purple97.from_key_sheet('9-1,2,3-23')
        Purple97.from_key_sheet('1-1,1,1-13')
        Purple97.from_key_sheet('25-25,25,25-31')
        Purple97.from_key_sheet('5-20,7,18-21', alphabet=string.ascii_uppercase)

    def test_bad_from_key_sheet(self):

        self.assertRaises(SteppingSwitchError, Purple97.from_key_sheet, '0-1,2,3-13')
        self.assertRaises(SteppingSwitchError, Purple97.from_key_sheet, '26-1,2,3-13')
        self.assertRaises(SteppingSwitchError, Purple97.from_key_sheet, '1-1,0,3-13')
        self.assertRaises(SteppingSwitchError, Purple97.from_key_sheet, '1-1,2,26-13')
        self.assertRaises(SteppingSwitchError, Purple97.from_key_sheet, '1-1,2,26-03')
        self.assertRaises(SteppingSwitchError, Purple97.from_key_sheet, '1-1,2,26-00')
        self.assertRaises(SteppingSwitchError, Purple97.from_key_sheet, '1-1,2,26-14')

        self.assertRaises(Purple97Error, Purple97.from_key_sheet, 'bad string')
        self.assertRaises(Purple97Error, Purple97.from_key_sheet, '1-2-1,2,26-14')
        self.assertRaises(Purple97Error, Purple97.from_key_sheet, 'a-9,2,20-13')
        self.assertRaises(Purple97Error, Purple97.from_key_sheet, '1-a,2,20-13')
        self.assertRaises(Purple97Error, Purple97.from_key_sheet, '1-9,a,20-13')
        self.assertRaises(Purple97Error, Purple97.from_key_sheet, '1-9,2,a-13')
        self.assertRaises(Purple97Error, Purple97.from_key_sheet, '1-9,2,20-a3')
        self.assertRaises(Purple97Error, Purple97.from_key_sheet, '1-9,2,20-1a')
        self.assertRaises(Purple97Error, Purple97.from_key_sheet, '1-9,2,20-123')

    def test_decrypt_part_1_message(self):

        ciphertext = PT1_CT
        plaintext = PT1_PT

        self.assertEqual(len(ciphertext), len(plaintext))

        # Decrypt
        purple = Purple97.from_key_sheet(
                switches='9-1,24,6-23',
                alphabet='NOKTYUXEQLHBRMPDICJASVWGZF')

        actual = purple.decrypt(ciphertext)

        mismatches = []
        for n, (a, b) in enumerate(zip(plaintext, actual)):
            if a != b:
                mismatches.append((n, a, b))

        msg = None
        if mismatches:
            msg = "There are {} mismatches: {}".format(len(mismatches),
                    mismatches)

        self.assertTrue(len(mismatches) == 0, msg)

    def test_encrypt_part_1_message(self):

        ciphertext = PT1_CT
        plaintext = PT1_PT

        # Use 'X' in place of the garbles
        input_text = plaintext.replace('-', 'X')

        self.assertEqual(len(ciphertext), len(plaintext))

        # Encrypt
        purple = Purple97.from_key_sheet(
                switches='9-1,24,6-23',
                alphabet='NOKTYUXEQLHBRMPDICJASVWGZF')

        actual = purple.encrypt(input_text)

        mismatches = []
        for n, (a, b) in enumerate(zip(ciphertext, actual)):
            if a != b and a != '-':
                mismatches.append((n, a, b))

        msg = None
        if mismatches:
            msg = "There are {} mismatches: {}".format(len(mismatches),
                    mismatches)

        self.assertTrue(len(mismatches) == 0, msg)
