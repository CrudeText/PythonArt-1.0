# PythonArt v1.0 (by CrudeText)

This project is a command-line art generator designed to produce static, abstract digital images using various algorithmic techniques.

All artworks are generated through mathematical or random processes, and the user interacts through a simple terminal-based interface.

---

## How to Use

### 1. Requirements

Install Python 3 and make sure you have the required libraries:

```bash
pip install matplotlib numpy pillow
```

### 2. Run the Main Script

```bash
python run_art.py
```

This will launch an interactive prompt where you'll:

- Choose a generation function (e.g., `maxlines`, `gradientImg`, etc.)
- Choose how many times to run it
- Enter parameters with help text and value hints
- See your art displayed
- (Optionally) Save the output image

---

## Available Art Functions

### 1. `maxlines(points)`
Creates a mandala-like figure using point-to-point connections around a polygon.

- **points** (int): Number of summits (vertices). Recommended 50–300.

---

### 2. `gradientImg(imgsizex, imgsizey)`
Creates a smooth gradient image from black to yellow.

- **imgsizex** (int): Width of the image
- **imgsizey** (int): Height of the image

---

### 3. `randGradient(...)`
Generates vertical columns of evolving colors, either randomly or from a base RGB.

**Key parameters:**

- `sizex`, `sizey`: Image size
- `columnsize`: Width of each color column
- `increment`: Color variation per pixel
- `R`, `G`, `B`: Starting color (0–255)
- `randstart`: Whether to start with a random color
- `save`: Whether to save the image
- `customname`: Filename if saving

---

## Output Directory

All saved images are automatically placed in an `output/` folder located next to your scripts.

All configuration logs (inputs, parameters, function names) are saved to:

```text
run_logs.json
```

This file grows with each run and can be used to replicate settings or for debugging.

---

## Example Usage

```bash
python run_art.py
```

```text
Available art functions:
1. maxlines: Creates a complex mandala-like figure from point-to-point connections on a polygon.
2. gradientImg: Generates a smooth linear gradient from black to yellow.
3. randGradient: Generates color columns with evolving RGB values down the image.

Enter the name of the function to run: randGradient
How many times do you want to run this function? 1

Enter value for 'sizex' (Width of image (px), range: 500 - 4000) [default: 1920]:
Enter value for 'sizey' (Height of image (px), range: 500 - 4000) [default: 1080]:
...
Enter value for 'save' (Save image to file?, range: True/False) [default: False]: true
Enter value for 'customname' (Custom filename (w/o .png), range: e.g. Jesus, mandala_test) [default: Jesus]: galaxy1
```

This will generate your art and save it as `output/galaxy1.png`.

---

## Adding New Art Functions

1. Define a new function in `Art.py`
2. Add it to `ART_SCRIPTS` in `run_art.py` with:
   - Description
   - Parameter names and types
   - Optional: default values, min/max, choices
3. That’s it! Your new function will appear in the prompt.

---

## Project Structure

```text
.
├── Art.py               # Art generation functions
├── run_art.py           # Main interactive runner
├── output/              # Auto-created for saved images
├── run_logs.json        # Auto-created config history
└── README.md            # This file
```

---

## Author

Created by William Arranz (aka **CrudeText**)
Contact: [your email or link here]
