# ci/coverage.py
import os
import subprocess
import sys
import webbrowser
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def run_tests_with_coverage() -> subprocess.CompletedProcess:
    """Run pytest with coverage and return the process result."""
    logger.info("Running tests with coverage...")

    cmd = ["coverage", "run", "-m", "pytest", "tests"]
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=False
        )
        return result
    except subprocess.SubprocessError as e:
        logger.error(f"Failed to run tests: {e}")
        raise

def run_coverage() -> None:
    """Run coverage tests and check coverage percentage."""
    try:
        # Run tests with coverage
        coverage_run = run_tests_with_coverage()

        if coverage_run.returncode != 0:
            logger.error("Tests failed:")
            logger.error(coverage_run.stdout)
            logger.error(coverage_run.stderr)
            sys.exit(1)

        # Generate coverage report
        logger.info("Generating coverage report...")
        coverage_report = subprocess.run(
            ["coverage", "report"],
            capture_output=True,
            text=True
        )

        # Print full coverage report
        print(coverage_report.stdout)

        # Check coverage threshold
        coverage_check = subprocess.run(
            ["coverage", "report", "--fail-under=90"],
            capture_output=True,
            text=True
        )

        if coverage_check.returncode != 0:
            logger.error("Coverage is below 90%")
            sys.exit(1)

        logger.info("Coverage check passed!")

    except Exception as e:
        logger.error(f"An error occurred during coverage run: {e}")
        sys.exit(1)

def generate_coverage_report() -> None:
    """Generate HTML coverage report and open in browser."""
    try:
        run_coverage()

        logger.info("Generating HTML coverage report...")
        result = subprocess.run(
            ["coverage", "html"],
            capture_output=True,
            text=True,
            check=True
        )

        report_path = os.path.abspath("htmlcov/index.html")
        if os.path.exists(report_path):
            webbrowser.open(f"file://{report_path}")
            logger.info(f"Opened coverage report: {report_path}")
        else:
            logger.error(f"Coverage report not found at: {report_path}")
            sys.exit(1)

    except subprocess.CalledProcessError as e:
        logger.error(f"Error generating HTML report: {e.stderr}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Unexpected error generating HTML report: {e}")
        sys.exit(1)

if __name__ == "__main__":
    run_coverage()