from utils.langchain.summary import main


def test_summary_help(runner):
    """Test the summary command's help output.

    Given: A CLI runner for the summary command
    When: The help flag is provided (--help)
    Then: The output should:
        - Return success (exit code 0)
        - Show the --objective option
    """
    result = runner.invoke(main, ["--help"])
    assert result.exit_code == 0
    assert "--objective" in result.output


def test_basic_summary(runner):
    """Test basic text summarization.

    Given: A simple test text to summarize
    When: The summary command is run with just the text
    Then: The output should:
        - Return success (exit code 0)
        - Start with the expected header ('\nSUMMARY:\n\n')
        - Contain a non-empty summary
        - Have content beyond just the header
    """
    test_text = "This is a test text that needs to be summarized."
    result = runner.invoke(main, [test_text])

    # Check that the command executed successfully
    assert result.exit_code == 0
    # Check that the output has the expected structure
    assert result.output.startswith("\nSUMMARY:\n\n")
    # Check that we got some non-empty output
    assert len(result.output.strip()) > len("\nSUMMARY:\n")


def test_summary_with_objective(runner):
    """Test summarization with a specific objective.

    Given:
        - A simple test text to summarize
        - An objective of finding 'key points'
    When: The summary command is run with both text and objective
    Then: The output should:
        - Return success (exit code 0)
        - Start with the expected header ('\nSUMMARY:\n\n')
        - Contain a non-empty summary
        - Include reference to the objective in the output
    """
    test_text = "This is a test text that needs to be summarized."
    objective = "key points"
    result = runner.invoke(main, ["--objective", objective, test_text])

    # Check that the command executed successfully
    assert result.exit_code == 0
    # Check that the output has the expected structure
    assert result.output.startswith("\nSUMMARY:\n\n")
    # Check that we got some non-empty output
    assert len(result.output.strip()) > len("\nSUMMARY:\n")
    # Check that the objective influenced the output
    assert objective.lower() in result.output.lower()
