import unittest
import datetime

from encryption import *
from logger import *

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

class TestLogger(unittest.TestCase):
    def test_datetime(self):
        now = datetime.datetime(2026, 10, 18, 18, 0)
        self.assertEqual(
            format_entry("START Logging Started.", now),
            "2026-10-18 18:00 [START] Logging Started."
        )
    
    def test_no_message(self):
        now = datetime.datetime(2026, 10, 18, 18, 0)
        self.assertEqual(
            format_entry("EXIT", now),
            "2026-10-18 18:00 [EXIT]"
        )