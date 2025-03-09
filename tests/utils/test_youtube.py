import pytest
from utils.youtube import youtube, get_transcript, format_time


def test_youtube_help(runner):
    """Test that the help command works."""
    result = runner.invoke(youtube, ["--help"])
    assert result.exit_code == 0
    assert "Commands:" in result.output
    assert "transcribe" in result.output
    assert "summarize" in result.output


def test_transcribe_command(runner, mock_youtube_transcript):
    """Test the transcribe command with a mock video."""
    result = runner.invoke(youtube, ["transcribe", "https://youtu.be/test"])
    assert result.exit_code == 0
    assert "00:00:00" in result.output
    assert "First line" in result.output
    assert "Second line" in result.output


def test_summarize_command(runner, mock_youtube_transcript):
    """Test the summarize command with a mock video."""
    result = runner.invoke(youtube, ["summarize", "https://youtu.be/test"])
    assert result.exit_code == 0
    assert "First line Second line" in result.output


def test_format_time():
    """Test the time formatting function."""
    assert format_time(0) == "00:00:00"
    assert format_time(61) == "00:01:01"
    assert format_time(3661) == "01:01:01"


def test_url_to_id():
    """Test URL parsing."""
    from utils.youtube import url_to_id

    assert url_to_id("https://youtu.be/abc123") == "abc123"
    assert url_to_id("https://youtube.com/watch?v=abc123") == "abc123"
    assert url_to_id("https://www.youtube.com/watch?v=abc123") == "abc123"
    assert url_to_id("https://www.youtube.com/watch?v=abc123&other=params") == "abc123"
