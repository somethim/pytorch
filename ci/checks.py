import subprocess
import sys


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


def run_flake8() -> bool:
    """Run flake8 for linting."""
    return run_command(["poetry", "run", "flake8", "--max-line-length=100"], "flake8 linting")


def run_black() -> bool:
    """Run black formatter."""
    return run_command(["poetry", "run", "black", "."], "Black formatter")


def run_isort() -> bool:
    """Run isort to sort imports."""
    return run_command(["poetry", "run", "isort", "."], "isort")


def run_mypy() -> bool:
    """Run mypy type checking."""
    return run_command(["poetry", "run", "mypy", "."], "mypy type checking")


def run_pyright() -> bool:
    """Run pyright for type checking."""
    return run_command(
        ["poetry", "run", "pyright", "."], "pyright type checking"
    )


def run_lint() -> None:
    """Run all linters."""
    print("Running linters...\n")
    linters = [run_flake8, run_isort, run_black, run_mypy, run_pyright]

    for linter in linters:
        if not linter():
            sys.exit(1)

    print("\nAll linters passed!")
