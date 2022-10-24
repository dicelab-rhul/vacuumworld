#!/usr/bin/env python3

from shutil import rmtree
from typing import List

import os


def main() -> None:
    pycache_dir_names: List[str] = ["__pycache__", ".pytest_cache"]

    for dir, subdir, _ in os.walk(os.getcwd()):
        for pycache_dir_name in pycache_dir_names:
            if pycache_dir_name in subdir:
                rmtree(os.path.join(dir, pycache_dir_name))
            elif pycache_dir_name in dir:
                rmtree(dir)


if __name__ == "__main__":
    main()
