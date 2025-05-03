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
```

Each entry will be printed with a timestamp, optional title, and the entry body, separated by lines for clarity.

## Storage

All entries are saved in a plain text file at:
```
~/.noteflow.txt
```