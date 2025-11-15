import os
import sys
import shutil
import subprocess
from pathlib import Path
from termios import PARMRK

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
            
            
# def tokenize_quote(text: str) -> list[str]:
#     tokens = []
#     current = ""
    
#     inside_single_quote = False
#     inside_double_quote = False
    
#     for char in text:  
#         if char == "'" and not inside_double_quote:
#             inside_single_quote = not inside_single_quote
#         elif char == '"' and not inside_single_quote:
#            inside_double_quote = not inside_double_quote 
  
#         elif char == " " and not (inside_double_quote or inside_single_quote):
#             if current:
#                 tokens.append(current)
#                 current = ""
#         else:
#             current += char
    
    
#     if current:
#         tokens.append(current)
        
#     return tokens
        
        
def tokenize_quote(text: str) -> list[str]:
    tokens = []
    current = []
    in_single = False
    in_double = False
    escaped = False

    for ch in text:
        if escaped:
            current.append(ch)
            escaped = False
        elif ch == "\\":
            escaped = True
            current.append(ch)
        elif ch == "'" and not in_double:
            in_single = not in_single
            current.append(ch)
        elif ch == '"' and not in_single:
            in_double = not in_double
            current.append(ch)
        elif ch.isspace() and not in_single and not in_double:
            if current:
                tokens.append("".join(current))
                current = []
        else:
            current.append(ch)
    if current:
        tokens.append("".join(current))
    
    return tokens


def main():
    # TODO: Uncomment the code below to pass the first stage
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
                
                found = False
                paths = os.environ["PATH"].split(":")
                for str_path in paths:
                    file_exists = Path(str_path).joinpath("command").exists()
                    if file_exists:
                        is_exec: str | None = shutil.which(command)
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



