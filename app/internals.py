import os
from pathlib import Path
from typing import Callable


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
    

def make_completer(vocabulary) -> Callable[[str, int], str | None]:
    # https://docs.python.org/3/library/rlcompleter.html#rlcompleter.Completer
    def custom_complete(text, state):
        # None is returned for the end of the completion session.
        results = [x + " " for x in vocabulary if x.startswith(text)] + [None]

        # A space is added to the completion since the Python readline doesn't
        # do this on its own. When a word is fully completed we want to mimic
        # the default readline library behavior of adding a space after it.
        return results[state]
    return custom_complete


def build_vocabulary():
    paths = os.environ["PATH"].split(":")
    # print(f"{paths = }")
    
    vocab = set()
    for directory in paths:
        if not directory:
            continue

        p = Path(directory)
        if not p.is_dir():
            continue  # ghosts of PATH past

        for file in p.iterdir():
            # Pick only real executables (and skip directories)
            if file.is_file() and os.access(file, os.X_OK):
                vocab.add(file.name)

    return BUILTIN_CMDS.union(vocab)
    
    