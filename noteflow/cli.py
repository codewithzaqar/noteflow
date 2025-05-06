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

    # Edit note command
    edit_parser = subparsers.add_parser("edit", help="Edit an existing note")
    edit_parser.add_argument("note_id", type=int, help="Note ID to edit")
    edit_parser.add_argument("content", help="New note content")

    # Delete note command
    delete_parser = subparsers.add_parser("delete", help="Delete a note")
    delete_parser.add_argument("note_id", type=int, help="Note ID to delete")

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
    elif args.command == "edit":
        if not args.content.strip():
            print("Error: Note content cannot be empty")
            sys.exit(1)
        if noteflow.edit_note(args.note_id, args.content):
            print("Note edited successfully")
        else:
            print(f"Note {args.note_id} not found")
    elif args.command == "delete":
        if noteflow.delete_note(args.note_id):
            print("Note deleted successfully")
        else:
            print(f"Note {args.note_id} not found")
    else:
        parser.print_help()

if __name__ == "__main__":
    main()