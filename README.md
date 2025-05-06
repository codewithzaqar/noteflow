# NoteFlow

NoteFlow is a simple CLI-based journal tool written in Python.

## Installation

Clone the repo and install locally:

```bash
git clone https://github.com/codewithzaqar/noteflow.git
cd noteflow
pip install .
```

## Usage

```bash
# Add a new note (with optional tags)
noteflow add "This is my note" --tags work,personal

# List all notes
noteflow list

# View a specific note
noteflow view 1

# Edit an existing note (with optional tags)
noteflow edit 1 "Updated note content" --tags work

# Delete a note
noteflow delete 1

# Search notes by keyword or tag
noteflow search work
```

## Development
```bash
# Install dependencies
pip install -r requirements.txt

# Run tests
python -m unittest discover tests
```