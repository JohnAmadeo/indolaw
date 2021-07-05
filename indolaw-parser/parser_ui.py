from typing import Any, Dict, List, Optional, Set, Union
from os import system, name
from termcolor import colored


def print_law(law: List[str]) -> None:
    for i, l in enumerate(law):
        print(f'[{i}] {l}\n')


def clear():
    # i.e Windows
    if name == 'nt':
        _ = system('cls')
    else:
        _ = system('clear')


def print_line():
    print('---------------')


def print_dashed_line():
    print('- - - - - - - -')


def print_yes_no():
    print(f"{colored('y', 'green')} / {colored('n', 'red')}")


def print_section_header(line):
    print(f"{colored('---------------', 'green')}")
    print()
    print(f"{colored(line, 'green')}")
    print()
    print(f"{colored('---------------', 'green')}")
