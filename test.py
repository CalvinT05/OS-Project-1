import unittest

from encryption import *

class TestEncryption(unittest.TestCase):
    def test_vigenere(self):
        self.assertEqual(vigenere_encrypt("HELLO", "HELLO"), "OIWWC")
        self.assertEqual(vigenere_decrypt("OIWWC", "HELLO"), "HELLO")

    def setUp(self):
        self.svc = EncryptionService()
    
    def test_commands_without_passkey(self):
        self.assertEqual(self.svc.handle("ENCRYPT HELLO"), "ERROR Passkey not set")
        self.assertEqual(self.svc.handle("DECRYPT HELLO"), "ERROR Passkey not set")

    def test_commands_with_passkey(self):
        self.assertEqual(self.svc.handle("PASS HELLO"), "RESULT")
        self.assertEqual(self.svc.handle("ENCRYPT HELLO"), "RESULT OIWWC")
        self.assertEqual(self.svc.handle("DECRYPT OIWWC"), "RESULT HELLO")