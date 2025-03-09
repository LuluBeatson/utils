import pytest
from click.testing import CliRunner


@pytest.fixture
def runner():
    """Provide a Click CLI test runner.

    Given: A need to test Click CLI commands
    When: The fixture is requested
    Then: Returns a CliRunner that can:
        - Execute CLI commands in isolation
        - Capture command output
        - Return command exit codes
    """
    return CliRunner()


@pytest.fixture
def test_dir(tmp_path):
    """Provide a temporary directory for test files.

    Given: A need for temporary file storage during tests
    When: The fixture is requested
    Then: Returns a Path object that:
        - Points to a clean temporary directory
        - Is unique for each test
        - Gets automatically cleaned up after the test
    """
    return tmp_path


@pytest.fixture
def sample_images(test_dir):
    """Create sample PNG images for testing.

    Given: A need for test images
    When: The fixture is requested
    Then: Creates and returns paths to three test images:
        - Size: 100x100 pixels each
        - Color: Grayscale (rgb(0,0,0) to rgb(100,100,100))
        - Names: test_image_0.png through test_image_2.png
        - Location: All saved in test_dir
    """
    from PIL import Image

    images = []
    for i in range(3):
        color = f"rgb({i*50}, {i*50}, {i*50})"
        img = Image.new("RGB", (100, 100), color=color)
        path = test_dir / f"test_image_{i}.png"
        img.save(path)
        images.append(path)

    return images


@pytest.fixture
def mock_youtube_transcript(monkeypatch):
    """Mock YouTube transcript API responses."""

    def mock_get_transcript(*args, **kwargs):
        return [
            {"text": "First line", "start": 0.0, "duration": 2.0},
            {"text": "Second line", "start": 2.0, "duration": 2.0},
        ]

    from youtube_transcript_api import YouTubeTranscriptApi

    monkeypatch.setattr(YouTubeTranscriptApi, "get_transcript", mock_get_transcript)
