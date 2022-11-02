#!/bin/bash

INVENV=$(python -c 'import sys; print ("1" if sys.prefix != sys.base_prefix else "0")')

if [[ ${INVENV} -eq 0 ]] ; then
    echo "No virtual environment active, exiting without updating VacuumWorld."

    exit 1
else
    echo "Virtualenv active, proceeding."

    git pull
    pip install .
    ./pycache_cleaner.py
    rm -rf build
    rm -rf dist
    rm -rf vacuumworld.egg-info

    echo
    echo "VacuumWorld version: $(pip list | grep vacuumworld | rev | cut -d' ' -f1)"
fi
