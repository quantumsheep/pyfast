from typing import Any

from pyfast import build
from pyfast.command import Command


def main():
    command = Command(
        name="pyfast",
        description="PyFast Python compiler",
        func=run,
    )

    command.add_subcommand(build.command())

    command.run()


def run(args: dict[str, Any]) -> None:
    pass


if __name__ == "__main__":
    main()
