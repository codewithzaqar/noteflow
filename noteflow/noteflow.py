import json
import os
from datetime import datetime

class NoteflowError(Exception):
    pass

class Noteflow:
    def __init__(self, storage_file="noteflow.json"):
        self.storage_file = storage_file
        self.notes = self._load_notes()

    def _load_notes(self):
        if os.path.exists(self.storage_file):
            try:
                with open(self.storage_file, "r") as f:
                    notes = json.load(f)
                    # Migrate old notes: add tags field if missing
                    for note in notes:
                        if "tags" not in note:
                            note["tags"] = []
                    return notes
            except json.JSONDecodeError:
                raise NoteflowError("Corrupted storage file")
        return []

    def _save_notes(self):
        try:
            with open(self.storage_file, "w") as f:
                json.dump(self.notes, f, indent=2)
        except IOError:
            raise NoteflowError("Failed to save notes")

    def add_note(self, content, tags=None):
        if not content.strip():
            raise NoteflowError("Note content cannot be empty")
        note = {
            "id": len(self.notes) + 1,
            "date": datetime.now().isoformat(),
            "content": content,
            "tags": tags or []
        }
        self.notes.append(note)
        self._save_notes()

    def list_notes(self):
        return self.notes

    def get_note(self, note_id):
        for note in self.notes:
            if note["id"] == note_id:
                return note
        return None

    def edit_note(self, note_id, content, tags=None):
        if not content.strip():
            raise NoteflowError("Note content cannot be empty")
        for note in self.notes:
            if note["id"] == note_id:
                note["content"] = content
                note["date"] = datetime.now().isoformat()
                if tags is not None:
                    note["tags"] = tags
                self._save_notes()
                return True
        return False

    def delete_note(self, note_id):
        for i, note in enumerate(self.notes):
            if note["id"] == note_id:
                self.notes.pop(i)
                self._save_notes()
                return True
        return False

    def search_notes(self, query):
        query = query.lower()
        results = []
        for note in self.notes:
            if query in note["content"].lower() or (note.get("tags") and query in [tag.lower() for tag in note["tags"]]):
                results.append(note)
        return results