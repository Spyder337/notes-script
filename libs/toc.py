from os import curdir
import os

PATH_BLACKLIST = ("./.git", "./bin", "./.vscode")
README_DESC = "Personal note repository\n"

#   Generate the README.md containing the notes ToC.


class ToCEntry:
    """Represents an item in the Table of Contents."""
    name: str = ""
    path: str = ""

    def __init__(self, name: str = "", path: str = ""):
        self.name = name
        self.path = path

    def __lt__(self, other) -> bool:
        return self.path < other.path

    def __gt__(self, other) -> bool:
        return self.path > other.path

    def __eq__(self, other) -> bool:
        return self.path == other.path


def create_dir_toc(d_path: str = curdir, title: str = "Table of Contents", is_readme=False) -> None:
    """Creates a README.md with the subdirs and files represented in a
table of contents format."""
    title = f"# {title}\n"
    toc_txt = dir_toc_txt(d_path)
    doc_txt = title

    if is_readme:
        doc_txt += README_DESC

    doc_txt += toc_txt

    with open("README.md", "w", encoding='utf-8') as f:
        f.write(doc_txt)


def dir_toc_txt(d_path: str) -> str:
    """Creates the text for a directory table of contents."""
    ret = ""

    for root, d, files in os.walk(d_path):
        if (root.startswith(PATH_BLACKLIST) or root == "."):
            continue
        # First level is 0 since we ignore one degree of
        # seperators from the root
        base_level = root.replace(d_path, '').count(os.sep) - 1
        hd_name = os.path.basename(root)
        hd_name_len = len(hd_name)
        hd = "#" * (base_level + 1)
        ret += f"{hd} {os.path.basename(root)}\n"
        if base_level == 0:
            div = "-" * (hd_name_len + len(hd) + 1)
            ret += f"{div}\n"

        for f in files:
            if is_valid_file(f):
                link_txt = f.rstrip(".md")
                link_ref = os.path.join(root, f)
                ret += f"- [{link_txt}]({link_ref})\n"

    return ret


def get_toc_entries(lines: list[str]) -> list[ToCEntry]:
    """Get the toc entries from a list of strings."""

    hdrs: list[ToCEntry] = []
    in_code_block = False
    hdr_path = ""
    level = 1
    for line in lines:

        if line.startswith("```"):
            in_code_block = not in_code_block

        if in_code_block:
            continue

        line = str.strip(line)
        is_hdr_line = line.startswith("#")

        if not is_hdr_line:
            continue

        line_len = len(line)
        start = line.index(' ') + 1
        hdr_name = line[start:line_len]
        new_level = 0
        for c in line:
            if c == '#':
                new_level += 1

        if new_level == 1:
            hdr_path = hdr_name
            hdrs.append(ToCEntry(hdr_name, hdr_path))
        elif new_level < level:
            hdr_parts = hdr_path.split('/')
            hdr_path = ""
            diff = level - new_level
            for p in hdr_parts[0, (len(hdr_parts) - diff)]:
                hdr_path += p
            hdr_path += f"/{hdr_name}"
            hdrs.append(ToCEntry(hdr_name, hdr_path))
        else:
            hdr_path += f"/{hdr_name}"
            hdrs.append(ToCEntry(hdr_name, hdr_path))
        level = new_level

    return hdrs


def note_toc_txt(n_path: str) -> str:
    """Reads a note file and generates a toc for it."""
    hdrs: list[ToCEntry] = []
    hdr_lines: list[str] = []
    txt: str = "# Table of Contents\n-----------------\n"

    with open(n_path, 'r+', encoding='utf-8') as f:
        lines = f.readlines()
        hdrs = get_toc_entries(lines[1:])

    for hdr in hdrs:
        level = hdr.path.count('/') + 1
        prfx = "#" * level
        hdr_l = f"{prfx} [{hdr.name}]({hdr.path})"
        if level == 1:
            hdr_l_len = len(hdr_l)
            div = "-" * hdr_l_len
            hdr_l += f"\n{div}"
        hdr_lines.append(hdr_l)

    for l in hdr_lines:
        txt += f"{l}\n"

    return txt


def insert_note_toc(n_path: str, txt: str) -> None:
    """Insert or Update a table of contents in a note file."""
    #   TODO: Check if the file has a table of contents
    #   TODO: Cache data section of a note file
    #   TODO: Modify document text
    #   TODO: Output to file
    pass


def is_valid_dir(d_path: str) -> bool:
    """Checks if a directory starts with the PATH_BLACKLIST"""
    return not d_path.startswith(PATH_BLACKLIST)


def is_valid_file(f_path: str) -> bool:
    """Checks if a file ends in markdown format."""
    return f_path.endswith(".md")
