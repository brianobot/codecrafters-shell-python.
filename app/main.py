import os
import sys
import shutil
import readline
import subprocess
from pathlib import Path


from .internals import tokenize_quote, make_completer
from .commands import cd, echo, run_command, _type

vocabulary = {'echo', 'exit'}
readline.parse_and_bind("tab: complete")
readline.parse_and_bind("bind ^I rl_complete")
readline.set_completer(make_completer(vocabulary))


def main():
    while True:
        _ = sys.stdout.write("$ ")
        user_input = input().strip()
        
        if (
            ">" in user_input 
            or "1>" in user_input 
            or "2>" in user_input 
            or ">>" in user_input 
            or "1>>" in user_input
            or "2>>" in user_input
        ):
            os.system(user_input)
            continue
        
        if user_input.startswith("'") or user_input.startswith('"'):
            args_list = tokenize_quote(user_input)    
            command, *args = args_list
            
            paths = os.environ["PATH"].split(":")
            found = False
            for path in paths:
                file_exists = Path(f"{path}/{command}").exists()
                if file_exists:
                    exec_path: str | None = shutil.which(command)
                    if exec_path is not None:
                        found = True
                        _ = subprocess.run([command] + args)
                        break
                
            if not found:
                print(f"{command}: command not found") 
            
            continue
            
        match user_input.split():
            case ["exit"]:
                exit()
            case ["exit", exit_code]:
                exit(int(exit_code))
            case ["pwd"]:
                print(f"{os.getcwd()}")
            case ["cd", directory]:
                cd(directory)
            case ["echo", *_]:
                echo(user_input)         
            case ["type", command]:
                _type(command)
            # this executes executes available on the system
            case [command, *_]:
                run_command(user_input, command)          
            case _:
                print(f"{user_input}: command not found")


if __name__ == "__main__":
    main()



