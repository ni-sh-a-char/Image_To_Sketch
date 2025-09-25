# Image_To_Sketch  
**A simple Python program to convert an image into a sketch.**  

---  

## Table of Contents
1. [Overview](#overview)  
2. [Installation](#installation)  
3. [Quick Start (CLI)](#quick-start-cli)  
4. [Python API](#python-api)  
5. [Examples](#examples)  
6. [Project Structure](#project-structure)  
7. [Contributing](#contributing)  
8. [License](#license)  

---  

## Overview <a name="overview"></a>

`Image_To_Sketch` provides a lightweight, dependency‑minimal way to turn any raster image (JPG, PNG, BMP, …) into a pencil‑style sketch.  
The core algorithm is based on OpenCV’s **grayscale → Gaussian blur → dodge blend** technique, which works well for both portraits and landscapes.

Features  

| Feature | Description |
|---------|-------------|
| ✅ Pure Python + OpenCV (no heavy ML models) |
| 🖥️ Command‑line interface (CLI) for one‑off conversions |
| 📦 Re‑usable Python API for integration in other projects |
| 🎨 Adjustable parameters (blur kernel size, sketch intensity) |
| 🧩 Works on Windows, macOS, Linux (Python 3.8+) |

---  

## Installation <a name="installation"></a>

### 1. Prerequisites  

| Requirement | Minimum version |
|-------------|-----------------|
| Python | 3.8 |
| pip | 21.0+ |
| Git (optional) | – |

> **Note** – The only non‑standard library dependency is **OpenCV‑Python**. All other modules are part of the Python standard library.

### 2. Clone the repository  

```bash
git clone https://github.com/yourusername/Image_To_Sketch.git
cd Image_To_Sketch
```

### 3. Install the package (editable mode recommended)

```bash
# Create a virtual environment (highly recommended)
python -m venv .venv
source .venv/bin/activate   # On Windows: .venv\Scripts\activate

# Install the package and its dependencies
pip install -e .
```

The `-e` flag installs the package in *editable* mode, so any changes you make to the source code are immediately reflected without reinstalling.

### 4. Verify the installation  

```bash
python -c "import image_to_sketch; print(image_to_sketch.__version__)"
```

You should see the current version string (e.g., `0.2.0`).

---  

## Quick Start (CLI) <a name="quick-start-cli"></a>

The repository ships a convenient command‑line tool called **`sketchify`**.

### Basic usage  

```bash
sketchify input.jpg output.png
```

- `input.jpg` – Path to the source image.  
- `output.png` – Desired path for the sketch image (any format supported by OpenCV).

### Advanced options  

```bash
sketchify input.jpg output.png \
    --blur-kernel 7 \
    --scale 1.5 \
    --invert \
    --show
```

| Option | Description |
|--------|-------------|
| `--blur-kernel N` | Size of the Gaussian blur kernel (must be odd). Default: `5`. |
| `--scale FACTOR` | Multiply the final sketch intensity by `FACTOR`. Default: `1.0`. |
| `--invert` | Produce a *negative* sketch (white lines on black background). |
| `--show` | Open a preview window (uses OpenCV’s `imshow`). |
| `-h, --help` | Show the help message. |

### Help output  

```bash
sketchify -h
```

```
usage: sketchify [-h] [--blur-kernel K] [--scale S] [--invert] [--show] input output

Convert an image to a pencil sketch.

positional arguments:
  input               Path to the input image.
  output              Path where the sketch will be saved.

optional arguments:
  -h, --help          show this help message and exit
  --blur-kernel K     Gaussian blur kernel size (odd integer, default=5)
  --scale S           Intensity scaling factor (default=1.0)
  --invert            Invert colors (white sketch on black)
  --show              Display the result in a window before saving
```

---  

## Python API <a name="python-api"></a>

The core functionality lives in `image_to_sketch.core`. Import the public functions as shown below.

### Module layout  

```
image_to_sketch/
│
├─ __init__.py          # package version & public symbols
├─ core.py              # main conversion logic
├─ utils.py             # helper functions (e.g., loading, saving)
└─ cli.py               # entry‑point for the `sketchify` console script
```

### Public functions  

| Function | Signature | Description |
|----------|-----------|-------------|
| `convert_to_sketch` | `convert_to_sketch(image: np.ndarray, blur_kernel: int = 5, scale: float = 1.0, invert: bool = False) -> np.ndarray` | Takes a **BGR** OpenCV image array and returns the sketch as a **grayscale** array. |
| `load_image` | `load_image(path: str, as_gray: bool = False) -> np.ndarray` | Wrapper around `cv2.imread`. Raises `FileNotFoundError` if the file does not exist. |
| `save_image` | `save_image(image: np.ndarray, path: str) -> None` | Saves a NumPy image to disk using `cv2.imwrite`. Supports all formats OpenCV can write. |
| `show_image` | `show_image(image: np.ndarray, title: str = "Image") -> None` | Convenience wrapper for `cv2.imshow` + `cv2.waitKey(0)`. |

#### Example: Using the API directly  

```python
import cv2
from image_to_sketch import convert_to_sketch, load_image, save_image

# 1️⃣ Load the source image (BGR)
src = load_image("photos/cat.jpg")

# 2️⃣ Convert to sketch
sketch = convert_to_sketch(src, blur_kernel=9, scale=1.2, invert=False)

# 3️⃣ Save the result
save_image(sketch, "output/cat_sketch.png")
```

### Advanced usage  

If you need to process a batch of images or integrate the sketching step into a larger pipeline, you can combine the API with Python’s `concurrent.futures` for parallel execution:

```python
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from image_to_sketch import convert_to_sketch, load_image, save_image

def process_one(in_path: Path, out_path: Path):
    img = load_image(str(in_path))
    sketch = convert_to_sketch(img, blur_kernel=7, scale=1.0)
    save_image(sketch, str(out_path))

input_dir = Path("photos/")
output_dir = Path("sketches/")
output_dir.mkdir(exist_ok=True)

with ThreadPoolExecutor(max_workers=4) as executor:
    futures = [
        executor.submit(process_one, p, output_dir / f"{p.stem}_sketch.png")
        for p in input_dir.glob("*.jpg")
    ]
    for f in as_completed(futures):
        f.result()   # will raise if any worker failed
```

---  

## Examples <a name="examples"></a>

### 1️⃣ Simple CLI conversion  

```bash
sketchify samples/landscape.jpg sketches/landscape_sketch.png
```

Result:  

| Original | Sketch |
|----------|--------|
| ![landscape](https://raw.githubusercontent.com/yourusername/Image_To_Sketch/main/docs/assets/landscape.jpg) | ![landscape_sketch](https://raw.githubusercontent.com/yourusername/Image_To_Sketch/main/docs/assets/landscape_sketch.png) |

---

### 2️⃣ Adjusting blur and intensity  

```bash
sketchify samples/portrait.jpg sketches/portrait_blur9.png \
    --blur-kernel 9 --scale 1.5 --show
```

Increasing the blur kernel smooths out fine texture, while `--scale 1.5` makes the lines darker.

---

### 3️⃣ Inverted sketch (white on black)  

```bash
sketchify samples/flower.png sketches/flower_inverted.png --invert
```

---

### 4️⃣ Using the API in a Jupyter notebook  

```python
import matplotlib.pyplot as plt
from image_to_sketch import load_image, convert_to_sketch

# Load image
img = load_image("samples/dog.jpg")

# Create sketch
sketch = convert_to_sketch(img, blur_kernel=5, scale=1.0)

# Plot side‑by‑side
fig, ax = plt.subplots(1, 2, figsize=(10, 4))
ax[0].imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
ax[0].