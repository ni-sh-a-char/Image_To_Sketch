# Image_To_Sketch  
*A simple Python program to convert an image into a sketch.*

---  

## Table of Contents
- [Overview](#overview)  
- [Installation](#installation)  
- [Quick Start (CLI)](#quick-start-cli)  
- [Python API](#python-api)  
- [Examples](#examples)  
- [Project Structure](#project-structure)  
- [Testing](#testing)  
- [Contributing](#contributing)  
- [License](#license)  

---  

## Overview  

`Image_To_Sketch` provides a lightweight, dependency‑friendly way to turn any photograph (or raster image) into a pencil‑style sketch.  
The core algorithm is based on classic image‑processing techniques (grayscale conversion, Gaussian blur, and dodge blending) implemented with **OpenCV** and **NumPy**.  

You can use it in three ways:

1. **Command‑line interface (CLI)** – one‑liner conversion.  
2. **Python library** – call the functions from your own code.  
3. **Web/GUI wrappers** – the library is deliberately kept UI‑agnostic so you can embed it anywhere.  

---  

## Installation  

### 1. Prerequisites  

| Tool | Minimum version |
|------|-----------------|
| Python | 3.8 |
| pip   | 21.0+ |
| Git   | optional (for cloning) |

### 2. Install from PyPI (recommended)

```bash
pip install image-to-sketch
```

> The PyPI package bundles the latest stable release and all required dependencies (`opencv-python`, `numpy`, `pillow`).

### 3. Install from source  

```bash
# Clone the repository
git clone https://github.com/yourusername/Image_To_Sketch.git
cd Image_To_Sketch

# Create a virtual environment (optional but recommended)
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

# Install the package in editable mode
pip install -e .
```

### 4. Optional dependencies  

| Feature | Extra | Packages |
|---------|-------|----------|
| GPU‑accelerated OpenCV (if you have CUDA) | `opencv-cuda` | `opencv-contrib-python-headless` |
| Image format support beyond PNG/JPG (e.g., TIFF, WebP) | `extra-formats` | `pillow[webp,tiff]` |

Install extras with:

```bash
pip install image-to-sketch[opencv-cuda,extra-formats]
```

---  

## Quick Start (CLI)

The package ships a small command‑line tool called **`sketchify`**.

```bash
sketchify -i path/to/input.jpg -o path/to/output.png
```

### Arguments

| Flag | Description | Default |
|------|-------------|---------|
| `-i`, `--input` | Path to the source image (required) | – |
| `-o`, `--output` | Destination path for the sketch (required) | – |
| `-b`, `--blur` | Gaussian blur kernel size (must be odd). Larger values give smoother sketches. | `21` |
| `-c`, `--contrast` | Contrast multiplier for the dodge blend (float). | `1.0` |
| `-s`, `--scale` | Resize factor (float). Useful for speeding up large images. | `1.0` |
| `-v`, `--verbose` | Print progress information. | `False` |

#### Example: High‑contrast, fast conversion

```bash
sketchify -i portrait.jpg -o portrait_sketch.png -b 31 -c 1.2 -s 0.5 -v
```

#### Example: Batch processing

```bash
for img in images/*.jpg; do
    sketchify -i "$img" -o "sketches/$(basename "$img" .jpg)_sketch.png"
done
```

---  

## Python API  

You can also import the library directly in your Python code.

```python
from image_to_sketch import Sketcher, utils
```

### Core Classes & Functions  

| Object | Signature | Description |
|--------|-----------|-------------|
| **`Sketcher`** | `Sketcher(blur_kernel: int = 21, contrast: float = 1.0, scale: float = 1.0)` | Main class that holds conversion parameters. |
| `Sketcher.convert(image: np.ndarray) -> np.ndarray` | Convert a **NumPy** image (BGR) to a sketch. |
| `Sketcher.convert_path(input_path: str, output_path: str) -> None` | Load an image from disk, convert, and write the result. |
| **`utils.load_image`** | `load_image(path: str, scale: float = 1.0) -> np.ndarray` | Reads an image with OpenCV, optionally resizes it. |
| **`utils.save_image`** | `save_image(image: np.ndarray, path: str) -> None` | Writes a BGR/gray image to disk (auto‑detects format). |
| **`utils.dodge_blend`** | `dodge_blend(gray: np.ndarray, blurred: np.ndarray, contrast: float = 1.0) -> np.ndarray` | Internal helper that implements the classic “dodge” operation. |
| **`utils.get_version`** | `() -> str` | Returns the current library version. |

#### Example: Using the API

```python
import cv2
from image_to_sketch import Sketcher, utils

# Load an image (OpenCV loads as BGR)
img = utils.load_image('samples/flower.jpg', scale=0.75)

# Create a Sketcher with custom parameters
sketcher = Sketcher(blur_kernel=31, contrast=1.2)

# Convert to sketch (still a NumPy array)
sketch = sketcher.convert(img)

# Show the result with OpenCV (optional)
cv2.imshow('Sketch', sketch)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Save to disk
utils.save_image(sketch, 'outputs/flower_sketch.png')
```

#### Advanced: Integrating with Pillow

If you prefer Pillow objects:

```python
from PIL import Image
import numpy as np
from image_to_sketch import Sketcher, utils

pil_img = Image.open('samples/cat.jpg')
np_img = np.array(pil_img)[:, :, ::-1]   # Convert RGB -> BGR for OpenCV

sketch = Sketcher().convert(np_img)

# Convert back to Pillow for further processing
sketch_pil = Image.fromarray(sketch[:, :, 0])  # grayscale
sketch_pil.save('outputs/cat_sketch.png')
```

---  

## Examples  

### 1. Simple script (single image)

```python
# file: simple_demo.py
from image_to_sketch import Sketcher, utils

if __name__ == '__main__':
    sketcher = Sketcher()
    sketch = sketcher.convert_path('samples/dog.jpg', 'outputs/dog_sketch.png')
    print('Sketch saved!')
```

Run:

```bash
python simple_demo.py
```

### 2. Batch conversion with progress bar

```python
# file: batch_demo.py
import pathlib
from tqdm import tqdm
from image_to_sketch import Sketcher

INPUT_DIR  = pathlib.Path('samples')
OUTPUT_DIR = pathlib.Path('outputs')
OUTPUT_DIR.mkdir(exist_ok=True)

sketcher = Sketcher(blur_kernel=25, contrast=1.1)

for img_path in tqdm(sorted(INPUT_DIR.glob('*.jpg'))):
    out_path = OUTPUT_DIR / f'{img_path.stem}_sketch.png'
    sketcher.convert_path(str(img_path), str(out_path))
```

```bash
python batch_demo.py
```

### 3. Jupyter Notebook snippet

```python
# In a Jupyter cell
from image_to_sketch import Sketcher, utils
import matplotlib.pyplot as plt

sketcher = Sketcher(blur_kernel=15, contrast=1.3)
sketch = sketcher.convert_path('samples/landscape.jpg', 'outputs/landscape_sketch.png')

# Display side‑by‑side
orig = utils.load_image('samples/landscape.jpg')
fig, ax = plt.subplots(1, 2, figsize=(12, 5))
ax[0].imshow(cv2.cvtColor(orig, cv2.COLOR_BGR2RGB))
ax[0].set_title('Original')
ax[0].axis('off')
ax[1].imshow(sketch, cmap='gray')
ax[1].set_title('Sketch')
ax[1].axis('