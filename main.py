import sys
from libs.menu import Menu, parse_args
from libs.menus.notes import notes_menu


def main() -> int:
    menu: Menu = notes_menu()
    parse_args(menu, sys.argv[1:])
    return 0


if __name__ == "__main__":
    main()
