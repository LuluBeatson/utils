from utils.dalle import dalle


def test_dalle_help(runner):
    """Test the DALL-E command's help output.

    Given: A CLI runner for the DALL-E command
    When: The help flag is provided (--help)
    Then: The output should:
        - Return success (exit code 0)
        - Show the --prompt option
        - Show the --quality option
        - Show the --size option
    """
    result = runner.invoke(dalle, ["--help"])
    assert result.exit_code == 0
    assert "--prompt" in result.output
    assert "--quality" in result.output
    assert "--size" in result.output
