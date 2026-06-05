# donut-ai

**donut-ai** is a Python tool that lets you turn text prompts into real-time 3D ASCII art — inspired by the classic donut.c code, but with actual 3D models fetched from the web.

## How It Works

1. **Prompt → 3D Model** — You type a description (e.g. `"a cat"`), and the script searches [Thingiverse](https://www.thingiverse.com/) via its API to find a matching 3D model.
2. **Download & Convert** — The model is downloaded (`.stl` or `.obj`), and if it's an STL it's automatically converted to OBJ format using [trimesh](https://trimesh.org/).
3. **Render to ASCII** — The OBJ file is parsed, its vertices centered and scaled, then rendered frame-by-frame using rotation, back-face culling, and a z-buffer. The result is displayed as an animated ASCII art scene in the terminal.

## Setup

1. Clone the repo and install dependencies:
   ```
   pip install requests trimesh python-dotenv
   ```
2. Get a **Thingiverse API token** (free) from [thingiverse.com/settings/apps](https://www.thingiverse.com/settings/apps).
3. Create a `.env` file in the project root with:
   ```
   THINGIVERSE_TOKEN=your_token_here
   ```

## Usage

Run the script:
```
python main.py
```

Enter a prompt when asked (e.g. `cat`, `robot`, `tree`) and watch the model spin in your terminal as ASCII art.

## Files Overview

| File | Purpose |
|---|---|
| `main.py` | Entry point — handles the render loop, screen buffer, and animation |
| `ai_generator.py` | Searches Thingiverse, downloads & converts 3D models |
| `parse_obj_file.py` | Parses `.obj` files into vertex and face lists |
| `math_utils.py` | Math helpers: 3D rotation, projection, normals, triangle rasterization |
| `generate_torus_obj.py` | Standalone script to generate a torus OBJ file (donut shape) |

## Customization

- **ASCII characters** — Edit `ASCII_CHARS` in `main.py` to change the shading ramp.
- **Scale / speed** — Adjust `SCALE`, `angle_x/y/z` increments, and `time.sleep()` in `main.py`.
- **Screen size** — Change `SCREEN_WIDTH` and `SCREEN_HEIGHT` for larger or smaller renders.