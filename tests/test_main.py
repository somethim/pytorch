import main
from src.pytorch.core import some_function


def test_main_import() -> None:
    assert main is not None


def test_some_function() -> None:
    result = some_function()
    assert result is not None
