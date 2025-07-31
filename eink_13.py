from PIL import Image, ImageDraw, ImageFont
from eink_calendar import draw_calendar
from weather import draw_weather
from habitica import draw_habits
from events import draw_events
from tasks import draw_tasks

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
    image.paste(events_image, (0, 595))

    # Draw Weather
    weather_image = draw_weather()
    image.paste(weather_image, (595, 0))

    # Draw Habitica
    habitica_image = draw_habits()
    image.paste(habitica_image, (595, 125))

    # Draw Tasks
    tasks_image = draw_tasks()
    image.paste(tasks_image, (1000, 125))

    return image

if __name__ == "__main__":
    image = draw_screen()
    image.show()