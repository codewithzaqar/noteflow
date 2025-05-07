import argparse
import sys
import logging
from datetime import datetime
from .noteflow import Noteflow, NoteflowError

# Configure logging
logging.basicConfig(
    filename="logs/noteflow.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def main():
    parser = argparse.ArgumentParser(description="Noteflow CLI")
    subparsers = parser.add_subparsers(dest="command")

    # Add note command
    add_parser = subparsers.add_parser("add", help="Add a new note")
    add_parser.add_argument("content", help="Note content")
    add_parser.add_argument("--tags", help="Comma-separated tags (e.g., work,personal)")

    # List notes command
    list_parser = subparsers.add_parser("list", help="List all notes")
    list_parser.add_argument("--start-date", help="Filter notes after this date (YYYY-MM-DD)")
    list_parser.add_argument("--end-date", help="Filter notes before this date (YYYY-MM-DD)")

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
    delete_parser.add_argument("--force", action="store_true", help="Skip confirmation prompt")

    # Search notes command
    search_parser = subparsers.add_parser("search", help="Search notes by keyword or tag")
    search_parser.add_argument("query", help="Keyword or tag to search for")
    search_parser.add_argument("--start-date", help="Filter notes after this date (YYYY-MM-DD)")
    search_parser.add_argument("--end-date", help="Filter notes before this date (YYYY-MM-DD)")

    args = parser.parse_args()

    try:
        noteflow = Noteflow()

        if args.command == "add":
            tags = args.tags.split(",") if args.tags else []
            noteflow.add_note(args.content, tags)
            print("Note added successfully")
            logging.info(f"Added note with content: {args.content[:50]}...")

        elif args.command == "list":
            start_date = args.start_date if args.start_date else None
            end_date = args.end_date if args.end_date else None
            notes = noteflow.list_notes(start_date, end_date)
            if not notes:
                print("No notes found")
            else:
                for note in notes:
                    tags = f" | Tags: {', '.join(note['tags'])}" if note.get('tags') else ""
                    print(f"ID: {note['id']} | Date: {note['date']} | {note['content'][:50]}...{tags}")
            logging.info("Listed notes")

        elif args.command == "view":
            note = noteflow.get_note(args.note_id)
            if note:
                tags = f"Tags: {', '.join(note['tags'])}" if note.get('tags') else "No tags"
                print(f"ID: {note['id']}\nDate: {note['date']}\n{tags}\nContent: {note['content']}")
                logging.info(f"Viewed note ID: {args.note_id}")
            else:
                raise NoteflowError(f"Note {args.note_id} not found")

        elif args.command == "edit":
            tags = args.tags.split(",") if args.tags else None
            if noteflow.edit_note(args.note_id, args.content, tags):
                print("Note edited successfully")
                logging.info(f"Edited note ID: {args.note_id}")
            else:
                raise NoteflowError(f"Note {args.note_id} not found")

        elif args.command == "delete":
            if not args.force:
                confirm = input(f"Are you sure you want to delete note {args.note_id}? (y/n): ").lower()
                if confirm != 'y':
                    print("Deletion cancelled")
                    logging.info(f"Deletion cancelled for note ID: {args.note_id}")
                    return
            if noteflow.delete_note(args.note_id):
                print("Note deleted successfully")
                logging.info(f"Deleted note ID: {args.note_id}")
            else:
                raise NoteflowError(f"Note {args.note_id} not found")

        elif args.command == "search":
            if not args.query.strip():
                raise NoteflowError("Search query cannot be empty")
            start_date = args.start_date if args.start_date else None
            end_date = args.end_date if args.end_date else None
            notes = noteflow.search_notes(args.query, start_date, end_date)
            if not notes:
                print(f"No notes found for query: {args.query}")
            else:
                for note in notes:
                    tags = f" | Tags: {', '.join(note['tags'])}" if note.get('tags') else ""
                    print(f"ID: {note['id']} | Date: {note['date']} | {note['content'][:50]}...{tags}")
            logging.info(f"Searched notes with query: {args.query}")

        else:
            parser.print_help()

    except NoteflowError as e:
        print(f"Error: {str(e)}")
        logging.error(f"NoteflowError: {str(e)}")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        logging.error(f"Unexpected error: {str(e)}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main()