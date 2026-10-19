from datetime import datetime
import sys

def format_entry(line: str, now: datetime = None) -> str:
    if now == None:
        now = datetime.now()
    
    message = line.strip().split(' ', 1)
    action = message[0]
    text = message[1] if len(message) > 1 else None
    
    entry = now.strftime("%Y-%m-%d %H:%M") + " [" + action + ']'

    if text:
        entry += ' ' + text
    return entry

def main() -> None:
    with open(sys.argv[1], "a", encoding="utf8") as log:
        for line in sys.stdin:
            if not line.strip():
                continue
            if line.split()[0] == "QUIT":
                break
            log.write(format_entry(line) + "\n")
            log.flush()

if __name__ == "__main__":
    main()