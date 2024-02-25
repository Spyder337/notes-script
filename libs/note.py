from os import mkdir, path

#   Takes in a name for a note and a path to a directory.
#   It returns a bool value representing successful file
#   creation.


def create_note(name: str, n_path: str) -> bool:
    """Creates an empty note file."""
    if (name == "" or n_path == ""):
        print("Name and Path must be non-null strings.")
        return False

    if (not path.exists(n_path)):
        mkdir(n_path)

    # File Name
    fn: str = f"{name}.md"
    # Note Path {Absolute}
    tmp = path.abspath(n_path)
    np: str = f"{tmp}/{fn}"

    with open(np, "w", encoding='utf-8') as f:
        f.write(f"# {name}")

    return True
