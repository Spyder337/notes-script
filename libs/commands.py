from typing import Callable
from libs.toc import create_toc

from libs.note import create_note

class CommandArgs:
    num_vals:       int = 0
    val_desc:       list[str] = []
    variable_len:   bool

    def __init__(self, num_vals: int, val_desc: list[str], variable_len: bool = False):
        self.num_vals = num_vals
        self.val_desc = val_desc
        self.variable_len = variable_len

class Command:
    flag: str
    args: CommandArgs
    desc: str
    cmd_exec: Callable[..., None]

    def __init__(self, flag: str, desc: str, cmd_exec: Callable[..., None], args: CommandArgs):
        self.flag = flag
        self.desc = desc
        self.args = args
        self.cmd_exec = cmd_exec
    
    def execute(self, cmd_mngr: "CommandManager" ,args: ...):
        if (not self.args.variable_len and args.__len__() == self.args.num_vals):
            self.cmd_exec(cmd_mngr, args)
        elif (self.args.variable_len):
            self.cmd_exec(cmd_mngr, args)
        else:
            print("Invalid number of arguments.")
            self.help_msg()
    
    def help_msg(self) -> str:
        ret_str = ""
        ret_str += f"CMD Flag: {self.flag}\n"
        ret_str += f"Desc: {self.desc}\n"
        if(self.args.num_vals != 0):
            ret_str += f"Usage: {self.flag} "
            for val in self.args.val_desc:
                ret_str += f"\"{val}\" "
            ret_str += "\n"
        ret_str += "\n"
        return ret_str

class CommandManager:
    cmds: dict[str, Command]

    def __init__(self):
        self.generate_commands()
    
    def parse_args(self, args: ...):
        if (self.cmds.__contains__(args[0])):
            flag = args[0]
            self.cmds[flag].execute(self, args[1:])

    def generate_commands(self):
        self.cmds: dict[str, Command] = {}
        # Command Definitions
        help_args = CommandArgs(1, ["FLAG: str"], True)
        help_cmd = Command("-h", "Outputs a list of commands.", help_exec, help_args)
        self.cmds[help_cmd.flag] = help_cmd

        nn_args: CommandArgs = CommandArgs(2, ["Note name: str", "Note path: str"])
        nn_cmd: Command = Command("-n", 
            """Creates a new note with the title provided.""", new_note_exec, nn_args)
        self.cmds[nn_cmd.flag] = nn_cmd

        gr_args = CommandArgs(1, ["Document Title: str"])
        gr_cmd = Command("-gr", "Generates a README.md with a table of contents", gr_exec, gr_args)
        self.cmds[gr_cmd.flag] = gr_cmd

#   Callbacks
def help_exec(cmd_mngr: CommandManager, args: ...):
    if len(args) == 0:
        print("Commands: ")
        for cmd in cmd_mngr.cmds.values():
            print(cmd.help_msg(), end='')
    elif cmd_mngr.cmds.__contains__(args[0]):
        flag = args[0]
        print(f"Command Help: {flag}")
        print(cmd_mngr.cmds[flag].help_msg(), end='')
    else:
        print("Invalid arguments.\nNone for all commands. Command flag for specific help.")

def gr_exec(cmd_mngr: CommandManager, args: ...):
    create_toc(args[0])

def new_note_exec(cmd_mngr: CommandManager, args: ...):
    create_note(args[0], args[1])

def test_callback():
    print("Called successfully.")
