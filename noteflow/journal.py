from datetime import datetime
import os

JOURNAL_FILE = os.path.expanduser("~/.noteflow.txt")

def add_entry(text):
    """Add a new journal entry."""
    with open(JOURNAL_FILE, "a") as f:
        f.write(f"{datetime.now().isoformat()} - {text}\n")

def list_entries():
    """List all journal entries."""
    if not os.path.exists(JOURNAL_FILE):
        return []
    with open(JOURNAL_FILE, "r") as f:
        return f.readlines()