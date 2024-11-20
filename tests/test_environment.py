import os
from pathlib import Path

import pytest

from src.pytorch.config.environment import (
    get_optional_env,
    get_required_env,
    load_environment,
)


@pytest.fixture
def temp_env_files(tmp_path):
    """Create temporary .env files for testing."""
    env_path = tmp_path / ".env"
    env_path.write_text("BASE_VAR=base_value\nSHARED_VAR=base_shared")

    env_local_path = tmp_path / ".env.local"
    env_local_path.write_text("LOCAL_VAR=local_value\nSHARED_VAR=local_shared")

    custom_env_path = tmp_path / "custom.env"
    custom_env_path.write_text("CUSTOM_VAR=custom_value\nSHARED_VAR=custom_shared")

    return {
        "base": env_path,
        "local": env_local_path,
        "custom": custom_env_path,
        "dir": tmp_path,
    }


@pytest.fixture(autouse=True)
def clear_env():
    """Clear relevant environment variables before and after each test."""
    original_env = dict(os.environ)

    for key in ["BASE_VAR", "LOCAL_VAR", "CUSTOM_VAR", "SHARED_VAR", "TEST_VAR"]:
        os.environ.pop(key, None)

    yield

    os.environ.clear()
    os.environ.update(original_env)


def test_load_environment_base(temp_env_files):
    """Test loading base .env file."""
    os.chdir(temp_env_files["dir"])
    load_environment()
    assert os.getenv("BASE_VAR") == "base_value"


def test_load_environment_local_override(temp_env_files):
    """Test that .env.local overrides .env."""
    os.chdir(temp_env_files["dir"])
    load_environment()
    assert os.getenv("SHARED_VAR") == "local_shared"


def test_load_environment_custom_path(temp_env_files):
    """Test loading a custom env file."""
    load_environment(temp_env_files["custom"])
    assert os.getenv("CUSTOM_VAR") == "custom_value"
    assert os.getenv("SHARED_VAR") == "custom_shared"


def test_load_environment_nonexistent_file():
    """Test loading a nonexistent env file."""
    load_environment(Path("nonexistent.env"))


def test_get_required_env():
    """Test getting a required environment variable."""
    os.environ["TEST_VAR"] = "test_value"
    assert get_required_env("TEST_VAR") == "test_value"


def test_get_required_env_missing():
    """Test getting a missing required environment variable."""
    with pytest.raises(ValueError) as exc_info:
        get_required_env("NONEXISTENT_VAR")
    assert "Required environment variable 'NONEXISTENT_VAR' is not set" in str(
        exc_info.value
    )


def test_get_optional_env_existing():
    """Test getting an existing optional environment variable."""
    os.environ["TEST_VAR"] = "test_value"
    assert get_optional_env("TEST_VAR") == "test_value"


def test_get_optional_env_missing():
    """Test getting a missing optional environment variable."""
    assert get_optional_env("NONEXISTENT_VAR", "default_value") == "default_value"


def test_get_optional_env_missing_no_default():
    """Test getting a missing optional environment variable with no default."""
    assert get_optional_env("NONEXISTENT_VAR") == ""


def test_load_environment_priority(temp_env_files):
    """Test that env files are loaded in the correct priority order."""
    os.chdir(temp_env_files["dir"])

    load_environment()
    assert os.getenv("SHARED_VAR") == "local_shared"

    load_environment(temp_env_files["custom"])
    assert os.getenv("SHARED_VAR") == "custom_shared"
