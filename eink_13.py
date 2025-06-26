from PIL import Image, ImageDraw, ImageFont
from eink_calendar import draw_calendar
from weather import draw_weather
from habitica import draw_tasks
from events import draw_events

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
    image.paste(calendar_image, (0, 0))

    # Draw Events
    events_image = draw_events()
    image.paste(events_image, (0, 550))

    # Draw Weather
    weather_image = draw_weather()
    image.paste(weather_image, (1600 - 1050, 0))

    # Draw Habitica
    habitica_image = draw_tasks()
    image.paste(habitica_image, (1600 - 1050, 125))

    return image

if __name__ == "__main__":
    image = draw_screen()
    image.show()