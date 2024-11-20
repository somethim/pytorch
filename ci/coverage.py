import os
import subprocess
import sys


def generate_coverage_report() -> None:
    """Run tests with coverage."""
    ci_dir = "ci"
    cmd = [
        "pytest",
        "--cov=src",
        "--cov=main",
        "--cov-config=pyproject.toml",
        "--cov-report=term-missing",
        f"--cov-report=html:{ci_dir}/htmlcov",
        "tests/",
    ]
    result = subprocess.run(
        cmd,
        text=True,
        stdout=sys.stdout,
        stderr=sys.stderr,
        env={**os.environ, "COVERAGE_FILE": f"{ci_dir}/.coverage"},
    )

    if result.returncode != 0:
        print("Tests failed.")
        sys.exit(result.returncode)
