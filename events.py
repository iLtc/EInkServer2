import requests
import os
from dotenv import load_dotenv
from PIL import Image, ImageDraw, ImageFont
from icalendar import Calendar
from datetime import datetime, timedelta, date
from pytz import timezone
import recurring_ical_events

from pprint import pprint

load_dotenv()

timezone_pacific = timezone("US/Pacific")


def get_calendars():
    i = 0
    calendars = []

    while True:
        if not os.getenv("ICAL_URL_{}".format(i)):
            break

        calendars.append({
            "url": os.getenv("ICAL_URL_{}".format(i)),
            "name": os.getenv("ICAL_NAME_{}".format(i)),
            "color": os.getenv("ICAL_COLOR_{}".format(i)),
        })

        i += 1

    return calendars


def get_events(calendars):
    now = datetime.now(timezone_pacific)
    startOfToday = now.replace(hour=0, minute=0, second=0, microsecond=0)
    endOfToday = now.replace(hour=23, minute=59, second=59, microsecond=999999)
    startOfTomorrow = startOfToday + timedelta(days=1)
    endOfTomorrow = endOfToday + timedelta(days=1)

    todayEvents = []
    tomorrowEvents = []

    for calendar in calendars:
        url = calendar["url"]
        response = requests.get(url)

        cal = Calendar.from_ical(response.text)
        rie = recurring_ical_events.of(cal)

        for event in rie.between(now, endOfToday):
            if type(event.start) == date:
                continue

            todayEvents.append({
                "summary": event.get("SUMMARY"),
                "start": event.start,
                "end": event.end,
                "calendar": calendar["name"],
                "color": calendar["color"],
            })

        for event in rie.between(startOfTomorrow, endOfTomorrow):
            if type(event.start) == date:
                continue

            tomorrowEvents.append({
                "summary": event.get("SUMMARY"),
                "start": event.start,
                "end": event.end,
                "calendar": calendar["name"],
                "color": calendar["color"],
            })

    todayEvents.sort(key=lambda x: (x["start"], x["end"]))
    tomorrowEvents.sort(key=lambda x: (x["start"], x["end"]))

    return todayEvents, tomorrowEvents


def draw_event_card(event):
    width, height = 545, 40
    image = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(image)

    # draw left color box
    draw.rounded_rectangle([(10, 0), (20, height)], outline=event["color"], fill=event["color"], width=3, radius=20)

    # draw right text
    font = ImageFont.truetype("./fonts/Roboto-Light.ttf", 15)
    right_text = "[{} - {}]".format(event["start"].astimezone(timezone_pacific).strftime("%I:%M %p"), event["end"].astimezone(timezone_pacific).strftime("%I:%M %p"))
    right_text_bbox = draw.textbbox((0, 0), right_text, font=font)
    right_text_height = right_text_bbox[3] - right_text_bbox[1]
    right_text_width = right_text_bbox[2] - right_text_bbox[0]

    draw.text((width - right_text_width - 10, (height - right_text_height) / 2 - right_text_bbox[1]), right_text, font=font, fill="black")

    # draw left text
    font = ImageFont.truetype("./fonts/Roboto-Regular.ttf", 25)
    left_text_original = event["summary"]
    left_text = left_text_original

    while True:
        left_text_bbox = draw.textbbox((0, 0), left_text, font=font)
        left_text_width = left_text_bbox[2] - left_text_bbox[0]

        if left_text_width < width - right_text_width - 30:
            break

        left_text_original = left_text_original[:-1]
        left_text = left_text_original + "..."

    left_text_bbox = draw.textbbox((0, 0), left_text, font=font)
    left_text_height = left_text_bbox[3] - left_text_bbox[1]

    draw.text((30, (height - left_text_height) / 2 - left_text_bbox[1]), left_text, font=font, fill="black")

    return image

def draw_events():
    calendars = get_calendars()
    todayEvents, tomorrowEvents = get_events(calendars)

    img_width, img_height = 545, 655
    image = Image.new("RGB", (img_width, img_height), "white")
    draw = ImageDraw.Draw(image)

    y = 0

    for event in todayEvents:
        event_image = draw_event_card(event)
        image.paste(event_image, (0, y))
        y += 45

    # draw separator
    draw.line([(0, y), (img_width, y)], fill="black", width=3)

    # draw tomorrow events
    y += 5

    for event in tomorrowEvents:
        event_image = draw_event_card(event)
        image.paste(event_image, (0, y))
        y += 45

    return image


if __name__ == "__main__":
    image = draw_events()
    image.show()
