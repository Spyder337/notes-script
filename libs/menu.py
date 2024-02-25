from typing import Callable
from subprocess import call


#   TODO: Handle OS specific cases for references to call


class CommandArgs:
    """Contains basic information for a command."""
    num_vals:       int = 0
    val_desc:       list[str] = []
    variable_len:   bool

    def __init__(self, num_vals: int, val_desc: list[str], variable_len: bool = False):
        self.num_vals = num_vals
        self.val_desc = val_desc
        self.variable_len = variable_len


class Command:
    """Represents a callable Menu Command"""
    flag: str
    args: CommandArgs
    desc: str
    cmd_exec: Callable[..., None]

    def __init__(self, flag: str, desc: str, cmd_exec: Callable[..., None], args: CommandArgs):
        self.flag = flag
        self.desc = desc
        self.args = args
        self.cmd_exec = cmd_exec


def help_msg(cmd: Command) -> str:
    """Returns the commands help message."""
    ret_str = ""
    ret_str += f"CMD Flag: {cmd.flag}\n"
    ret_str += f"Desc: {cmd.desc}\n"
    if cmd.args.num_vals != 0:
        ret_str += f"Usage: {cmd.flag} "
        for val in cmd.args.val_desc:
            ret_str += f"\"{val}\" "
        ret_str += "\n"
    ret_str += "\n"
    return ret_str


def can_execute(cmd: Command, args: ...) -> bool:
    """Checks if the arguments are valid for the command."""
    # print("can_execute")
    # print(f"Vairable Len:   {self.args.variable_len}")
    # print(f"Min Args:       {self.args.num_vals}")
    # print(f"Args Passed In: {len(args)}")
    if (not cmd.args.variable_len and len(args) == cmd.args.num_vals):
        return True
    if cmd.args.variable_len:
        return True
    return False


class Menu:
    """Represents a Menu accessed by cmd keys."""
    cmds: dict[str, Command] = {}
    sub_menus: dict[str, "Menu"] = {}


# Menu Builders


def execute(cmd: Command, menu: "Menu", args: ...):
    """Calls the execute function if valid args are passed in."""
    if can_execute(cmd, args):
        cmd.cmd_exec(menu, args)
    else:
        print("Invalid number of arguments.")
        help_msg(cmd)


def generate_help() -> Command:
    """Creates a help command."""
    help_args = CommandArgs(1, ["FLAG: str"], True)
    help_cmd = Command("-h", "Outputs a list of commands.",
                       help_exec, help_args)
    return help_cmd


def init_cmd_dict(menu: Menu) -> None:
    """Initializes a new command dictionary with a help command."""
    menu: dict[str, Command] = {}
    help_cmd = generate_help()
    menu[help_cmd.flag] = help_cmd


def parse_args(menu: Menu, args: ...):
    """Execute valid commands."""
    if args[0] in menu.cmds:
        flag = args[0]
        menu.cmds[flag].cmd_exec(menu, args[1:])


# Common Callbacks


def help_exec(menu: Menu, args: ...):
    """Help execute function."""
    if len(args) == 0:
        print("Commands: ")
        for cmd in menu.cmds.values():
            print(help_msg(cmd), end='')
    elif args[0] in menu.cmds:
        flag = args[0]
        print(f"Command Help: {flag}")
        print(help_msg(menu.cmds[flag]), end='')
    else:
        print("Invalid arguments.\nNone for all commands. Command flag for specific help.")


# Build2 Command Calls


def shell_call(cmd: str):
    """Wrapper for suprocess.call with the shell arg set to True."""
    call(cmd, shell=True)
