from pyfast import build, run
from pyfast.command import Command


def main():
    command = Command(
        name="pyfast",
        description="PyFast Python compiler",
        func=lambda _: None,
    )

    command.add_subcommand(build.command())
    command.add_subcommand(run.command())

    command.run()


if __name__ == "__main__":
    main()
