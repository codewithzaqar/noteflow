from datetime import datetime, date
import os

JOURNAL_FILE = os.path.expanduser("~/.noteflow.txt")

def _parse_entries():
    if not os.path.exists(JOURNAL_FILE):
        return []
    raw_entries = open(JOURNAL_FILE, "r").read().strip().split("\n\n")
    return [(i + 1, entry.strip()) for i, entry in enumerate(raw_entries)]

def _save_entries(entries):
    with open(JOURNAL_FILE, "w") as f:
        for entry in entries:
            f.write(entry.strip() + "\n\n")

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
    for i, entry in _parse_entries():
        if i == entry_id:
            return entry
    return None

def delete_entry_by_id(entry_id):
    entries = _parse_entries()
    updated = [entry for i, entry in entries if i != entry_id]
    _save_entries(updated)
    return len(updated) < len(entries)

def export_entries(filepath):
    entries = _parse_entries()
    with open(filepath, "w") as f:
        for i, entry in entries:
            f.write(f"# {i}\n" + "=" * 40 + "\n")
            f.write(entry + "\n")
            f.write("=" * 40 + "\n\n")