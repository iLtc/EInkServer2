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

resizedimage = image.resize(inky.resolution)

inky.set_image(resizedimage)

inky.show()