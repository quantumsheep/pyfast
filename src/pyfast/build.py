import os
import sys
from parser import ast
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
    command.add_flag(
        long="--print-ast-tree",
        help="Print AST tree",
    )

    return command


def run(args: dict[str, Any]) -> None:
    filename: str = args["filename"]
    verbose: bool = args["verbose"]

    if not os.path.exists(filename):
        print(f"File {filename} does not exist")
        sys.exit(1)

    filename = os.path.abspath(filename)

    try:
        program_ast = parse(filename)

        if args["print_ast_tree"]:
            tree = ast.to_tree(program_ast)
            print(tree.show(stdout=False, sorting=False))

        print(compile(program_ast))
    except Exception as e:
        if verbose:
            raise e

        print(e)
        sys.exit(1)
