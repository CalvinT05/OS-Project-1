import datetime

def format_entry(line: str, now: datetime) -> str:
    if now is None:
        now = datetime.now()
    
    message = line.split(' ', 1)
    action = message[0]
    text = message[1]
    
    entry = now.strftime("%Y-%m-%d %H:%M") + " [" + action + ']'

    if text:
        entry += ' ' + text
    return entry

def main() -> None: ...