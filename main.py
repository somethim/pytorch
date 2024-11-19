import sys

from ci.checks import run_lint


def main() -> None:
    run_lint()
    sys.exit(0)


if __name__ == "__main__":
    main()
