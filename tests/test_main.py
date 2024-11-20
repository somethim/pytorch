from unittest.mock import patch

import main
from src.pytorch.core import some_function


def test_main():
    with patch("ci.checks.run_lint") as mock_run_lint:
        main.main()
        mock_run_lint.assert_called_once()


def test_some_function() -> None:
    result = some_function()
    assert result is not None
