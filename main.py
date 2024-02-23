#! /usr/bin/python3

import sys
from libs.commands import CommandManager
from os import mkdir, path


def init_subdirs():
    if not path.exists("rsrc"):
        mkdir("rsrc")

def main() -> int:
    init_subdirs()
    mngr: CommandManager = CommandManager()
    mngr.parse_args(sys.argv[1:])
    return 0

if __name__ == "__main__":
    main()
