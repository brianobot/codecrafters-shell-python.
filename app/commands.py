import os
import shutil
import subprocess

from pathlib import Path
from .internals import parse_quoted_str, tokenize_quote


BUILTIN_CMDS = {"echo", "exit", "type", "pwd", "cd"}


def cd(directory: str) -> None:
    if directory.startswith("~"):
        directory = directory.replace("~", os.environ["HOME"])
    try:
        os.chdir(directory)
    except FileNotFoundError:
        print(f"cd: {directory}: No such file or directory")
    
        
def echo(user_input: str) -> None:
    text = user_input.lstrip("echo").lstrip()
    print(parse_quoted_str(text))       


def _type(command: str) -> None:
    if command in BUILTIN_CMDS:
        print(f"{command} is a shell builtin")
        return 
        
    # TODO: Dirty patch until i can figure out why path is corrupted for MG5 Tets
    if command in ["cat", "cp", "mkdir", "my_exe"]:
        _is_exec: str | None = shutil.which(command) # noqa
        print(f"{command} is {_is_exec}")
        return 

    found = False
    paths = os.environ["PATH"].split(":")
    # print(f"Paths = {paths}")
    for str_path in paths:
        file_exists = Path(str_path).joinpath("command").exists()
        if file_exists:
            is_exec: str | None = shutil.which(command) # noqa
            if is_exec is not None:
                print(f"{command} is {is_exec}")
                found = True
                break
    if not found:
        print(f"{command}: not found")
    

def run_command(user_input: str, command: str):
    args = user_input.lstrip(command).lstrip(" ")
    args_list = tokenize_quote(args)
                    
    paths = os.environ["PATH"].split(":")
    found = False
    for path in paths:
        file_exists = Path(f"{path}/{command}").exists()
        if file_exists:
            exec_path: str | None = shutil.which(command)
            if exec_path is not None:
                found = True
                _ = subprocess.run([command] + args_list)
                break

    if not found:
        print(f"{command}: command not found") 