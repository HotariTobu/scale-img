import argparse
from PIL import Image
from pathlib import Path
from math import sqrt
import re


SUPPORTED_EXTENSIONS = (".jpg", ".jpeg", ".png", ".bmp")


def is_valid_image_file(file_path: Path) -> bool:
    return file_path.is_file() and file_path.suffix.lower() in SUPPORTED_EXTENSIONS


def resize_image(
    input_image_path: Path,
    output_image_path: Path,
    total_pixels: int,
    desired_width: int,
    desired_height: int,
):
    try:
        original_image = Image.open(input_image_path)
        original_width, original_height = original_image.size
        aspect_ratio = original_width / original_height

        resized_width: int
        resized_height: int

        if desired_width:
            resized_width = desired_width
            resized_height = int(desired_width / aspect_ratio)
        elif desired_height:
            resized_width = int(desired_height * aspect_ratio)
            resized_height = desired_height
        else:
            resized_width = int(sqrt(total_pixels * aspect_ratio))
            resized_height = int(resized_width / aspect_ratio)

        size = (resized_width, resized_height)
        exif = original_image.getexif()

        resized_image = original_image.resize(size)
        resized_image.save(output_image_path, exif=exif)
    except FileNotFoundError:
        print(f"Error: {input_image_path} not found.")
    except Exception as e:
        print(f"Error processing {input_image_path}: {e}")


def parse_resolution(resolution: str) -> int:
    match = re.match(r"(\d*\.?\d+)MP", resolution, re.IGNORECASE)
    if match:
        try:
            megapixels = float(match.group(1))
            total_pixels = int(megapixels * 1000000)
            return total_pixels
        except ValueError:
            raise argparse.ArgumentTypeError("Invalid resolution value.")
    else:
        raise argparse.ArgumentTypeError(
            "Invalid resolution format. Please use a number followed by 'MP' (e.g., 16MP or 16.5MP)."
        )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Resize images to a specified resolution, width, or height.")
    parser.add_argument(
        "input_path", help="Input file or directory containing images.", type=Path
    )
    parser.add_argument(
        "output_dir", help="Output directory to save resized images.", type=Path
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "-tp",
        "--total-pixels",
        help="Desired resolution in megapixels (e.g., 16MP).",
        type=parse_resolution,
    )
    group.add_argument("--width", help="Desired width in pixels.", type=int)
    group.add_argument("--height", help="Desired height in pixels.", type=int)

    args = parser.parse_args()

    input_path: Path = args.input_path
    output_dir: Path = args.output_dir
    total_pixels: int = args.total_pixels
    width: int = args.width
    height: int = args.height

    if not output_dir.exists():
        print(f"Output directory {output_dir} does not exist. Create it? (y/n)")
        create_dir = input()
        if create_dir.lower() == "y":
            output_dir.mkdir(parents=True, exist_ok=True)
        else:
            print("Exiting.")
            exit()

    image_files: list[Path] = []
    if input_path.is_dir():
        image_files = [
            file for file in input_path.iterdir() if is_valid_image_file(file)
        ]
    elif is_valid_image_file(input_path):
        image_files.append(input_path)
    else:
        print(
            f"Invalid input path: {input_path}. Please provide a valid image file or directory."
        )
        exit()

    if not image_files:
        print(f"No valid image files found in {input_path}.")
        exit()

    for file in image_files:
        output_image_path = output_dir / file.name
        resize_image(file, output_image_path, total_pixels, width, height)
