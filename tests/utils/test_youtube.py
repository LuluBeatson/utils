from utils.youtube import youtube, format_time


def test_youtube_help(runner):
    """Test the YouTube command's help output.

    Given: A CLI runner for the YouTube command
    When: The help flag is provided (--help)
    Then: The output should:
        - Return success (exit code 0)
        - Show available commands section
        - List the 'transcribe' subcommand
        - List the 'summarize' subcommand
    """
    result = runner.invoke(youtube, ["--help"])
    assert result.exit_code == 0
    assert "Commands:" in result.output
    assert "transcribe" in result.output
    assert "summarize" in result.output


def test_transcribe_command(runner, mock_youtube_transcript):
    """Test the YouTube transcribe command.

    Given: A mock YouTube video URL and transcript data
    When: The transcribe command is run with the URL
    Then: The output should:
        - Return success (exit code 0)
        - Include timestamps (00:00:00)
        - Show the first line of transcript
        - Show the second line of transcript
    """
    result = runner.invoke(youtube, ["transcribe", "https://youtu.be/test"])
    assert result.exit_code == 0
    assert "00:00:00" in result.output
    assert "First line" in result.output
    assert "Second line" in result.output


def test_summarize_command(runner, mock_youtube_transcript):
    """Test the YouTube summarize command.

    Given: A mock YouTube video URL and transcript data
    When: The summarize command is run with the URL
    Then: The output should:
        - Return success (exit code 0)
        - Contain the concatenated transcript text
    """
    result = runner.invoke(youtube, ["summarize", "https://youtu.be/test"])
    assert result.exit_code == 0
    assert "First line Second line" in result.output


def test_format_time():
    """Test the time formatting utility.

    Given: Various time values in seconds
    When: Each value is passed to format_time()
    Then: Should return correctly formatted strings:
        - 0 seconds -> "00:00:00"
        - 61 seconds -> "00:01:01"
        - 3661 seconds -> "01:01:01"
    """
    assert format_time(0) == "00:00:00"
    assert format_time(61) == "00:01:01"
    assert format_time(3661) == "01:01:01"


def test_url_to_id():
    """Test YouTube URL parsing.

    Given: Various YouTube URL formats
    When: Each URL is passed to url_to_id()
    Then: Should extract the correct video ID:
        - Short URL (youtu.be)
        - Standard URL (youtube.com/watch)
        - Full URL (www.youtube.com/watch)
        - URL with query parameters
    """
    from utils.youtube import url_to_id

    assert url_to_id("https://youtu.be/abc123") == "abc123"
    assert url_to_id("https://youtube.com/watch?v=abc123") == "abc123"
    assert url_to_id("https://www.youtube.com/watch?v=abc123") == "abc123"
    test_url = "https://www.youtube.com/watch?v=abc123&other=params"
    assert url_to_id(test_url) == "abc123"
