import unittest
import os
from noteflow.noteflow import Noteflow

class TestNoteflow(unittest.TestCase):
    def setUp(self):
        self.test_file = "test_noteflow.json"
        self.noteflow = Noteflow(self.test_file)

    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_add_note(self):
        self.noteflow.add_note("Test note")
        notes = self.noteflow.list_notes()
        self.assertEqual(len(notes), 1)
        self.assertEqual(notes[0]["content"], "Test note")

    def test_get_note(self):
        self.noteflow.add_note("Test note")
        note = self.noteflow.get_note(1)
        self.assertIsNotNone(note)
        self.assertEqual(note["content"], "Test note")
        self.assertIsNone(self.noteflow.get_note(999))

if __name__ == "__main__":
    unittest.main()