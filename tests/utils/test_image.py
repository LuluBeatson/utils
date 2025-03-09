import os
from PIL import Image
from utils.image import image


def test_image_help(runner):
    """Test the image command's help output.

    Given: A CLI runner for the image command
    When: The help flag is provided (--help)
    Then: The output should:
        - Return success (exit code 0)
        - Show available commands section
        - List the 'grid' subcommand
    """
    result = runner.invoke(image, ["--help"])
    assert result.exit_code == 0
    assert "Commands:" in result.output
    assert "grid" in result.output


def test_grid_command(runner, test_dir, sample_images):
    """Test the grid command with default settings.

    Given:
        - 3 sample images of 100x100 pixels each
        - Default border size of 1 pixel
        - Grid layout of 2 columns

    When: Creating a grid with default settings

    Then: Should produce an image with:
        Width calculation:
        - Base width = 100px (image width)
        - Add spacing = 100px + 1px = 101px per cell
        - 2 columns = 101px * 2 = 202px
        - Plus final border = 203px total width

        Height calculation:
        - Base height = 100px (image height)
        - Add spacing = 100px + 1px = 101px per cell
        - 2 rows needed = 101px * 2 = 202px
        - Plus final border = 203px total height
    """
    output_path = str(test_dir / "output")
    result = runner.invoke(
        image, ["grid", "--columns", "2", "--output", output_path, str(test_dir)]
    )

    assert result.exit_code == 0
    assert os.path.exists(output_path + ".png")

    # Verify the output image
    with Image.open(output_path + ".png") as img:
        assert img.mode == "RGBA"
        width, height = img.size
        assert width == 203  # (100 + 1)px * 2 + 1px
        assert height == 203  # (100 + 1)px * 2 + 1px
