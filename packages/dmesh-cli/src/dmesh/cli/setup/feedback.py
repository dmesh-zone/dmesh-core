"""Feedback abstractions for the dm init command."""

from typing import Protocol

import typer


class Feedback(Protocol):
    def step(self, message: str) -> None: ...
    def success(self, message: str) -> None: ...
    def error(self, message: str) -> None: ...


from rich.console import Console

class ConsoleFeedback:
    def __init__(self) -> None:
        self.console = Console()
        self.current_status = None

    def step(self, message: str) -> None:
        if self.current_status:
            self.current_status.stop()
        # 'dots' is a 6-frame braille spinner, similar to npm
        self.current_status = self.console.status(f"[blue]{message}[/blue]", spinner="dots")
        self.current_status.start()

    def success(self, message: str) -> None:
        if self.current_status:
            self.current_status.stop()
            self.current_status = None
        self.console.print(f"[green]{message}[/green]")

    def error(self, message: str) -> None:
        if self.current_status:
            self.current_status.stop()
            self.current_status = None
        self.console.print(f"[red]{message}[/red]")



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
