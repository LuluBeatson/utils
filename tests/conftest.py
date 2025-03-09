import os
import pytest
from click.testing import CliRunner


@pytest.fixture
def runner():
    """Fixture for testing Click commands."""
    return CliRunner()


@pytest.fixture
def test_dir(tmp_path):
    """Create a temporary directory for test files."""
    return tmp_path


@pytest.fixture
def sample_images(test_dir):
    """Create sample PNG images for testing."""
    from PIL import Image

    # Create three sample images
    images = []
    for i in range(3):
        img = Image.new("RGB", (100, 100), color=f"rgb({i*50}, {i*50}, {i*50})")
        path = test_dir / f"test_image_{i}.png"
        img.save(path)
        images.append(path)

    return images


@pytest.fixture
def mock_openai_response(monkeypatch):
    """Mock OpenAI API responses."""

    class MockResponse:
        def __init__(self):
            self.data = [type("obj", (), {"url": "http://example.com/image.png"})]

    def mock_generate(*args, **kwargs):
        return MockResponse()

    from openai import OpenAI

    monkeypatch.setattr(OpenAI, "images", type("obj", (), {"generate": mock_generate}))


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
