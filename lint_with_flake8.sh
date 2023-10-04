#!/usr/bin/env bash

FLAKE8=flake8

if ! command -v $FLAKE8 &> /dev/null ; then
    echo "${FLAKE8} could not be found."
    exit
else
    $FLAKE8 . --count --exit-zero --max-complexity=10 --max-line-length=512 --statistics
fi
