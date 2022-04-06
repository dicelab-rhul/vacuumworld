from setuptools import setup, find_packages
from json import load

import os



# All reusable metadata should go here.

name: str = "vacuumworld"
version: str = "TO_OVERRIDE_PROGRAMMATICALLY"
description: str = "VacuumWorld: an agent platform for cleaning robots."
author: list = ["Emanuele Uliana", "Benedict Wilkins", "Nausheen Saba", "Joel Clarke", "Kostas Stathis"]
author_email: str = "vw@[R.E.M.O.V.E.T.H.I.S]dicelab-rhul.org"
license: str = "GNU3"
classifiers: list = [
      "Programming Language :: Python :: 3",
      "Programming Language :: Python :: 3.8",
      "Programming Language :: Python :: 3.9",
      "Programming Language :: Python :: 3.10",
      "Programming Language :: Python :: 3 :: Only",
      "Development Status :: 4 - Beta",
      "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
      "Operating System :: OS Independent",
]
url: str = "https://github.com/dicelab-rhul/vacuumworld"
dependencies: list = ["pystarworldsturbo>=1.0.5", "pillow", "wheel", "ipython", "screeninfo", "tk"]

# End of static metadata

CONFIG_FILE_PATH: str = os.path.join(os.path.dirname(os.path.abspath(__file__)), "vacuumworld", "config.json")

with open(CONFIG_FILE_PATH, "r") as f:
      config: dict = load(fp=f)
      version = config["version_number"]

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
