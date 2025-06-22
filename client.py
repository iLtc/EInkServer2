#!/usr/bin/env python3

import argparse
import sys
import requests
from datetime import datetime
from io import BytesIO

from PIL import Image, ImageDraw, ImageFont

from inky.auto import auto

parser = argparse.ArgumentParser()

parser.add_argument("--url", "-u", type=str, help="Image URL")

inky = auto(ask_user=False, verbose=True)

args, _ = parser.parse_known_args()

if not args.url:
    print(f"""Usage:
    {sys.argv[0]} --url https://example.com/image.png""")
    sys.exit(1)


response = requests.get(args.url)
image = Image.open(BytesIO(response.content))

# add timestamp

draw = ImageDraw.Draw(image)
font = ImageFont.truetype("Roboto-Regular.ttf", 24)  # Adjust size as needed
draw.text((10, 10), "Last updated: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"), fill="black", font=font)

image = image.rotate(180)
resizedimage = image.resize(inky.resolution)

inky.set_image(resizedimage)

inky.show()