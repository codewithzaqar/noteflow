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
# Add a new note
noteflow add "This is my note"

# List all notes
noteflow list

# View a specific note
noteflow view 1

# Edit an existing note
noteflow edit 1 "Updated note content"

# Delete a note
noteflow delete 1
```

## Development
```bash
# Install dependencies
pip install -r requirements.txt

# Run tests
python -m unittest discover tests
```