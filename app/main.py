import sys


def main():
    # TODO: Uncomment the code below to pass the first stage
    while True:
        _ = sys.stdout.write("$ ")
        command = input()
        match command.split():
            case ["exit", exit_code]:
                exit(int(exit_code))
            case _:
                print(f"{command}: command not found")


if __name__ == "__main__":
    main()
