# Scale-Img

`scale-img` is a Python-based tool for resizing and scaling images efficiently. This project provides a simple and customizable way to process images for various use cases.

## Features

- Resize images to specific dimensions.
- Maintain aspect ratio during scaling.
- Support for multiple image formats (e.g., JPEG, PNG).
- Batch processing for multiple images.

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/your-username/scale-img.git
    ```
2. Navigate to the project directory:
    ```bash
    cd scale-img
    ```
3. Install dependencies:
    ```bash
    poetry install
    ```

## Usage

1. Place the images you want to scale in the `input` folder.
2. Run the script:
    ```bash
    python scale_img.py -tp=10MP input output
    ```
3. Processed images will be saved in the `output` folder.

### Command-Line Options

- `-tp` / `--total-pixels`: Target resolution of the image.
- `--width`: Target width of the image.
- `--height`: Target height of the image.

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a new branch:
    ```bash
    git checkout -b feature-name
    ```
3. Commit your changes:
    ```bash
    git commit -m "Add feature-name"
    ```
4. Push to your branch:
    ```bash
    git push origin feature-name
    ```
5. Open a pull request.
