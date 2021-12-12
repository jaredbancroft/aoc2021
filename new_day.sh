#!/bin/bash

if [ $# -ne 1 ]; then
    echo "Please specify the AoC day"
    exit 1
fi

DAY=$1

BASE_DIR="/workspaces/aoc2021"

DAY_DIR="${BASE_DIR}/days/${DAY}"

INPUTS_DIR="${BASE_DIR}/inputs"

if [ -d ${DAY_DIR} ]; then
    echo "Day already exists"
    exit 1
fi

echo "Creating ${DAY_DIR}"
mkdir ${DAY_DIR}

FILES=("__init__.py" "part1.py" "part2.py")

for file in ${FILES[@]}; do
    echo "Creating ${DAY_DIR}/${file}"
    touch "${DAY_DIR}/${file}"
done

echo "Creating ${INPUTS_DIR}/${DAY}.txt"
touch "${INPUTS_DIR}/${DAY}.txt"