import argparse
from noteflow import journal

def main():
    parser = argparse.ArgumentParser(description="NoteFlow - A simple CLI journal")
    subparsers = parser.add_subparsers(dest="command")

    # Command to add a new journal entry
    add_parser = subparsers.add_parser("add", help="Add a new journal enyty")
    add_parser.add_argument("text", help="The journal entry body")
    add_parser.add_argument("-t", "--title", help="Optional title for the entry")

    # Command to list journal entries
    list_parser = subparsers.add_parser("list", help="List journal entries")
    list_parser.add_argument("--today", action="store_true", help="Show only today's entries")

    # Search command
    search_parser = subparsers.add_parser("search", help="Search entries by keyword")
    search_parser.add_argument("keyword", help="Keyword to search for")

    view_parser = subparsers.add_parser("view", help="View an entry by ID")
    view_parser.add_argument("id", type=int, help="ID of the entry to view")

    args = parser.parse_args()

    if args.command == "add":
        journal.add_entry(args.text, title=args.title)
        print("Entry added.")

    elif args.command == "list":
        entries = journal.today_entries() if args.today else journal.list_entries()
        for i, entry in entries:
            print(f"#{i}\n" + "=" * 40)
            print(entry)
            print("=" * 40)

    elif args.command == "search":
        matches = journal.search_entries(args.keyword)
        for i, entry in matches:
            print(f"#{i}\n" + "=" * 40)
            print(entry)
            print("=" * 40)
        if not matches:
            print("No matching entries found.")

    elif args.command == "view":
        entry = journal.get_entry_by_id(args.id)
        if entry:
            print(f"# {args.id}\n" + "=" * 40)
            print(entry)
            print("=" * 40)
        else:
            print("Entry not found.")

    else:
        parser.print_help()