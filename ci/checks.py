import subprocess
import sys
from dataclasses import dataclass
from typing import List


@dataclass
class LintCommand:
    description: str
    check_command: List[str]
    fix_command: List[str] | None = None

    def should_fix(self, fix_mode: bool) -> List[str]:
        """Return the appropriate command based on fix mode."""
        return self.fix_command if (fix_mode and self.fix_command) else self.check_command


def run_command(command: list[str], description: str) -> bool:
    """Run a shell command and print its output."""
    print(f"Running {description}...")
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"{description} failed:")
        print(result.stdout)
        print(result.stderr)
        return False
    print(f"{description} passed!")
    return True


def get_linters() -> List[LintCommand]:
    """Get all linter commands with their fix modes."""
    return [
        LintCommand(
            "flake8 linting",
            ["poetry", "run", "flake8", "--max-line-length=100"],
            # flake8 doesn't have a fix mode
            None,
        ),
        LintCommand(
            "Black formatter",
            ["poetry", "run", "black", "--check", "."],
            ["poetry", "run", "black", "."],
        ),
        LintCommand(
            "isort",
            ["poetry", "run", "isort", "--check-only", "."],
            ["poetry", "run", "isort", "."],
        ),
        LintCommand(
            "mypy type checking",
            ["poetry", "run", "mypy", "."],
            # mypy doesn't have a fix mode
            None,
        ),
        LintCommand(
            "pyright type checking",
            ["poetry", "run", "pyright", "."],
            # pyright doesn't have a fix mode
            None,
        ),
    ]


def run_lint(fix: bool = False) -> None:
    """Run all linters.

    Args:
        fix: If True, will attempt to fix issues where possible
    """
    mode = "fixing" if fix else "checking"
    print(f"Running linters in {mode} mode...\n")

    linters = get_linters()

    for linter in linters:
        command = linter.should_fix(fix)
        if not run_command(command, linter.description):
            sys.exit(1)

    print("\nAll linters passed!")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Run linting checks with optional fixing")
    parser.add_argument(
        "--fix",
        action="store_true",
        help="Attempt to automatically fix issues where possible",
    )

    args = parser.parse_args()
    run_lint(fix=args.fix)