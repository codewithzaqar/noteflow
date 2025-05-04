# NoteFlow

NoteFlow is a simple CLI-based journal tool written in Python.

## Installation

Clone the repo and install locally:

```bash
git clone
https://github.com/codewithzaqar/noteflow.git
cd noteflow
pip install .
```

## Usage

```bash
# Add a new journal entry
noteflow add "Today I started writting in NoteFlow." --title "NoteFlow"

noteflow add "Had a productive day." -t "Daily Recap"

# List all journal entries
noteflow list

# List today's entries only
noteflow list --today

# Search entries by keyword
noteflow search "started"

# Example Entry Format
[2025-05-03 14:20:31]
Title: NoteFlow
Today I started writting in NoteFlow.

# View a specific entry
noteflow view 2

# Entry Format
'#2'
=======================================================
[2025-05-04 14:20:31]
Title: NoteFlow
Today I started writting in Noteflow.
=======================================================
```

Each entry will be printed with a timestamp, optional title, and the entry body, separated by lines for clarity.

## Storage

All entries are saved in a plain text file at:
```
~/.noteflow.txt
```