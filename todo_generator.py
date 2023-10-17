#!/usr/bin/env python3

'''
Please run this file as ./todo_generator.py from within its parent directory.
Otherwise, the paths will not be generated/printed correctly.
'''

import os


TODO_FILE: str = "TODO.md"
INTERESTING_FILES_EXTENSIONS: list[str] = [".py", ".md", ".txt", ".sh", ".json"]
FILES_EXCLUSION_LIST: list[str] = [os.path.basename(__file__), TODO_FILE]
DIR_EXCLUSION_LIST_PREFIX: str = os.path.dirname(os.path.dirname(__file__))
DIR_EXCLUSION_LIST: list[str] = [os.path.join(DIR_EXCLUSION_LIST_PREFIX, directory) for directory in ["examples_not_to_commit", "build", ".git"]]
TODO_PATTERN: str = "TODO:"
TODO_HEADER: str = "# List of TODOs"


def main() -> None:
    lines: list[str] = []

    for d, _, files in os.walk(os.getcwd()):
        if any([d.startswith(excluded_dir) for excluded_dir in DIR_EXCLUSION_LIST]):
            continue

        for f in filter(lambda candidate: any([candidate.endswith(ext) for ext in INTERESTING_FILES_EXTENSIONS]), files):
            if f not in FILES_EXCLUSION_LIST:
                lines += __look_for_todos(os.path.join(d, f))

    with open(TODO_FILE, "w") as f:
        f.write(TODO_HEADER + "\n")

        if len(lines) > 0:
            f.write("\n")

        for line in lines:
            f.write(line + "\n")

        f.flush()


def __look_for_todos(path: str) -> list[str]:
    to_add: list[str] = []
    path_to_print: str = __get_relative_path(absolute_path=path)
    prefix: str = "* File {} - line ".format(path_to_print)
    lines: list[str] = []

    with open(path, "r") as f:
        lines = f.readlines()

    for i in range(len(lines)):
        line_number = i + 1

        if TODO_PATTERN in lines[i]:
            to_add.append(prefix + "{}: `{}`".format(line_number, lines[i].strip().replace("`", "'")))

    return to_add


def __get_relative_path(absolute_path: str) -> str:
    tokens: list[str] = absolute_path.split(os.path.sep)
    vw_top_dir: str = os.path.basename(os.getcwd())

    while tokens[0] != vw_top_dir:
        tokens = tokens[1:]

        if len(tokens) < 2:
            raise ValueError("Malformed path: {}".format(absolute_path))

    tokens = tokens[1:]

    return os.path.join(*tokens)


if __name__ == "__main__":
    main()
