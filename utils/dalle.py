from openai import OpenAI
import requests
import os
from typing import Literal
import dotenv
import click

dotenv.load_dotenv()

# initialize OpenAI client
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)


@click.command()
@click.option("--prompt", "-p", help="The prompt to generate the image from.")
@click.option("--n", default=1, help="The number of images to generate.")
@click.option("--size", default="1024x1024", help="The size of the image.")
@click.option(
    "--quality",
    default="standard",
    help="The quality of the image. Can be standard or hd.",
)
@click.option("--output-dir", "-o", help="The output directory for the images.")
@click.option(
    "--name", default="generated_image", help="The name of the generated image."
)
@click.option("--prompt-path", help="The path to a file containing the prompt.")
def dalle(
    prompt: str = None,
    n: int = 1,
    size: Literal["1024x1024", "1024x1792", "1792x1024"] = "1024x1024",
    quality: Literal["standard", "hd"] = "standard",
    output_dir: str = None,
    name: str = "generated_image",
    prompt_path: str = None,
):
    """
    Generate images using OpenAI's DALL·E model.

    Args:
        prompt (str): The prompt to generate the image from.
        n (int): The number of images to generate. Defaults to 1.
        size (str): The size of the image. Defaults to "256x256".
        response_format (str): The format of the response. Defaults to "url".

    Returns:
        list: A list of image URLs or filepaths.
    """
    if prompt_path:
        with open(prompt_path, "r") as file:
            prompt = file.read()
    assert prompt, "--prompt or --prompt-path is required"

    if not output_dir:
        output_dir = os.curdir

    # call the OpenAI API
    generation_response = client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        n=n,
        size=size,
        response_format="url",
        quality=quality,
    )
    print(generation_response)

    # save the images
    image_urls = []
    for i in range(n):
        generated_image_name = f"{name}_{i}.png"
        generated_image_filepath = os.path.join(output_dir, generated_image_name)
        generated_image_url = generation_response.data[i].url
        generated_image = requests.get(generated_image_url).content

        with open(generated_image_filepath, "wb") as image_file:
            image_file.write(generated_image)

        image_urls.append(generated_image_filepath)
        print(generated_image_filepath)


if __name__ == "__main__":
    dalle()
