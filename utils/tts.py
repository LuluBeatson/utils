import os
import io
import pyaudio
import requests
import soundfile as sf
import dotenv
import click

dotenv.load_dotenv()


@click.command()
@click.option(
    "-m", "--model", default="tts-1", help="The model, one of: tts-1, tts-1-hd"
)
@click.option(
    "-v",
    "--voice",
    default="alloy",
    help="A voice, one of: alloy, echo, fable, onyx, nova, shimmer",
)
@click.option(
    "-s",
    "--speed",
    default=1.0,
    help="The speed of the generated audio. A value between 0.25 and 4.0",
)
@click.option(
    "-o",
    "--output-file",
    default=None,
    help="Save the audio to a file. Allowed extensions: mp3, flac, opus, acc",
)
@click.argument("input_text")
def tts(input_text, model="tts-1", voice="alloy", speed=1.0, output_file=None):
    """Text to speech using OpenAI's API

    https://platform.openai.com/docs/guides/text-to-speech
    """
    url = "https://api.openai.com/v1/audio/speech"
    headers = {
        "Authorization": f'Bearer {os.getenv("OPENAI_API_KEY")}',
    }

    # if output_file, infer response_format from file extension
    if output_file:
        response_format = output_file.split(".")[-1]
        assert response_format in ["mp3", "flac", "opus", "acc"]
    else:
        response_format = "opus"  # needed for realtime playback

    data = {
        "model": model,
        "input": input_text,
        "voice": voice,
        "speed": speed,
        "response_format": response_format,
    }

    # If an output_file is specified, make a non-streaming request and save the
    # response to the file. Otherwise, stream the response to pyaudio for realtime
    if output_file:
        with requests.post(url, headers=headers, json=data) as response:
            if response.status_code == 200:
                with open(output_file, "wb") as file:
                    file.write(response.content)
            else:
                print(f"Error: {response.status_code} - {response.text}")
        return

    audio = pyaudio.PyAudio()
    with requests.post(url, headers=headers, json=data, stream=True) as response:
        if response.status_code == 200:
            buffer = io.BytesIO()
            for chunk in response.iter_content(chunk_size=4096):
                buffer.write(chunk)

            buffer.seek(0)

            if output_file:
                with open(output_file, "wb") as file:
                    file.write(buffer.read())
            else:
                with sf.SoundFile(buffer, "r") as sound_file:
                    format = pyaudio.paInt16
                    channels = sound_file.channels
                    rate = sound_file.samplerate

                    stream = audio.open(
                        format=format, channels=channels, rate=rate, output=True
                    )
                    chunk_size = 1024
                    data = sound_file.read(chunk_size, dtype="int16")

                    while len(data) > 0:
                        stream.write(data.tobytes())
                        data = sound_file.read(chunk_size, dtype="int16")

                    stream.stop_stream()
                    stream.close()
        else:
            print(f"Error: {response.status_code} - {response.text}")

        audio.terminate()


if __name__ == "__main__":
    tts()
