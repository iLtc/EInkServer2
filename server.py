import os
from io import BytesIO
from dotenv import load_dotenv
from flask import Flask, request, send_file

from eink_13 import draw_screen as draw_screen_13

load_dotenv()

app = Flask(__name__)

@app.route("/")
def index():
    return "OK"

@app.route("/13.png")
def screen_13():
    if request.args.get("token") != os.getenv("TOKEN_13"):
        return "Unauthorized", 401

    image = draw_screen_13()

    # Convert PIL image to bytes
    img_io = BytesIO()
    image.save(img_io, 'PNG')
    img_io.seek(0)

    return send_file(img_io, mimetype='image/png')

if __name__ == "__main__":
    app.run(debug=True)