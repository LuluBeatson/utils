import click
from PIL import Image, ImageOps
import os


@click.group()
def image():
    """Image utility commands."""
    pass


@image.command()
@click.option("--output", default=None, help="The name of the output image")
@click.option(
    "--columns", default=3, help="Number of images in each row in the grid", type=int
)
@click.option(
    "--range",
    default=None,
    help="Range of images to include in the grid. Format: start,end",
)
@click.option("--border-size", default=1, help="Size of the border between images")
@click.option(
    "--border-color", default="grey", help="Color of the border. Default is grey"
)
@click.option(
    "--overwrite", is_flag=True, help="Overwrite the output file if it exists"
)
@click.argument("directory", type=click.Path(exists=True))
def grid(
    directory: str,
    output: str,
    columns: int,
    border_size: int,
    border_color,
    overwrite: bool,
    range: tuple[int, int] = None,
):
    """Create a grid of images from a directory."""
    if not os.path.isdir(directory):
        raise click.BadParameter(f"Directory {directory} does not exist")
    if output is None:
        output = directory
    if os.path.exists(output + ".png") and not overwrite:
        raise click.BadParameter(
            f"Output file {output}.png already exists. Use --overwrite to overwrite it"
        )

    # Retrieve all the png images
    images = [img for img in os.listdir(directory) if img.endswith(".png")]
    images.sort()
    if range is not None:
        start, end = range.split(",")
        start = int(start)
        end = int(end)
        images = images[start:end]

    # Open images and determine total size
    opened_images = []
    total_width = total_height = 0

    for img in images:
        current_image = Image.open(os.path.join(directory, img))
        opened_images.append(current_image)
        total_width = max(total_width, current_image.size[0])
        total_height = max(total_height, current_image.size[1])

    total_width += border_size
    total_height += border_size

    # Calculate the number of rows and columns
    rows = -(-len(images) // columns)
    grid_width = total_width * columns + border_size
    grid_height = total_height * rows + border_size

    # Create new image with calculated total size
    new_img = Image.new("RGBA", (grid_width, grid_height))

    # Iterate over images and paste them to the new image
    for index, img in enumerate(opened_images):
        row = index // columns
        col = index % columns
        if border_size > 0:
            border = (
                border_size,
                border_size,
                border_size,
                border_size,
            )  # border size for each side
            img_with_border = ImageOps.expand(img, border=border, fill=border_color)
            new_img.paste(img_with_border, (col * total_width, row * total_height))
        else:
            new_img.paste(img, (col * total_width, row * total_height))

    new_img.save(output + ".png")


if __name__ == "__main__":
    image()
