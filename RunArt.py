# -*- coding: utf-8 -*-
"""
Created on Thu Mar 22 19:24:16 2025

@author: willi
"""

import Art
import os
import json
from datetime import datetime

# Define available art functions and their parameter metadata
ART_SCRIPTS = {
    "maxlines": {
        "description": "Creates a complex mandala-like figure from point-to-point connections on a polygon.",
        "params": {
            "points": {
                "type": int,
                "desc": "Number of summits (vertices) for the polygon",
                "range": "int ≥ 3 (recommended: 50-300)",
                "default": 150,
                "min": 3,
                "max": 1000
            }
        }
    },
    "gradientImg": {
        "description": "Generates a smooth linear gradient from black to yellow.",
        "params": {
            "imgsizex": {
                "type": int,
                "desc": "Width of the image in pixels",
                "range": "int > 0",
                "default": 800,
                "min": 1
            },
            "imgsizey": {
                "type": int,
                "desc": "Height of the image in pixels",
                "range": "int > 0",
                "default": 600,
                "min": 1
            }
        }
    },
    "randGradient": {
        "description": "Generates color columns with evolving RGB values down the image.",
        "params": {
            "sizex": {"type": int, "desc": "Width of image (px)", "range": "500 - 4000", "default": 1920, "min": 100, "max": 8000},
            "sizey": {"type": int, "desc": "Height of image (px)", "range": "500 - 4000", "default": 1080, "min": 100, "max": 8000},
            "columnsize": {"type": int, "desc": "Width of each column", "range": "5 - 50", "default": 10, "min": 1},
            "increment": {"type": int, "desc": "Amount color changes per step", "range": "1 - 10", "default": 1, "min": 1},
            "darkvariation": {"type": int, "desc": "Chance of darkening", "range": "5 - 20", "default": 10, "min": 0},
            "lightvariation": {"type": int, "desc": "Chance of brightening", "range": "5 - 20", "default": 10, "min": 0},
            "vartotal": {"type": int, "desc": "Random scale total", "range": "Typically 100", "default": 100, "min": 1},
            "R": {"type": int, "desc": "Starting red value", "range": "0 - 255", "default": 127, "min": 0, "max": 255},
            "G": {"type": int, "desc": "Starting green value", "range": "0 - 255", "default": 127, "min": 0, "max": 255},
            "B": {"type": int, "desc": "Starting blue value", "range": "0 - 255", "default": 127, "min": 0, "max": 255},
            "randstart": {"type": bool, "desc": "Randomize initial color?", "range": "True/False", "default": False},
            "randvariation": {"type": int, "desc": "Extra variation", "range": "0 - 20", "default": 0, "min": 0},
            "save": {"type": bool, "desc": "Save image to file?", "range": "True/False", "default": False},
            "customname": {"type": str, "desc": "Custom filename (w/o .png)", "range": "e.g. Jesus, mandala_test", "default": "Jesus"}
        }
    },
    "SunRay": {
        "description": "Draws symmetrical rays between two concentric rings of points.",
        "params": {
            "linenumber": {"type": int, "desc": "Number of rays to draw", "range": "10 - 500", "default": 30, "min": 1},
            "ringnumber": {"type": int, "desc": "Number of concentric ring layers", "range": "1 - 10", "default": 1, "min": 1},
            "imgsize": {"type": int, "desc": "Image size (px)", "range": "500 - 3000", "default": 1000, "min": 100},
            "shift": {"type": int, "desc": "Rotation offset between inner and outer rings", "range": "0 - linenumber", "default": 5},
            "R": {"type": int, "desc": "Red value for line color", "range": "0 - 255", "default": 255, "min": 0, "max": 255},
            "G": {"type": int, "desc": "Green value for line color", "range": "0 - 255", "default": 0, "min": 0, "max": 255},
            "B": {"type": int, "desc": "Blue value for line color", "range": "0 - 255", "default": 0, "min": 0, "max": 255},
            "linethickness": {"type": int, "desc": "Thickness of lines", "range": "1 - 20", "default": 5, "min": 1},
            "inRatio": {"type": float, "desc": "Ratio for inner ring radius", "range": "0.0 - 1.0", "default": 0.3, "min": 0.0, "max": 1.0},
            "outRatio": {"type": float, "desc": "Ratio for outer ring radius", "range": "0.0 - 1.0", "default": 1.0, "min": 0.0, "max": 1.0}
        }
    },
    "randSun": {
        "description": "Like SunRay but adds random angle and color variation.",
        "params": {
            "linenumber": {"type": int, "desc": "Number of rays", "range": "100 - 5000", "default": 2000, "min": 1},
            "imgsize": {"type": int, "desc": "Image size (px)", "range": "500 - 3000", "default": 1080, "min": 100},
            "shift": {"type": int, "desc": "Rotation offset between rings", "range": "0 - linenumber", "default": 5},
            "R": {"type": int, "desc": "Base red (not strictly used)", "range": "0 - 255", "default": 255, "min": 0, "max": 255},
            "G": {"type": int, "desc": "Base green (not strictly used)", "range": "0 - 255", "default": 0, "min": 0, "max": 255},
            "B": {"type": int, "desc": "Base blue (not strictly used)", "range": "0 - 255", "default": 0, "min": 0, "max": 255},
            "linethickness": {"type": int, "desc": "Line thickness", "range": "1 - 10", "default": 1, "min": 1},
            "inRatio": {"type": float, "desc": "Inner ring radius ratio", "range": "0.0 - 1.0", "default": 0.3, "min": 0.0, "max": 1.0},
            "outRatio": {"type": float, "desc": "Outer ring radius ratio", "range": "0.0 - 1.0", "default": 1.0, "min": 0.0, "max": 1.0},
            "maxvarout": {"type": int, "desc": "Max angular variation for outer ring", "range": "0 - 1000", "default": 300, "min": 0},
            "maxvarin": {"type": int, "desc": "Max angular variation for inner ring", "range": "0 - 1000", "default": 300, "min": 0}
        }
    }
}

    # Add other functions here if needed



def get_input(prompt, typ, default=None, meta=None):
    while True:
        val = input(prompt).strip()

        # Use default
        if val == "":
            if default is not None:
                val = default
            else:
                print("This value is required. Please enter something.")
                continue

        # Handle bools
        if typ == bool:
            if isinstance(val, bool):
                return val
            elif val.lower() in ("true", "1", "yes", "y"):
                return True
            elif val.lower() in ("false", "0", "no", "n"):
                return False
            else:
                print("Invalid boolean. Use yes/no or true/false.")
                continue

        try:
            if typ == int:
                val = int(float(val))
            elif typ == float:
                val = float(val)
            elif typ == str:
                val = str(val)

            # Apply validation if any
            if meta:
                if "choices" in meta and val not in meta["choices"]:
                    print(f"Value must be one of: {meta['choices']}")
                    continue
                if "min" in meta and val < meta["min"]:
                    print(f"Value must be ≥ {meta['min']}")
                    continue
                if "max" in meta and val > meta["max"]:
                    print(f"Value must be ≤ {meta['max']}")
                    continue

            return val

        except ValueError:
            print(f"Invalid input. Expected a {typ.__name__}. Try again.")


def save_run_to_log(script_name, params):
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "function": script_name,
        "parameters": params
    }
    log_path = "run_logs.json"

    try:
        if os.path.exists(log_path):
            with open(log_path, "r") as f:
                data = json.load(f)
        else:
            data = []

        data.append(log_entry)

        with open(log_path, "w") as f:
            json.dump(data, f, indent=4)

        print(f"Configuration saved to {log_path}")

    except Exception as e:
        print("Warning: Could not save run log.")
        print(e)


def run():
    print("Available art functions:")
    for idx, key in enumerate(ART_SCRIPTS):
        print(f"{idx + 1}. {key}: {ART_SCRIPTS[key]['description']}")

    choice = input("Enter the name of the function to run: ").strip()

    if choice not in ART_SCRIPTS:
        print("Function not found.")
        return

    try:
        runs = int(input("How many times do you want to run this function? "))
    except:
        print("Invalid number.")
        return

    for run_idx in range(runs):
        print(f"\nConfiguration for run #{run_idx + 1}")
        params = {}
        for param, meta in ART_SCRIPTS[choice]['params'].items():
            desc = meta["desc"]
            rng = meta["range"]
            typ = meta["type"]
            default = meta.get("default", None)
            default_str = f" [default: {default}]" if default is not None else ""
            prompt = f"Enter value for '{param}' ({desc}, range: {rng}){default_str}: "
            val = get_input(prompt, typ, default, meta)
            params[param] = val

        print(f"Running {choice} with parameters: {params}")
        func = getattr(Art, choice)
        result = func(**params)
        save_run_to_log(choice, params)

        if result and hasattr(result, "show"):
            result.show()


if __name__ == "__main__":
    run()
