from datetime import datetime, date
import os
import re

JOURNAL_FILE = os.path.expanduser("~/.noteflow.txt")

def add_entry(text, title=None):
    """Add a new journal entry with optional title."""
    now = datetime.now()
    with open(JOURNAL_FILE, "a") as f:
        f.write(f"\n[{now.strftime('%Y-%m-%d %H:%M:%S')}]\n")
        if title:
            f.write(f"Title: {title}\n")
        f.write(f"{text}\n")

def list_entries():
    """List all journal entries."""
    if not os.path.exists(JOURNAL_FILE):
        return []
    with open(JOURNAL_FILE, "r") as f:
        return f.read().strip().split("\n\n")
    
def search_entries(keyword):
    """Return entries that contain the keyword."""
    return [entry for entry in list_entries() if keyword.lower() in entry.lower()]

def today_entries():
    """Return entries from today."""
    today_str = date.today().strftime("%Y-%m-%d")
    return [entry for entry in list_entries() if entry.startswith(f"[{today_str}]")]