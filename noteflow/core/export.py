def export_entries(filepath, fmt="txt"):
    entries = _parse_entries()
    with open(filepath, "w") as f:
        for i, e in entries:
            if fmt == "md":
                f.write(f"## Entry #{i}\n\n{e}\n\n---\n\n")
            else:
                f.write(f"# {i}\n{'='*40}\n{e}\n{'='*40}\n\n")