import sys

# Base ASCII id
A = ord("A")

def vigenere_encrypt(text: str, key: str) -> str:
    encrypted = ""

    for i, ch in enumerate(text):
        # Take index of text and get character at index of key (wrapping)
        shift = ord(key[i % len(key)]) - A
        # Get the alphabet postition of text char,
        # add shift, mod to get alphabet position,
        # and convert back to char
        encrypted += chr((ord(ch) - A + shift) % 26 + A)

    return encrypted

def vigenere_decrypt(text: str, key: str) -> str:
    decrypted = ""

    for i, ch in enumerate(text):
        # Same as encrypted except subrtract the shift
        shift = ord(key[i % len(key)]) - A
        decrypted += chr((ord(ch) - A - shift) % 26 + A)

    return decrypted

class EncryptionService:
    def __init__(self):
        self.passkey = None

    def handle(self, line: str) -> str: ...

    def _set_pass(self, arg: str) -> str: ...
    def _encrypt(self, arg: str) -> str: ...
    def _decrypt(self, arg: str) -> str: ...

def main() -> None: ...