# All the metadata that are expected to be reused should go here.

name: str = "vacuumworld"
version: str = "4.1.8"
description: str = ""
author: str = "Benedict Wilkins"
authors: list = ["Benedict Wilkins", "Nausheen Saba", "Emanuele Uliana"]
authors_short : list = ["ben", "nausheen", "cloudstrife9999"]
author_email: str = "brjw@hotmail.co.uk"
license: str = "GNU3"
classifiers: list = [
        "Programming Language :: Python :: 3.7",
        "Development Status :: 2 - Pre-Alpha",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
      ]
url: str = "https://github.com/dicelab-rhul/vacuumworld"
wiki: str = url + "/wiki"
dependencies: list = ["pystarworlds>=0.0.3", "pillow"]
