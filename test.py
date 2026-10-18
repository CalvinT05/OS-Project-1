import unittest

from encryption import *

class TestEncryption(unittest.TestCase):
    def test(self):
        self.assertEqual(vigenere_encrypt("HELLO", "HELLO"), "OIWWC")
        self.assertEqual(vigenere_decrypt("OIWWC", "HELLO"), "HELLO")