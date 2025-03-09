import os
import pytest
from utils.dalle import dalle


def test_dalle_help(runner):
    """Test that the help command works."""
    result = runner.invoke(dalle, ["--help"])
    assert result.exit_code == 0
    assert "--prompt" in result.output
    assert "--quality" in result.output
    assert "--size" in result.output
