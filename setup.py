from setuptools import setup, find_packages



# All the metadata that are expected to be reused should go here.

name: str = "vacuumworld"
version: str = "4.2.0"
description: str = "VacuumWorld: an agent platform for cleaning robots."
author: list = ["Benedict Wilkins", "Nausheen Saba", "Emanuele Uliana", "Joel Clarke"]
author_email: str = "brjw@hotmail.co.uk"
license: str = "GNU3"
classifiers: list = [
      "Programming Language :: Python :: 3",
      "Programming Language :: Python :: 3.8",
      "Programming Language :: Python :: 3.9",
      "Programming Language :: Python :: 3 :: Only",
      "Development Status :: 3 - Alpha",
      "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
      "Operating System :: OS Independent",
]
url: str = "https://github.com/dicelab-rhul/vacuumworld"
wiki: str = url + "/wiki"
issues: str = url + "/issues"
dependencies: list = ["pystarworldsturbo>=1.0.3", "pillow", "wheel", "ipython", "screeninfo"]

# End of metadata


setup(
      name=name,
      version=version,
      description=description,
      url=url,
      wiki=wiki,
      issues=issues,
      author=author,
      author_email=author_email,
      license=license,
      packages=find_packages(),
      include_package_data=True,
      install_requires=dependencies,
      classifiers=classifiers
)
