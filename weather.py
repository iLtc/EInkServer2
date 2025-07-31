import requests
import os
from dotenv import load_dotenv
from datetime import datetime, timezone
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO

load_dotenv()


def get_weather():
    results = {}

    # get current weather
    url = "https://weather.googleapis.com/v1/currentConditions:lookup?location.latitude={}&location.longitude={}&unitsSystem=IMPERIAL&key={}".format(os.getenv("WEATHER_LATITUDE"), os.getenv("WEATHER_LONGITUDE"), os.getenv("GOOGLE_API_KEY"))
    response = requests.get(url).json()

    results["current"] = response

    # get forecast
    now = datetime.now(timezone.utc)

    url = "https://weather.googleapis.com/v1/forecast/days:lookup?days=2&location.latitude={}&location.longitude={}&unitsSystem=IMPERIAL&key={}".format(os.getenv("WEATHER_LATITUDE"), os.getenv("WEATHER_LONGITUDE"), os.getenv("GOOGLE_API_KEY"))
    response = requests.get(url).json()
    today, tomorrow = response["forecastDays"]
    today_end = datetime.fromisoformat(today["daytimeForecast"]["interval"]["endTime"].replace('Z', '+00:00'))

    if now < today_end:
        results["today"] = today["daytimeForecast"]
        results["tonight"] = today["nighttimeForecast"]
        results["maxTemperature"] = today["maxTemperature"]
        results["minTemperature"] = today["minTemperature"]
    else:
        results["tonight"] = today["nighttimeForecast"]
        results["tomorrow"] = tomorrow["daytimeForecast"]
        results["maxTemperature"] = tomorrow["maxTemperature"]
        results["minTemperature"] = today["minTemperature"]

    return results


def draw_weather_card(icon_url, label, condition, temperature):
    width, height = 335, 120
    image = Image.new("RGB", (width, height), "black")

    # draw icon
    icon_width, icon_height = 96, 96
    icon_response = requests.get(icon_url)
    icon = Image.open(BytesIO(icon_response.content))

    if icon.mode != 'RGBA':
        icon = icon.convert('RGBA')

    # Create a transparent background for the icon area
    icon_bg = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    icon_bg.paste(icon, (0, (height - icon_height) // 2), icon)

    # Composite the icon onto the main image
    image = Image.alpha_composite(image.convert('RGBA'), icon_bg).convert('RGB')

    draw = ImageDraw.Draw(image)

    # draw label
    font_label = ImageFont.truetype("./fonts/Roboto-Regular.ttf", 12)
    label_bbox = draw.textbbox((0,0), label, font=font_label)
    label_width = label_bbox[2] - label_bbox[0]

    draw.text((((width - icon_width) - label_width) / 2 + icon_width, 10), label, fill="white", font=font_label)

    # draw condition
    font_size = 30

    while True:
        font_condition = ImageFont.truetype("./fonts/Roboto-Regular.ttf", font_size)
        condition_bbox = draw.textbbox((0,0), condition, font=font_condition)
        condition_width = condition_bbox[2] - condition_bbox[0]

        if condition_width < width - icon_width:
            break

        font_size -= 1

    font_condition = ImageFont.truetype("./fonts/Roboto-Regular.ttf", font_size)
    condition_bbox = draw.textbbox((0,0), condition, font=font_condition)
    condition_width = condition_bbox[2] - condition_bbox[0]
    condition_height = condition_bbox[3] - condition_bbox[1]

    draw.text((((width - icon_width) - condition_width) / 2 + icon_width, (height / 4) - (condition_height / 2) + 15), condition, fill="white", font=font_condition)

    # draw temperature
    font_temperature = ImageFont.truetype("./fonts/Roboto-Regular.ttf", 30)
    temperature_bbox = draw.textbbox((0,0), temperature, font=font_temperature)
    temperature_width = temperature_bbox[2] - temperature_bbox[0]
    temperature_height = temperature_bbox[3] - temperature_bbox[1]
    draw.text((((width - icon_width) - temperature_width) / 2 + icon_width, (height * 3 / 4) - (temperature_height / 2)), temperature, fill="white", font=font_temperature)

    # draw separator
    draw.line((icon_width + 10, height // 2 + 10, width - 10, height // 2 + 10), fill="white", width=2)

    return image


def draw_weather():
    width, height = 1005, 120
    weather_data = get_weather()

    image = Image.new("RGB", (width, height), "white")

    first_card = draw_weather_card(
        weather_data["current"]["weatherCondition"]['iconBaseUri'] + ".png",
        "Now",
        weather_data["current"]["weatherCondition"]["description"]["text"],
        "{} °F / {} °F".format(weather_data["current"]["temperature"]["degrees"], weather_data["current"]["feelsLikeTemperature"]["degrees"])
    )
    image.paste(first_card, (0, 0))

    if "today" in weather_data:
        second_card = draw_weather_card(
            weather_data["today"]["weatherCondition"]['iconBaseUri'] + ".png",
            "Today",
            weather_data["today"]["weatherCondition"]["description"]["text"],
            "Max: {} °F".format(weather_data["maxTemperature"]["degrees"])
        )

        third_card = draw_weather_card(
            weather_data["tonight"]["weatherCondition"]['iconBaseUri'] + ".png",
            "Tonight",
            weather_data["tonight"]["weatherCondition"]["description"]["text"],
            "Min: {} °F".format(weather_data["minTemperature"]["degrees"])
        )

    else:
        second_card = draw_weather_card(
            weather_data["tonight"]["weatherCondition"]['iconBaseUri'] + ".png",
            "Tonight",
            weather_data["tonight"]["weatherCondition"]["description"]["text"],
            "Min: {} °F".format(weather_data["minTemperature"]["degrees"])
        )

        third_card = draw_weather_card(
            weather_data["tomorrow"]["weatherCondition"]['iconBaseUri'] + ".png",
            "Tomorrow",
            weather_data["tomorrow"]["weatherCondition"]["description"]["text"],
            "Max: {} °F".format(weather_data["maxTemperature"]["degrees"])
        )

    image.paste(second_card, (width // 3, 0))
    image.paste(third_card, (width // 3 * 2, 0))

    return image


if __name__ == "__main__":
    # draw_weather()
    image = draw_weather()
    image.show()