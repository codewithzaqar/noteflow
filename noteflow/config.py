import os

DEFAULT_PATH = os.path.expanduser("~/.noteflow.txt")

def get_journal_path():
    return os.getenv("NOTEFLOW_PATH", DEFAULT_PATH)