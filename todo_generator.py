#!/usr/bin/env python3



from typing import List

import os



INTERESTING_FILES_EXTENSIONS: List[str] = [".py"]
EXCLUSION_LIST: List[str] = [os.path.basename(__file__)]
TODO_FILE: str = "TODO.md"
TODO_PATTERN: str = "TODO"
TODO_HEADER: str = "# List of TODOs"


def main() -> None:
    lines: List[str] = []

    for dir, _, files in os.walk(os.getcwd()):
        for f in filter(lambda candidate: any(filter(lambda ext: candidate.endswith(ext), INTERESTING_FILES_EXTENSIONS)), files):
            if not f in EXCLUSION_LIST:
                lines += look_for_todos(os.path.join(dir, f))

    
    with open(TODO_FILE, "w") as f:
        f.write(TODO_HEADER + "\n\n")

        for l in lines:
            f.write(l + "\n")

        f.flush()


def look_for_todos(path: str) -> List[str]:
    to_add: List[str] = []
    prefix: str = "* File {} - line ".format(path)
    lines: List[str] = []

    with open(path, "r") as f:
        lines = f.readlines()

    for i in range(len(lines)):
        line_number = i + 1

        if TODO_PATTERN in lines[i]:
            to_add.append(prefix + "{}: `{}`".format(line_number, lines[i].strip()))

    return to_add


if __name__ == "__main__":
    main()
