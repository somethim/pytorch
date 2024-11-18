import sys

from ci.checks import run_black, run_flake8, run_isort, run_mypy, run_pyright


def main() -> None:
    print("Running checks...\n")
    if not run_flake8():
        sys.exit(1)
    if not run_isort():
        sys.exit(1)
    if not run_black():
        sys.exit(1)
    if not run_mypy():
        sys.exit(1)
    if not run_pyright():
        sys.exit(1)
    print("\nAll checks passed!")

    sys.exit(0)


if __name__ == "__main__":
    main()
