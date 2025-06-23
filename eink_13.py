from PIL import Image, ImageDraw, ImageFont
from eink_calendar import draw_calendar

def draw_screen():
    # Colors
    white = (255, 255, 255)
    black = (0, 0, 0)

    # Image size
    img_width, img_height = 1600, 1200
    image = Image.new("RGB", (img_width, img_height), white)
    draw = ImageDraw.Draw(image)

    # Draw Calendar
    calendar_image = draw_calendar()
    image.paste(calendar_image, (0, 30))

    return image

if __name__ == "__main__":
    image = draw_screen()
    image.show()