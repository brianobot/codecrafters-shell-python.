import os
import sys
import shutil
import readline
import subprocess
from pathlib import Path

from .commands import cd, echo, run_command, _type
from .internals import tokenize_quote, make_completer, build_vocabulary


vocabulary = build_vocabulary()    

readline.parse_and_bind("tab: complete")
if sys.platform == "darwin":
    readline.parse_and_bind("bind ^I rl_complete")
readline.set_completer(make_completer(vocabulary))


def main():
    command_count = 0
    while True:
        user_input = input("$ ").strip()
        command_count += 1
        
        if (
            ">" in user_input 
            or "1>" in user_input 
            or "2>" in user_input 
            or ">>" in user_input 
            or "1>>" in user_input
            or "2>>" in user_input
            or "|" in user_input
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
            case ["history"]:
                for i in range(1, readline.get_current_history_length() + 1):
                    print(f"\t{i} {readline.get_history_item(i)}")
            case ["history", limit] if limit.isdigit():
                limit = int(limit)
                history_length = readline.get_current_history_length()
                current_index = (history_length - limit) + 1
                for i in range(current_index, history_length + 1):
                    print(f"\t{current_index} {readline.get_history_item(i)}")
                    current_index += 1
            case ["history", "-r", history_filepath]:
                readline.read_history_file(history_filepath)
            case ["history", "-w", history_filepath]:
                readline.write_history_file(history_filepath)
            case ["history", "-a", history_filepath]:
                readline.append_history_file(command_count, history_filepath)
                command_count = 0
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



