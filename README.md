# Utils

A collection of command-line utilities for various tasks including:

-   Image manipulation and grid creation
-   YouTube video transcription and summarization
-   Text summarization using LangChain
-   DALL-E image generation
-   Text-to-speech conversion

## Requirements

-   Python 3.11 or higher
-   OpenAI API key for DALL-E and summarization features
-   `venv` module (comes with Python)

## Installation

1. Clone the repository:

```bash
git clone <repository-url>
cd utils
```

2. Create and activate a project-specific virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate  # On Unix/macOS
# or .venv\Scripts\activate
```

The virtual environment isolates the project's dependencies from your system Python installation.

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Set up environment variables:

```bash
cp template.env .env
```

Then edit `.env` and add your OpenAI API key.

5. Install the package in development mode:

```bash
pip install -e .
```

## Available Commands

### Image Utilities

-   `image grid`: Create a grid from multiple images
    ```bash
    image grid --columns 2 --border-size 1 path/to/images/
    ```

### YouTube Utilities

-   `youtube transcribe`: Get video transcript
    ```bash
    youtube transcribe https://youtu.be/video_id
    ```
-   `youtube summarize`: Get video summary
    ```bash
    youtube summarize https://youtu.be/video_id
    ```

### Text Summarization

-   `summary`: Summarize text content
    ```bash
    summary "text to summarize"
    summary --objective "key points" "text to summarize"
    ```

### DALL-E Image Generation

-   `dalle`: Generate images using DALL-E
    ```bash
    dalle --prompt "your prompt here"
    dalle --prompt "your prompt" --size 1024 --quality hd
    ```

### Text-to-Speech

-   `tts`: Convert text to speech
    ```bash
    tts "text to convert"
    ```

## Development

Run tests:

```bash
pytest
```

## License

Personal use only. All rights reserved.
