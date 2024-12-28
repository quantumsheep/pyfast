import os
import sys
from parser.driver import parse
from compiler.compiler import compile


def main():
    files = sys.argv[1:]

    for i, file in enumerate(files):
        if not os.path.exists(file):
            print(f"File {file} does not exist")
            sys.exit(1)

        files[i] = os.path.relpath(file, os.getcwd())

    asts = parse(files)

    for ast in asts:
        print(ast)
        print(compile(ast))


if __name__ == "__main__":
    main()
