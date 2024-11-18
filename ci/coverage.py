import os
import subprocess
import sys
import webbrowser


def run_coverage() -> None:
    """Run coverage tests and check coverage percentage."""
    print("Running coverage tests...")

    # Run tests with coverage
    coverage_run = subprocess.run(
        ["coverage", "run", "-m", "pytest"],
        capture_output=True,
        text=True
    )

    # If tests fail, exit immediately
    if coverage_run.returncode != 0:
        print("Tests failed:")
        print(coverage_run.stdout)
        print(coverage_run.stderr)
        sys.exit(1)

    # Generate coverage report
    coverage_report = subprocess.run(
        ["coverage", "report"],
        capture_output=True,
        text=True
    )

    # Print full coverage report
    print(coverage_report.stdout)

    # Exit if coverage is below threshold
    coverage_check = subprocess.run(
        ["coverage", "report", "--fail-under=90"],
        capture_output=True,
        text=True
    )

    if coverage_check.returncode != 0:
        print("Coverage is below 90%")
        sys.exit(1)

    print("Coverage passed!")


def generate_coverage_report() -> None:
    """Generate HTML coverage report."""
    run_coverage()

    print("Generating HTML coverage report...")
    try:
        result = subprocess.run(["coverage", "html"], capture_output=True, text=True)
        if result.returncode != 0:
            print(f"Error generating HTML report: {result.stderr}")
            sys.exit(1)
        print("HTML coverage report generated!")
        report_path = os.path.abspath("htmlcov/index.html")
        webbrowser.open(f"file://{report_path}")
        print(f"Opened coverage report: {report_path}")

    except Exception as e:
        print(f"Unexpected error generating HTML report: {e}")
        sys.exit(1)
