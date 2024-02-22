from os import curdir
import os

PATH_BLACKLIST = ("./.git", "./bin", "./.vscode")

#   Generate the README.md containing the notes ToC.
def create_toc(title: str) -> None:
    title = f"# {title}\n"
    desc = "Personal note repository\n"
    toc_txt = create_toc_txt()
    doc_txt = title
    doc_txt += desc
    doc_txt += toc_txt

    with open("README.md", "w") as f:
        f.write(doc_txt)

#   Generate the text representing the dir structure.
def create_toc_txt(base_level: int = 0) -> str:
    ret = ""

    for root, d, files in os.walk(curdir):
        if(root.startswith(PATH_BLACKLIST) or root == "."):
            continue
        #print(root)
        # First level is 0 since we ignore one degree of
        # seperators from the root
        base_level = root.replace(curdir, '').count(os.sep) - 1
        hd_name = os.path.basename(root)
        hd_name_len = len(hd_name)
        hd = "#" * (base_level + 1)
        ret +=f"{hd} {os.path.basename(root)}\n"
        if base_level == 0:
            div = "-" * (hd_name_len + len(hd) + 1)
            ret += f"{div}\n"

        for f in files:
            if is_valid_file(f):
                link_txt = f.rstrip(".md")
                link_ref = os.path.join(root, f)
                ret += f"- [{link_txt}]({link_ref})\n"

    return ret

def is_valid_dir(d_path: str) -> bool:
    return not d_path.startswith(PATH_BLACKLIST)

def is_valid_file(f_path: str) -> bool:
    return f_path.endswith(".md")
