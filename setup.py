from setuptools import setup, find_packages

setup(
    name="utils",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "openai>=1.3.6",
        "python-dotenv>=1.0.0",
        "sounddevice>=0.4.6",
        "pydub>=0.25.1",
        "pygame>=2.5.2",
        "soundfile>=0.12.1",
        "pyaudio>=0.2.14",
        "requests>=2.31.0",
        "numpy>=1.26.2",
        "click>=8.1.7",
        "clipboard>=0.0.4",
        "youtube-transcript-api>=0.6.1",
        "langchain>=0.0.344",
        "tiktoken>=0.5.1",
        "pillow>=10.1.0",
        "toml>=0.10.2",
    ],
    entry_points={
        "console_scripts": [
            "tts=utils.tts:tts",
            "youtube=utils.youtube:youtube",
            "image=utils.image:image",
            "summary=utils.langchain.summary:main",
            "dalle=utils.dalle:dalle",
        ],
    },
)
