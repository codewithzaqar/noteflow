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

    def _validate_tags(self, tags):
        if not tags:
            return []
        validated_tags = [tag.strip() for tag in tags if tag.strip()]
        if not validated_tags and tags:
            raise NoteflowError("All tags must be non-empty")
        return validated_tags

    def add_note(self, content, tags=None, date=None):
        if not content.strip():
            raise NoteflowError("Note content cannot be empty")
        tags = self._validate_tags(tags)
        note = {
            "id": len(self.notes) + 1,
            "date": date or datetime.now().isoformat(),
            "content": content,
            "tags": tags
        }
        self.notes.append(note)
        self._save_notes()

    def list_notes(self, start_date=None, end_date=None):
        notes = self.notes
        if start_date or end_date:
            notes = self._filter_by_date(notes, start_date, end_date)
        return notes

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
                    note["tags"] = self._validate_tags(tags)
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

    def search_notes(self, query, start_date=None, end_date=None):
        query = query.lower()
        results = []
        for note in self.notes:
            if query in note["content"].lower() or (note.get("tags") and query in [tag.lower() for tag in note["tags"]]):
                results.append(note)
        if start_date or end_date:
            results = self._filter_by_date(results, start_date, end_date)
        return results

    def _filter_by_date(self, notes, start_date, end_date):
        try:
            start = datetime.fromisoformat(start_date.replace('Z', '+00:00')) if start_date else None
            end = datetime.fromisoformat(end_date.replace('Z', '+00:00')) if end_date else None
        except ValueError:
            raise NoteflowError("Invalid date format. Use YYYY-MM-DD")
        
        filtered = []
        for note in notes:
            note_date = datetime.fromisoformat(note["date"].replace('Z', '+00:00'))
            if start and note_date < start:
                continue
            if end and note_date > end:
                continue
            filtered.append(note)
        return filtered