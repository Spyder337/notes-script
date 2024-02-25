import os

from libs.menu import Command, CommandArgs, Menu, help_exec
from libs.note import create_note
from libs.toc import create_dir_toc


def notes_menu() -> Menu:
    """Creates a menu populated with commands related to notes."""
    menu = Menu()
    menu.cmds: dict[str, Command] = {}
    # Command Definitions
    help_args = CommandArgs(1, ["FLAG: str"], True)
    help_cmd = Command("-h", "Outputs a list of commands.",
                       help_exec, help_args)
    menu.cmds[help_cmd.flag] = help_cmd

    nn_args: CommandArgs = CommandArgs(2, ["Note name: str", "Note path: str"])
    nn_cmd: Command = Command("-n",
                              """Creates a new note with the title provided.""", new_note_exec, nn_args)
    menu.cmds[nn_cmd.flag] = nn_cmd

    gr_args = CommandArgs(1, ["Document Title: str"])
    gr_cmd = Command(
        "-gr", "Generates a README.md with a table of contents", gr_exec, gr_args)
    menu.cmds[gr_cmd.flag] = gr_cmd

    return menu


def gr_exec(menu: Menu, args: ...) -> None:
    """Execute function to generate README.md files."""
    create_dir_toc(title=args[0], is_readme=True)


def st_exec(menu: Menu, args: ...) -> None:
    """Execute function to generate directory ToC.md files."""
    d_path = args[0]
    for r, d, _ in os.walk(d_path):
        level = r.replace(d_path, '').count(os.sep) - 1
        if level == 0:
            create_dir_toc(d_path, "Table of Contents", False)


def new_note_exec(menu: Menu, args: ...) -> None:
    """Execute function to generate new notes."""
    create_note(args[0], args[1])
