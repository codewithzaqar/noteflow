import os
from datetime import datetime, date
from noteflow.config import get_journal_path

JOURNAL_FILE = get_journal_path()

def _parse_entries():
    if not os.path.exists(JOURNAL_FILE):
        return []
    raw = open(JOURNAL_FILE, "r").read().strip().split("\n\n")
    return [(i + 1, e.strip()) for i, e in enumerate(raw)]

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
    today = date.today().strftime("%Y-%m-%d")
    return [(i, e) for i, e in _parse_entries() if e.startswith(f"[{today}]")]

def get_entry_by_id(entry_id):
    return next((e for i, e in _parse_entries() if i == entry_id), None)

def delete_entry_by_id(entry_id):
    entries = _parse_entries()
    updated = [e for i, e in entries if i != entry_id]
    _save_entries(updated)
    return len(updated) < len(entries)