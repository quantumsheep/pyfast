import os
import sys
from parser.driver import parse
from typing import Any

from compiler.compiler import compile
from pyfast.command import Command


def command() -> Command:
    command = Command(
        name="build",
        description="PyFast Python compiler",
        func=run,
    )

    command.add_positional(name="filename", help="Python file to compile")
    command.add_flag(
        short="-v",
        long="--verbose",
        help="Enable verbose mode",
    )

    return command


def run(args: dict[str, Any]) -> None:
    filename: str = args["filename"]
    verbose: bool = args["verbose"]

    if not os.path.exists(filename):
        print(f"File {filename} does not exist")
        sys.exit(1)

    filename = os.path.relpath(filename, os.getcwd())

    try:
        ast = parse(filename)
        print(ast)
        print(compile(ast))
    except Exception as e:
        if verbose:
            raise e

        print(e)
        sys.exit(1)
