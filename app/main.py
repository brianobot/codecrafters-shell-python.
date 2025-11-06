import os
import shutil
import sys
from pathlib import Path


def main():
    # TODO: Uncomment the code below to pass the first stage
    while True:
        _ = sys.stdout.write("$ ")
        command = input()
        match command.split():
            case ["exit"]:
                exit()
            case ["exit", exit_code]:
                exit(int(exit_code))
            case ["echo", *values]:
                print(f"{' '.join(values)}")
            case ["type", command]:
                if command in ["echo", "exit", "type"]:
                    print(f"{command} is a shell builtin")
                    continue 
                
                found = False
                paths = os.environ.get("PATH").split(":")
                for path in paths:
                    file_exists = Path(f"{path}/{command}").exists()
                    if file_exists:
                        exec_path: str | None = shutil.which(command)
                        if exec_path  is not None:
                            print(f"{command} is {exec_path}")
                            found = True
                            break
                if not found:
                    print(f"{command}: not found")
            case _:
                print(f"{command}: command not found")


if __name__ == "__main__":
    main()
