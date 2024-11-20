# todo: add environment variables


def main() -> None:
    """Main entry point of the application."""
    from ci.checks import run_lint

    run_lint()


if __name__ == "__main__":
    main()
