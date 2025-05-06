import unittest
import json
import os
from noteflow.noteflow import Noteflow, NoteflowError

class TestNoteflow(unittest.TestCase):
    def setUp(self):
        self.test_file = "test_noteflow.json"
        self.noteflow = Noteflow(self.test_file)

    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

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
        # Simulate an old note without tags
        old_note = {"id": 1, "date": "2025-05-06T12:00:00", "content": "Old note"}
        with open(self.test_file, "w") as f:
            json.dump([old_note], f)
        # Reload notes
        self.noteflow = Noteflow(self.test_file)
        notes = self.noteflow.list_notes()
        self.assertEqual(len(notes), 1)
        self.assertEqual(notes[0]["tags"], [])
        # Test search with old note
        results = self.noteflow.search_notes("old")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["content"], "Old note")

if __name__ == "__main__":
    unittest.main()