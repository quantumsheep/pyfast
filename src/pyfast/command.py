from __future__ import annotations

import argparse
from dataclasses import dataclass, field
from typing import Any, Callable


@dataclass(kw_only=True)
class Argument:
    short: str | None = None
    long: str
    type: argparse._ActionType
    help: str
    default: Any = None
    action: str = "store"


@dataclass(kw_only=True)
class Command:
    name: str
    description: str

    func: Callable[[dict[str, str]], None]

    _arguments: list[Argument] = field(default_factory=list)
    _subcommands: dict[str, Command] = field(default_factory=dict)

    def add_positional(
        self,
        *,
        name: str,
        help: str,
        type: argparse._ActionType = str,
        default: Any = None,
    ) -> None:
        self._arguments.append(
            Argument(
                short=None,
                long=name,
                type=type,
                help=help,
                default=default,
            )
        )

    def add_flag(
        self,
        *,
        short: str | None = None,
        long: str,
        help: str,
    ) -> None:
        self._arguments.append(
            Argument(
                short=short,
                long=long,
                type=bool,
                help=help,
                action="store_true",
            )
        )

    def add_subcommand(self, subcommand: Command) -> None:
        self._subcommands[subcommand.name] = subcommand

        # if not self.subparser:
        #     self.subparser = self.parser.add_subparsers(dest="subparser")

        # subparsers = self.subparser.add_parser()

    def parse(
        self, parser: argparse.ArgumentParser | None = None
    ) -> argparse.ArgumentParser:
        if parser is None:
            parser = argparse.ArgumentParser(
                prog=self.name,
                description=self.description,
            )

        for argument in self._arguments:
            names = list(filter(None, [argument.short, argument.long]))

            if argument.action == "store_true":
                parser.add_argument(
                    *names,
                    help=argument.help,
                    action=argument.action,
                )
            else:
                parser.add_argument(
                    *names,
                    type=argument.type,
                    help=argument.help,
                    default=argument.default,
                    action=argument.action,
                )

        if self._subcommands:
            subparsers = parser.add_subparsers(dest="subcommand", required=True)

            for subcommand in self._subcommands.values():
                subparser = subparsers.add_parser(
                    subcommand.name,
                    description=subcommand.description,
                )

                subcommand.parse(subparser)

        return parser

    def run(self) -> None:
        parser = self.parse()
        args = vars(parser.parse_args())
        subcommand = args.pop("subcommand", None)

        if subcommand:
            self._subcommands[subcommand].func(args)
        else:
            self.func(args)
