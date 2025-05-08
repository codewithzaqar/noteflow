import unittest
import os
import json
from datetime import datetime, timedelta
from noteflow.noteflow import Noteflow, NoteflowError

class TestNoteflow(unittest.TestCase):
    def setUp(self):
        self.test_file = "test_noteflow.json"
        self.noteflow = Noteflow(self.test_file)

    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
        if os.path.exists("logs/noteflow.log"):
            os.remove("logs/noteflow.log")

    def test_add_note(self):
        self.noteflow.add_note("Test note", ["work"])
        notes = self.noteflow.list_notes()
        self.assertEqual(len(notes), 1)
        self.assertEqual(notes[0]["content"], "Test note")
        self.assertEqual(notes[0]["tags"], ["work"])

    def test_get_note(self):
        self.noteflow.add_note("Test note", ["personal"])
        note = self.noteflow.get_note(1)
        self.assertIsNotNone(note)
        self.assertEqual(note["content"], "Test note")
        self.assertEqual(note["tags"], ["personal"])
        self.assertIsNone(self.noteflow.get_note(999))

    def test_edit_note(self):
        self.noteflow.add_note("Original note", ["work"])
        result = self.noteflow.edit_note(1, "Edited note", ["personal"])
        self.assertTrue(result)
        note = self.noteflow.get_note(1)
        self.assertEqual(note["content"], "Edited note")
        self.assertEqual(note["tags"], ["personal"])
        self.assertFalse(self.noteflow.edit_note(999, "Non-existent"))

    def test_delete_note(self):
        self.noteflow.add_note("Test note")
        result = self.noteflow.delete_note(1)
        self.assertTrue(result)
        self.assertEqual(len(self.noteflow.list_notes()), 0)
        self.assertFalse(self.noteflow.delete_note(999))

    def test_search_notes(self):
        self.noteflow.add_note("Test note about work", ["work"])
        self.noteflow.add_note("Personal note", ["personal"])
        results = self.noteflow.search_notes("work")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["content"], "Test note about work")
        results = self.noteflow.search_notes("personal")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["content"], "Personal note")
        results = self.noteflow.search_notes("nothing")
        self.assertEqual(len(results), 0)

    def test_empty_content(self):
        with self.assertRaises(NoteflowError):
            self.noteflow.add_note("")
        with self.assertRaises(NoteflowError):
            self.noteflow.edit_note(1, "")

    def test_backward_compatibility(self):
        old_note = {"id": 1, "date": "2025-05-06T12:00:00", "content": "Old note"}
        with open(self.test_file, "w") as f:
            json.dump([old_note], f)
        self.noteflow = Noteflow(self.test_file)
        notes = self.noteflow.list_notes()
        self.assertEqual(len(notes), 1)
        self.assertEqual(notes[0]["tags"], [])
        results = self.noteflow.search_notes("old")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["content"], "Old note")

    def test_date_filtering(self):
        now = datetime.now()
        yesterday = (now - timedelta(days=1)).isoformat()
        today = now.isoformat()
        self.noteflow.add_note("Yesterday's note", tags=["test"], date=yesterday)
        self.noteflow.add_note("Today's note", tags=["test"], date=today)
        notes = self.noteflow.list_notes(start_date=now.strftime("%Y-%m-%d"))
        self.assertEqual(len(notes), 1)
        self.assertEqual(notes[0]["content"], "Today's note")
        notes = self.noteflow.list_notes(end_date=(now - timedelta(days=2)).strftime("%Y-%m-%d"))
        self.assertEqual(len(notes), 0)

    def test_search_with_date_filter(self):
        now = datetime.now()
        yesterday = (now - timedelta(days=1)).isoformat()
        today = now.isoformat()
        self.noteflow.add_note("Work note", tags=["work"], date=yesterday)
        self.noteflow.add_note("Another work note", tags=["work"], date=today)
        results = self.noteflow.search_notes("work", start_date=now.strftime("%Y-%m-%d"))
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["content"], "Another work note")

    def test_tag_validation(self):
        self.noteflow.add_note("Valid note", ["work", "personal"])
        note = self.noteflow.get_note(1)
        self.assertEqual(note["tags"], ["work", "personal"])
        with self.assertRaises(NoteflowError):
            self.noteflow.add_note("Invalid note", ["", "  "])
        self.noteflow.edit_note(1, "Edited note", ["valid"])
        note = self.noteflow.get_note(1)
        self.assertEqual(note["tags"], ["valid"])

if __name__ == "__main__":
    unittest.main()