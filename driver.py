import sys
from subprocess import Popen, PIPE
from typing import List

class LoggerClient:
    def __init__(self, logfile: str):
        self.proc = Popen(
            ['python', 'logger.py', logfile],
            stdin=PIPE,
            encoding='utf8'
        )

    def log(self, action: str, text: str = "") -> None:
        self.proc.stdin.write(action + ' ' + text + '\n')
        self.proc.stdin.flush()

    def close(self) -> None:
        self.proc.stdin.write("QUIT\n")
        self.proc.stdin.flush()
        self.proc.stdin.close()
        self.proc.wait()

class EncryptionClient:
    def __init__(self):
        self.proc = Popen(
            ['python', 'encryption.py'],
            stdout=PIPE,
            stdin=PIPE,
            encoding='utf8'
        )

    def send(self, command: str, arg: str = "") -> tuple[str, str]:
        self.proc.stdin.write(command + ' ' + arg + '\n')
        self.proc.stdin.flush()
        reply = self.proc.stdout.readline().rstrip('\n')
        if not reply:
            return "ERROR", "Encryption program did not respond"
        kind, _, message = reply.partition(' ')
        return kind, message

    def close(self) -> None:
        self.proc.stdin.write("QUIT\n")
        self.proc.stdin.flush()
        self.proc.stdin.close()
        self.proc.wait()

class History:
    def __init__(self):
        self.items: List[str] = []

    def add(self, s: str) -> None:
        self.items.append(s)

    def is_empty(self) -> bool:
        return not self.items

    def print_history(self) -> None:
        for i, item in enumerate(self.items, start = 1):
            print(str(i) + '\t' + item)

    def select(self) -> str | None:
        if not self.is_empty():
            print("Entry History:")
            self.print_history()
            print()

            inp = input("Select from history (enter number) or enter new string: ")

            if inp.isdigit():
                selection = int(inp)
                if 1 <= selection <= len(self.items):
                    return self.items[selection - 1]
            else:
                return inp
        else:
            return input("Enter string: ")

        print("Please enter a valid input.")


class Driver:
    def __init__(self, logfile: str):
        self.logger = LoggerClient(logfile)
        self.encryption = EncryptionClient()
        self.history = History()

        self.commands = {
            "password": self.cmd_password,
            "encrypt": self.cmd_encrypt,
            "decrypt": self.cmd_decrypt,
            "history": self.cmd_history
        }

    def run(self) -> None:
        self.logger.log("START", "Driver started.")

        try:
            while True:
                print_menu()

                command = input("Enter command: ").strip().lower()

                if command == "quit":
                    self.logger.log("COMMAND", "quit")
                    break

                handler = self.commands.get(command)

                if handler is None:
                    print("Error: Unknown command.")
                    self.logger.log("ERROR", "Unknown command")
                    continue

                self.logger.log("COMMAND", command)
                handler()
        except (EOFError, KeyboardInterrupt):
            print()
            self.logger.log("COMMAND", "quit (input ended)")

        self.cmd_quit()

    def cmd_password(self) -> None:
        password = self.input_with_history(save_to_history=False)
        if password is None:
            return

        kind, message = self.encryption.send("PASS", password)

        if kind == "RESULT":
            print("Passkey set")
            self.logger.log("RESULT", "Passkey set")
        else:
            print("Error: " + message)
            self.logger.log("ERROR", message)

    def cmd_encrypt(self) -> None:
        self._crypt("ENCRYPT")

    def cmd_decrypt(self) -> None:
        self._crypt("DECRYPT")

    def cmd_history(self) -> None:
        print("History:")
        if self.history.is_empty():
            print("\t(empty)")
        else:
            self.history.print_history()
        self.logger.log("RESULT", "Showed " + str(len(self.history.items)) + " history entries")

    def cmd_quit(self) -> None:
        self.encryption.close()
        self.logger.log("EXIT", "Driver exiting")
        self.logger.close()

    def _crypt(self, command: str) -> None:
        text = self.input_with_history(save_to_history=True)
        if text is None:
            return

        self.logger.log("INPUT", text)
        kind, message = self.encryption.send(command, text)

        if kind == "RESULT":
            print("Result: " + message)
            self.history.add(message)
            self.logger.log("RESULT", message)
        else:
            print("Error: " + message)
            self.logger.log("ERROR", message)

    def input_with_history(self, save_to_history: bool) -> str | None:
        text = self.history.select()
        if text is None:
            return None

        text = text.strip()
        if not is_letters_only(text):
            print("Error: input must contain only letters.")
            self.logger.log("ERROR", "Input must contain only letters")
            return None

        text = text.upper()

        if save_to_history and text not in self.history.items:
            self.history.add(text)
        return text

def is_letters_only(s: str) -> bool:
    return s.isascii() and s.isalpha()

def print_menu() -> None:
    print("""
Commands:
    password    set passkey
    encrypt     encrypt a string
    decrypt     decrypt a string
    history     show history
    quit        exit program
""")

def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: python driver.py <logfile>")
        sys.exit(1)
    Driver(sys.argv[1]).run()

if __name__ == "__main__":
    main()