#!/usr/bin/env python3

from shutil import rmtree

import os



def main() -> None:
    pycache_dir_name: str = "__pycache__"

    for dir, subdir, _ in os.walk("."):
        if pycache_dir_name in subdir:
            rmtree(os.path.join(dir, pycache_dir_name))
        elif pycache_dir_name in dir:
            rmtree(dir)


if __name__ == "__main__":
    main()
