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

    def handle(self, line: str) -> str:
        command = line.strip().split(' ', 1)
        name = command[0]
        arg = command[1] if len(command) > 1 else None
        if name == "QUIT":
            return None
        if name == "PASS":
            return self.set_passkey(arg)
        if name == "ENCRYPT":
            return self.encrypt(arg)
        if name == "DECRYPT":
            return self.decrypt(arg)
        return "ERROR Unknown command"

    def set_passkey(self, arg: str) -> str:
        if not arg:
            return "ERROR No argument"
        if not arg.isalpha():
            return "ERROR Passkey must contain only letters"
        
        self.passkey = arg.upper()
        return "RESULT"

    def encrypt(self, arg: str) -> str:
        if self.passkey == None:
            return "ERROR Passkey not set"
        if not arg:
            return "ERROR No argument"
        if not arg.isalpha():
            return "ERROR Text must contain only letters"
        
        return "RESULT " + vigenere_encrypt(arg.upper(), self.passkey)

    def decrypt(self, arg: str) -> str:
        if self.passkey == None:
            return "ERROR Passkey not set"
        if not arg:
            return "ERROR No argument"
        if not arg.isalpha():
            return "ERROR Text must contain only letters"
        
        return "RESULT " + vigenere_decrypt(arg.upper(), self.passkey)

def main() -> None:
    service = EncryptionService()
    for line in sys.stdin:
        response = service.handle(line)
        if response == None:
            break
        print(response)
        sys.stdout.flush()

if __name__ == "__main__":
    main()