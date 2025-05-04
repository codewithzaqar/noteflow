from datetime import datetime, date
import os

JOURNAL_FILE = os.path.expanduser("~/.noteflow.txt")

def _parse_entries():
    """Parses entries into (id, entry) tuples."""
    if not os.path.exists(JOURNAL_FILE):
        return []
    raw_entries = open(JOURNAL_FILE, "r").read().strip().split("\n\n")
    return [(i + 1, entry.strip()) for i, entry in enumerate(raw_entries)]

def add_entry(text, title=None):
    now = datetime.now()
    with open(JOURNAL_FILE, "a") as f:
        f.write(f"\n[{now.strftime('%Y-%m-%d %H:%M:%S')}]\n")
        if title:
            f.write(f"Title: {title}\n")
        f.write(f"{text}\n")

def list_entries():
    return _parse_entries()
    
def search_entries(keyword):
    return [(i, e) for i, e in _parse_entries() if keyword.lower() in e.lower()]

def today_entries():
    today_str = date.today().strftime("%Y-%m-%d")
    return [(i, e) for i, e in _parse_entries() if e.startswith(f"[{today_str}]")]

def get_entry_by_id(entry_id):
    entries = _parse_entries()
    for i, entry in entries:
        if i == entry_id:
            return entry
    return None