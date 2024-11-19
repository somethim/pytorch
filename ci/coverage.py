import logging
import os
import subprocess
import sys

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

CI_DIR = "ci"


def run_tests_with_coverage() -> None:
    """Run tests with coverage."""
    logger.info("Running tests with coverage...")

    cmd = [
        "pytest",
        "--cov=src",
        "--cov=main.py",
        "--cov-report=term-missing",
        f"--cov-report=xml:{CI_DIR}/coverage.xml",
        f"--cov-report=html:{CI_DIR}/htmlcov",
        "tests/",
    ]
    result = subprocess.run(
        cmd,
        text=True,
        stdout=sys.stdout,
        stderr=sys.stderr,
        env={**os.environ, "COVERAGE_FILE": f"{CI_DIR}/.coverage"}
    )

    if result.returncode != 0:
        logger.error("Tests failed.")
        sys.exit(result.returncode)

    logger.info("Tests passed!")


def generate_html_report() -> None:
    """Generate HTML coverage report."""
    logger.info("Generating HTML coverage report...")
    cmd = [
        "coverage",
        "html",
        f"--directory={CI_DIR}/htmlcov",
        "--coverage-file=/.coverage"
    ]
    result = subprocess.run(
        cmd, check=True, text=True, stdout=sys.stdout, stderr=sys.stderr
    )
    if result.returncode == 0:
        logger.info("HTML coverage report generated successfully!")


def check_coverage_threshold(threshold: int = 90) -> None:
    """Check if coverage meets the required threshold."""
    logger.info("Checking coverage threshold...")

    cmd = [
        "coverage",
        "report",
        f"--fail-under={threshold}",
        f"--coverage-file={CI_DIR}/.coverage"
    ]
    result = subprocess.run(
        cmd, text=True, stdout=sys.stdout, stderr=sys.stderr
    )

    if result.returncode != 0:
        logger.error(f"Coverage is below {threshold}%")
        sys.exit(result.returncode)

    logger.info("Coverage threshold met!")


def generate_coverage_report() -> None:
    """Run tests, generate reports, and check coverage."""
    logger.info("Starting generate_coverage_report()")
    run_tests_with_coverage()
    # generate_html_report()
    # check_coverage_threshold()
    logger.info("Coverage tasks completed successfully!")
    exit(0)
