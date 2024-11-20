import os
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv


def load_environment(env_path: Optional[Path] = None) -> None:
    """
    Load environment variables from .env files
    Priority: .env.local > .env

    Args:
        env_path: Optional path to environment file
    """
    # Default paths
    env_local = Path(".env.local")
    env_default = Path(".env")

    # Load .env first (base configuration)
    if env_default.exists():
        load_dotenv(env_default)

    # Load .env.local second (overrides .env)
    if env_local.exists():
        load_dotenv(env_local, override=True)

    # Load specific env file if provided
    if env_path and env_path.exists():
        load_dotenv(env_path, override=True)


def get_required_env(key: str) -> str:
    """
    Get a required environment variable or raise an error

    Args:
        key: Environment variable name

    Returns:
        str: Environment variable value

    Raises:
        ValueError: If environment variable is not set
    """
    value = os.getenv(key)
    if value is None:
        raise ValueError(f"Required environment variable '{key}' is not set")
    return value


def get_optional_env(key: str, default: str = "") -> str:
    """
    Get an optional environment variable with a default value

    Args:
        key: Environment variable name
        default: Default value if not set

    Returns:
        str: Environment variable value or default
    """
    return os.getenv(key, default)
