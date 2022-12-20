#!/usr/bin/env python3

'''
Please run this file as ./todo_generator.py from within its parent directory.
Otherwise, the paths will not be generated/printed correctly.
'''

from typing import List

import os


INTERESTING_FILES_EXTENSIONS: List[str] = [".py"]
FILES_EXCLUSION_LIST: List[str] = [os.path.basename(__file__)]
DIR_EXCLUSION_LIST: List[str] = ["examples_not_to_commit"]
TODO_FILE: str = "TODO.md"
TODO_PATTERN: str = "TODO"
TODO_HEADER: str = "# List of TODOs"


def main() -> None:
    lines: List[str] = []

    for dir, _, files in os.walk(os.getcwd()):
        if os.path.basename(dir) in DIR_EXCLUSION_LIST:
            continue

        for f in filter(lambda candidate: any(filter(lambda ext: isinstance(ext, str) and candidate.endswith(ext), INTERESTING_FILES_EXTENSIONS)), files):
            if f not in FILES_EXCLUSION_LIST:
                lines += __look_for_todos(os.path.join(dir, f))

    with open(TODO_FILE, "w") as f:
        f.write(TODO_HEADER + "\n")

        if len(lines) > 0:
            f.write("\n")

        for line in lines:
            f.write(line + "\n")

        f.flush()


def __look_for_todos(path: str) -> List[str]:
    to_add: List[str] = []
    path_to_print: str = __get_relative_path(absolute_path=path)
    prefix: str = "* File {} - line ".format(path_to_print)
    lines: List[str] = []

    with open(path, "r") as f:
        lines = f.readlines()

    for i in range(len(lines)):
        line_number = i + 1

        if TODO_PATTERN in lines[i]:
            to_add.append(prefix + "{}: `{}`".format(line_number, lines[i].strip().replace("`", "'")))

    return to_add


def __get_relative_path(absolute_path: str) -> str:
    tokens: List[str] = absolute_path.split(os.path.sep)
    vw_top_dir: str = os.path.basename(os.getcwd())

    while tokens[0] != vw_top_dir:
        tokens = tokens[1:]

        if len(tokens) < 2:
            raise ValueError("Malformed path: {}".format(absolute_path))

    tokens = tokens[1:]

    return os.path.join(*tokens)


if __name__ == "__main__":
    main()
