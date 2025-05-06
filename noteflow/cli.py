import argparse
from noteflow.core import journal, export
from noteflow.config import get_journal_path

def main():
    parser = argparse.ArgumentParser(description="NoteFlow - A simple CLI journal")
    sub = parser.add_subparsers(dest="command")

    sub.add_parser("list").add_argument("--today", action="store_true")
    sub.add_parser("search").add_argument("keyword")
    sub.add_parser("view").add_argument("id", type=int)
    sub.add_parser("delete").add_argument("id", type=int)

    add = sub.add_parser("add")
    add.add_argument("text")
    add.add_argument("-t", "--title")

    exp = sub.add_parser("export")
    exp.add_argument("filepath")
    exp.add_argument("--format", choices=["txt", "md"], default="txt")

    args = parser.parse_args()

    if args.command == "add":
        journal.add_entry(args.text, args.title)
        print("Entry added.")

    elif args.command == "list":
        entries = journal.today_entries() if args.today else journal.list_entries()
        for i, e in entries:
            print(f"#{i}\n{'='*40}\n{e}\n{'='*40}")

    elif args.command == "search":
        for i, e in journal.search_entries(args.keyword):
            print(f"#{i}\n{'='*40}\n{e}\n{'='*40}")

    elif args.command == "view":
        entry = journal.get_entry_by_id(args.id)
        print(f"# {args.id}\n{'='*40}\n{entry}\n{'='*40}" if entry else "Entry not found.")

    elif args.command == "delete":
        deleted = journal.delete_entry_by_id(args.id)
        print(f"Entry #{args.id} deleted." if deleted else "Entry not found.")

    elif args.command == "export":
        export.export_entries(journal.list_entries(), args.filepath, args.format)
        print(f"Exported to {args.filepath} as {args.format}.")

    else:
        parser.print_help()
        print(f"Journal file: {get_journal_path()}")