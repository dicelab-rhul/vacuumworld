from setuptools import setup, find_packages
from json import load
from typing import Any, cast

import os


# All reusable metadata should go here.

name: str = "vacuumworld"
description: str = "VacuumWorld: an agent platform for cleaning robots."
author: str = ", ".join(["Emanuele Uliana", "Benedict Wilkins", "Nausheen Saba", "Joel Clarke", "Kostas Stathis"])
author_email: str = "vw@dicelab-rhul.org"
license: str = "GNU3"
classifiers: list[str] = [
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
    "Programming Language :: Python :: 3 :: Only",
    "Development Status :: 4 - Beta",
    "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    "Operating System :: OS Independent",
]
dependencies: list[str] = [
    "pystarworldsturbo>=1.2.8",
    "pillow",
    "wheel",
    "ipython",
    "pytest",
    "screeninfo",
    "tk",
    "requests",
    "playsound",
    "pyjoptional>=1.1.2",
    "pymonitors>=1.0.2"
]

# End of static metadata

CONFIG_FILE_PATH: str = os.path.join(os.path.dirname(os.path.abspath(__file__)), "vacuumworld", "config.json")

with open(CONFIG_FILE_PATH, "r") as f:
    # The type of config is dict[str, Any] because JSONValue is defined in a dependency that is meant to be installed with this package.
    config: dict[str, Any] = load(fp=f)

    version: str = cast(str, config["version_number"])
    url: str = cast(str, config["project_repo_url"])

# End of metadata

setup(
    name=name,
    version=version,
    description=description,
    url=url,
    author=author,
    author_email=author_email,
    license=license,
    packages=find_packages(),
    include_package_data=True,
    install_requires=dependencies,
    classifiers=classifiers
)
