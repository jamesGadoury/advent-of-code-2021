#!/bin/bash

if [ ! -n "$1" ]; 
then
    echo "Need to supply day #"
    exit
fi

DAY_DIR="day-$1/"
mkdir $DAY_DIR
touch "$DAY_DIR/sample_input.txt"
cat << EOF > "$DAY_DIR/main.py"
# https://adventofcode.com/2021/day/$1

import sys

def main(args):
    if len(args) != 2:
        print('Need to provide file input')
        return

if __name__ == '__main__':
    main(sys.argv)
EOF

google-chrome https://adventofcode.com/2021/day/$1
