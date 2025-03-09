import pytest
from utils.langchain.summary import main


def test_summary_help(runner):
    """Test that the help command works."""
    result = runner.invoke(main, ["--help"])
    assert result.exit_code == 0
    assert "--objective" in result.output


def test_basic_summary(runner):
    """Test basic text summarization."""
    test_text = "This is a test text that needs to be summarized."
    result = runner.invoke(main, [test_text])

    # Check that the command executed successfully
    assert result.exit_code == 0
    # Check that the output has the expected structure
    assert result.output.startswith("\nSUMMARY:\n\n")
    # Check that we got some non-empty output
    assert len(result.output.strip()) > len("\nSUMMARY:\n")


def test_summary_with_objective(runner):
    """Test summarization with a specific objective."""
    test_text = "This is a test text that needs to be summarized."
    objective = "key points"
    result = runner.invoke(main, ["--objective", objective, test_text])

    # Check that the command executed successfully
    assert result.exit_code == 0
    # Check that the output has the expected structure
    assert result.output.startswith("\nSUMMARY:\n\n")
    # Check that we got some non-empty output
    assert len(result.output.strip()) > len("\nSUMMARY:\n")
    # Check that the objective influenced the output (if implemented)
    assert objective.lower() in result.output.lower()
