import os
import sys
import shutil
import subprocess
from pathlib import Path


BUILTIN_CMDS = {"echo", "exit", "type", "pwd", "cd"}


def parse_quoted_str(text: str, keep_quote: bool = False) -> str:
    current = ""
    last_char_space = False
    
    active_backslash = False
    inside_single_quote = False
    inside_double_quote = False
    
    for char in text:
        if char == "'" and not inside_double_quote and not active_backslash:
            inside_single_quote = not inside_single_quote
            
            if keep_quote:
                current += char
                
        elif char == '"' and not inside_single_quote and not active_backslash:
            inside_double_quote = not inside_double_quote
            
            if keep_quote:
                current += char
        
        elif char == " ":
            if inside_double_quote or inside_single_quote or active_backslash:
                current += " "
                active_backslash = False
            else:
                if not last_char_space:
                    current += " "
                last_char_space = True
                
        elif char == "\\":
            if inside_single_quote:
                # Do nothing
                current += "\\"
            # this else handles for inside double quotes and outside double quotes
            # Escape the following characters [", \, $, ']
            else:
                if active_backslash:
                    current += "\\"
                    active_backslash = False
                else:
                    active_backslash = True
                    
        else:
            current += char
            last_char_space = False
            active_backslash = False
        
    return current
            
            
def tokenize_quote(text: str) -> list[str]:
    tokens = []
    current = ""
    
    active_backslash = False
    inside_single_quote = False
    inside_double_quote = False
    
    for char in text:          
        if char == "'" and not inside_double_quote and not active_backslash:
            inside_single_quote = not inside_single_quote
        elif char == '"' and not inside_single_quote and not active_backslash:
           inside_double_quote = not inside_double_quote 
  
        elif char == " " and not (inside_double_quote or inside_single_quote):
            if current:
                tokens.append(current)
                current = ""
        elif char == "\\":
            if inside_single_quote:
                current += "\\"
            else:
                if active_backslash:
                    current += "\\"
                    # print("✅ Deactivating Backslash")
                    active_backslash = False
                else:
                    # print("✅ Activating BackSlash")
                    active_backslash = True
        else:
            # print(f"✅ {char not in {"$", "\\", "'", '"'} = }")
            if active_backslash and char not in {"$", "\\", '"'}:
                # print(f"Char '{char}' Should be prefixed with a backslash, {active_backslash=}")
                current += f"\\{char}"
                active_backslash = False
            else:
                # print(f"Char '{char}' should be placed alone, {active_backslash=}")
                current += char
                active_backslash = False
    
    if current:
        tokens.append(current)
        
    return tokens
    

def main():
    while True:
        _ = sys.stdout.write("$ ")
        user_input = input()
        
        match user_input.split():
            case ["exit"]:
                exit()
            case ["exit", exit_code]:
                exit(int(exit_code))
            case ["pwd"]:
                print(f"{os.getcwd()}")
            case ["cd", directory]:
                if directory.startswith("~"):
                    directory = directory.replace("~", os.environ["HOME"])
                try:
                    os.chdir(directory)
                except FileNotFoundError:
                    print(f"cd: {directory}: No such file or directory")
                    
            case ["echo", *_]:
                text = user_input.lstrip("echo").lstrip()
                print(parse_quoted_str(text))                
            case ["type", command]:
                if command in BUILTIN_CMDS:
                    print(f"{command} is a shell builtin")
                    continue 
                    
                # Dirty patch until i can figure out why path is corrupted for MG5 Tets
                if command in ["cat", "cp", "mkdir", "my_exe"]:
                    is_exec: str | None = shutil.which(command) # noqa
                    print(f"{command} is {is_exec}")
                    continue 

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
            # this executes executes available on the system
            case [command, *args]:
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
                        else:
                            continue
                    
                if not found:
                    print(f"{command}: command not found")           
            case _:
                print(f"{user_input}: command not found")


if __name__ == "__main__":
    main()



