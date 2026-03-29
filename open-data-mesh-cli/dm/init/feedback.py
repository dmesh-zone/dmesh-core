"""Feedback abstractions for the dm init command."""

from typing import Protocol

import typer


class Feedback(Protocol):
    def step(self, message: str) -> None: ...
    def success(self, message: str) -> None: ...
    def error(self, message: str) -> None: ...


class ConsoleFeedback:
    def step(self, message: str) -> None:
        typer.echo(typer.style(message, fg=typer.colors.BLUE))

    def success(self, message: str) -> None:
        typer.echo(typer.style(message, fg=typer.colors.GREEN))

    def error(self, message: str) -> None:
        typer.echo(typer.style(message, fg=typer.colors.RED))


class CapturingFeedback:
    def __init__(self) -> None:
        self.steps: list[str] = []
        self.successes: list[str] = []
        self.errors: list[str] = []

    def step(self, message: str) -> None:
        self.steps.append(message)

    def success(self, message: str) -> None:
        self.successes.append(message)

    def error(self, message: str) -> None:
        self.errors.append(message)
