from PIL import Image, ImageDraw, ImageFont

def draw_screen():
    # Colors
    white = (255, 255, 255)
    black = (0, 0, 0)

    # Image size
    img_width, img_height = 1600, 1200
    image = Image.new("RGB", (img_width, img_height), white)
    draw = ImageDraw.Draw(image)

    # Draw Test Text
    font = ImageFont.truetype("./fonts/Roboto-Regular.ttf", 100)
    draw.text((100, 100), "Hello, World!", font=font, fill=black)

    return image

if __name__ == "__main__":
    image = draw_screen()
    image.show()