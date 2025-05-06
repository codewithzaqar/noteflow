import argparse
import sys
from .noteflow import Noteflow

def main():
    parser = argparse.ArgumentParser(description="Noteflow CLI")
    subparsers = parser.add_subparsers(dest="command")

    # Add note command
    add_parser = subparsers.add_parser("add", help="Add a new note")
    add_parser.add_argument("content", help="Note content")

    # List notes command
    list_parser = subparsers.add_parser("list", help="List all notes")

    # View note command
    view_parser = subparsers.add_parser("view", help="View a specific note")
    view_parser.add_argument("note_id", type=int, help="Note ID to view")

    args = parser.parse_args()

    noteflow = Noteflow()

    if args.command == "add":
        noteflow.add_note(args.content)
        print("Note added successfully")
    elif args.command == "list":
        notes = noteflow.list_notes()
        for note in notes:
            print(f"ID: {note['id']} | Date: {note['date']} | {note['content'][:50]}...")
    elif args.command == "view":
        note = noteflow.get_note(args.note_id)
        if note:
            print(f"ID: {note['id']}\nDate: {note['date']}\nContent: {note['content']}")
        else:
            print(f"Note {args.note_id} not found")
    else:
        parser.print_help()

if __name__ == "__main__":
    main()