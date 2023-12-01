import os
import io
import pyaudio
import requests
import soundfile as sf
import dotenv
import click

dotenv.load_dotenv()


@click.command()
@click.option("--model", default="tts-1", help="The model to use for the TTS")
@click.option("--voice", default="alloy", help="The voice to use for the TTS")
@click.argument("input_text")
def tts(input_text, model="tts-1", voice="alloy"):
    url = "https://api.openai.com/v1/audio/speech"
    headers = {
        "Authorization": f'Bearer {os.getenv("OPENAI_API_KEY")}',
    }

    data = {
        "model": model,
        "input": input_text,
        "voice": voice,
        "response_format": "opus",
    }

    audio = pyaudio.PyAudio()

    with requests.post(url, headers=headers, json=data, stream=True) as response:
        if response.status_code == 200:
            buffer = io.BytesIO()
            for chunk in response.iter_content(chunk_size=4096):
                buffer.write(chunk)

            buffer.seek(0)

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
