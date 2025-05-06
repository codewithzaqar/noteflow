import json
import os
from datetime import datetime

class Noteflow:
    def __init__(self, storage_file="noteflow.json"):
        self.storage_file = storage_file
        self.notes = self._load_notes()

    def _load_notes(self):
        if os.path.exists(self.storage_file):
            with open(self.storage_file, "r") as f:
                return json.load(f)
        return []
    
    def _save_notes(self):
        with open(self.storage_file, "w") as f:
            json.dump(self.notes, f, indent=2)

    def add_note(self, content):
        note = {
            "id": len(self.notes) + 1,
            "date": datetime.now().isoformat(),
            "content": content
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
    
    def edit_note(self, note_id, content):
        for note in self.notes:
            if note["id"] == note_id:
                note["content"] = content
                note["date"] = datetime.now().isoformat()
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