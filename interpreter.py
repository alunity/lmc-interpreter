import sys

# Overwrite builtin "compile"
from compiler import compile

from executor import execute

code: list[str] = []

with open(sys.argv[1], "r") as file:
    # Read line by line by as opposed to reading it all at once
    # Using a method like file.readlines() is only suitable for files which can fit entirely into memory
    for line in file:
        # strip removes new line
        # Case insensitive
        code.append(line.strip().lower())

execute(compile(code), "-d" in sys.argv)
