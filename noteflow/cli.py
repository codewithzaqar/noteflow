import argparse
import sys
from .noteflow import Noteflow, NoteflowError

def main():
    parser = argparse.ArgumentParser(description="Noteflow CLI")
    subparsers = parser.add_subparsers(dest="command")

    # Add note command
    add_parser = subparsers.add_parser("add", help="Add a new note")
    add_parser.add_argument("content", help="Note content")
    add_parser.add_argument("--tags", help="Comma-separated tags (e.g., work,personal)")

    # List notes command
    list_parser = subparsers.add_parser("list", help="List all notes")

    # View note command
    view_parser = subparsers.add_parser("view", help="View a specific note")
    view_parser.add_argument("note_id", type=int, help="Note ID to view")

    # Edit note command
    edit_parser = subparsers.add_parser("edit", help="Edit an existing note")
    edit_parser.add_argument("note_id", type=int, help="Note ID to edit")
    edit_parser.add_argument("content", help="New note content")
    edit_parser.add_argument("--tags", help="Comma-separated tags (e.g., work,personal)")

    # Delete note command
    delete_parser = subparsers.add_parser("delete", help="Delete a note")
    delete_parser.add_argument("note_id", type=int, help="Note ID to delete")

    # Search notes command
    search_parser = subparsers.add_parser("search", help="Search notes by keyword or tag")
    search_parser.add_argument("query", help="Keyword or tag to search for")

    args = parser.parse_args()

    try:
        noteflow = Noteflow()

        if args.command == "add":
            tags = args.tags.split(",") if args.tags else []
            noteflow.add_note(args.content, tags)
            print("Note added successfully")

        elif args.command == "list":
            notes = noteflow.list_notes()
            if not notes:
                print("No notes found")
            else:
                for note in notes:
                    tags = f" | Tags: {', '.join(note['tags'])}" if note.get('tags') else ""
                    print(f"ID: {note['id']} | Date: {note['date']} | {note['content'][:50]}...{tags}")

        elif args.command == "view":
            note = noteflow.get_note(args.note_id)
            if note:
                tags = f"Tags: {', '.join(note['tags'])}" if note.get('tags') else "No tags"
                print(f"ID: {note['id']}\nDate: {note['date']}\n{tags}\nContent: {note['content']}")
            else:
                raise NoteflowError(f"Note {args.note_id} not found")

        elif args.command == "edit":
            tags = args.tags.split(",") if args.tags else None
            if noteflow.edit_note(args.note_id, args.content, tags):
                print("Note edited successfully")
            else:
                raise NoteflowError(f"Note {args.note_id} not found")

        elif args.command == "delete":
            if noteflow.delete_note(args.note_id):
                print("Note deleted successfully")
            else:
                raise NoteflowError(f"Note {args.note_id} not found")

        elif args.command == "search":
            if not args.query.strip():
                raise NoteflowError("Search query cannot be empty")
            notes = noteflow.search_notes(args.query)
            if not notes:
                print(f"No notes found for query: {args.query}")
            else:
                for note in notes:
                    tags = f" | Tags: {', '.join(note['tags'])}" if note.get('tags') else ""
                    print(f"ID: {note['id']} | Date: {note['date']} | {note['content'][:50]}...{tags}")

        else:
            parser.print_help()

    except NoteflowError as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()