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
        type, _, message = reply.partition(' ')
        return type, message
    
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
            print(str(i) + "\t" + item)
    
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
        self.history = {
            "password": History(),
            "encrypt": History(),
            "decrypt": History()
        }

        self.commands = {
            "password": self.cmd_password,
            "encrypt": self.cmd_encrypt,
            "decrypt": self.cmd_decrypt,
            "history": self.cmd_history
        }

    def run(self) -> None:
        self.logger.log("START", "Driver started.")

        while True:
            print("""
Commands:
    password    set passkey
    encrypt     encrypt a string
    decrypt     decrypt a string
    history     show passkey history
    quit        exit program
""")

            command = input("Enter command: ").strip().lower()

            if command == "quit":
                self.logger.log("COMMAND", "quit")
                break
            
            handler = self.commands.get(command)

            if handler == None:
                print("Error: Unknown command.")
                self.logger.log("ERROR", "Unknown command")
                continue

            self.logger.log("COMMAND", command)
            handler()
        
        self.encryption.close()
        self.logger.log("EXIT", "Driver exiting")
        self.logger.close()

    def cmd_password(self) -> None:
        password = self.history["password"].select()
        if password == None:
            return
        type, message = self.encryption.send("PASS", password)

        if type == "RESULT":
            print("Passkey set")
            self.logger.log("RESULT", "Passkey set")
            self.history["password"].add(password)
        else:
            print("Error: issue setting passkey")

    def cmd_encrypt(self) -> None: ...
    def cmd_decrypt(self) -> None: ...
    def cmd_history(self) -> None: ...
    def cmd_quit(self) -> None: ...
    def _get_input_string(self, prompt: str, save_to_history: bool) -> str | None: ...

def is_letters_only(s: str) -> bool: ...
def print_menu() -> None: ...

def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: python driver.py <logfile>")
        sys.exit(1)
    Driver(sys.argv[1]).run()

if __name__ == "__main__":
    main()