import argparse
from noteflow import journal

def main():
    parser = argparse.ArgumentParser(description="Simple CLI Journal - NoteFlow")
    subparsers = parser.add_subparsers(dest="command")

    # Command to add a new journal entry
    add_parser = subparsers.add_parser("add", help="Add a new journal enyty")
    add_parser.add_argument("text", help="The journal text")

    # Command to list journal entries
    list_parser = subparsers.add_parser("list", help="List journal entries")

    args = parser.parse_args()

    if args.command == "add":
        journal.add_entry(args.text)
        print("Entry added.")
    elif args.command == "list":
        entries = journal.list_entries()
        for entry in entries:
            print(entry.strip())
    else:
        parser.print_help()