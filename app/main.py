import sys


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
                else:
                    print(f"{command}: not found")
            case _:
                print(f"{command}: command not found")


if __name__ == "__main__":
    main()
