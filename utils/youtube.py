import click
from urllib.parse import urlparse, parse_qs
from youtube_transcript_api import YouTubeTranscriptApi


@click.group()
def youtube():
    """YouTube utility commands for transcription and summarization."""
    pass


@youtube.command()
@click.argument("url")
def transcribe(url):
    """Get the transcript of a YouTube video and print with timestamps"""
    transcript = get_transcript(url)
    print_transcript(transcript)


@youtube.command()
@click.argument("url")
def summarize(url):
    """Get a summary of a YouTube video"""
    transcript = get_transcript(url)
    summary = summarize_transcript(transcript)
    print(summary)


def get_transcript(url):
    video_id = url_to_id(url)
    transcript = YouTubeTranscriptApi.get_transcript(video_id)
    return transcript


def print_transcript(transcript: list[dict]):
    """Print the transcript with timestamps"""
    for line in transcript:
        start = format_time(line["start"])
        end = format_time(line["start"] + line["duration"])
        print(f"{start} - {end}\t{line['text']}")


def summarize_transcript(transcript):
    text = " ".join([line["text"] for line in transcript])

    # TODO: Invoke a langchain summarizer here
    return text


def url_to_id(url):
    """Extract the video id from a youtube url.

    There are two types of youtube urls:
    - https://www.youtube.com/watch?v=dQw4w9WgXcQ&other=params
    - https://youtu.be/dQw4w9WgXcQ?other=params
    """
    parsed_url = urlparse(url)
    if parsed_url.hostname == "youtu.be":
        return parsed_url.path[1:]
    elif parsed_url.hostname in ["www.youtube.com", "youtube.com"]:
        return parse_qs(parsed_url.query).get("v", [None])[0]
    return None


def format_time(seconds: float) -> str:
    """Convert seconds to a time string in the format of 00:00:00"""
    seconds = int(seconds)
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"


if __name__ == "__main__":
    youtube()
