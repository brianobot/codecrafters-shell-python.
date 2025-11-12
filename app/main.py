import os
import sys
import shutil
import argparse
import subprocess
from pathlib import Path


global_parser = argparse.ArgumentParser()


def parse_single_quoted_str(text: str, keep_quote: bool = False) -> str:
    index = 0
    current = ""
    inside_quote = False
    last_char_space = False
    
    while index < len(text):
        char = text[index]
        
        if char == "'":
            inside_quote = not inside_quote
            if keep_quote:
                current += "'"
        elif char == " ":
            if inside_quote:
                current += " "
            else:
                if not last_char_space:
                    current += " "
                last_char_space = True
        else:
            current += char
            last_char_space = False
        
        index += 1
        
    return current
            
            
def tokenize_single_quote(text: str) -> list[str]:
    tokens = []
    current = ""
    inside_quote = False
    index = 0
    
    while index < len(text):
        char  = text[index]
            
        if char == "'":
            inside_quote = not inside_quote
        elif char.isspace() and not inside_quote:
            if current:
                tokens.append(current)
                current = ""
        else:
            current += char
        
        index += 1
    
    if current:
        tokens.append(current)
        
    return tokens
        

def main():
    # TODO: Uncomment the code below to pass the first stage
    while True:
        _ = sys.stdout.write("$ ")
        user_input = input()
        
        match user_input.split():
            case ["cd", directory]:
                if directory.startswith("~"):
                    directory = directory.replace("~", os.environ["HOME"])
                try:
                    os.chdir(directory)
                except FileNotFoundError:
                    print(f"cd: {directory}: No such file or directory")
            case ["exit"]:
                exit()
            case ["pwd"]:
                print(f"{os.getcwd()}")
            case ["exit", exit_code]:
                exit(int(exit_code))
            case ["echo", *_]:
                text = user_input.lstrip("echo").lstrip()
                print(parse_single_quoted_str(text))                
            case ["type", command]:
                if command in ["echo", "exit", "type", "pwd", "cd"]:
                    print(f"{command} is a shell builtin")
                    continue 
                
                found = False
                paths = os.environ["PATH"].split(":")
                for path in paths:
                    file_exists = Path(f"{path}/{command}").exists()
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
                
                refined_args = parse_single_quoted_str(args, keep_quote=True)
                args_list = tokenize_single_quote(refined_args)
                
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
