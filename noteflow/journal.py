from datetime import datetime
import os

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