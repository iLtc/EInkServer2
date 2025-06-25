import requests
import os
from dotenv import load_dotenv
from PIL import Image, ImageDraw, ImageFont
from pprint import pprint

load_dotenv()


def get_tasks():
    headers = {
        "x-api-user": os.getenv("HABITICA_USER_ID"),
        "x-api-key": os.getenv("HABITICA_API_KEY")
    }
    response = requests.get("https://habitica.com/api/v3/tasks/user", headers=headers).json()['data']
    daily_tasks = [task["text"] for task in response if task["type"] == "daily" and task["completed"] == False and task["isDue"] == True]
    habit_tasks = [task["text"] for task in response if task["type"] == "habit" and task["counterUp"] == 0]
    return daily_tasks + habit_tasks


def draw_task_card(task, dark_background=False, center_text=False):
    image_width, image_height = 525, 70
    image = Image.new("RGB", (image_width, image_height), "white")
    draw = ImageDraw.Draw(image)

    draw.rounded_rectangle([(0, 0), (image_width, image_height)], outline="purple", fill="purple" if dark_background else "white", width=3, radius=20)

    font = ImageFont.truetype("./fonts/Roboto-Regular.ttf", 25)
    text_bbox = draw.textbbox((0, 0), task, font=font)
    text_height = text_bbox[3] - text_bbox[1]
    text_width = text_bbox[2] - text_bbox[0]

    if center_text:
        draw.text(((image_width - text_width) / 2, (image_height - text_height) / 2 - text_bbox[1]), task, fill="white" if dark_background else "black", font=font)
    else:
        draw.text((10, (image_height - text_height) / 2 - text_bbox[1]), task, fill="white" if dark_background else "black", font=font)

    return image


def draw_tasks():
    tasks = get_tasks()
    image_width, image_height = 525, 1080
    image = Image.new("RGB", (image_width, image_height), "white")

    title_image = draw_task_card("HABITICA", dark_background=True, center_text=True)
    image.paste(title_image, (0, 0))

    for i, task in enumerate(tasks):
        task_image = draw_task_card(task)
        image.paste(task_image, (0, (i + 1) * 75))

    return image


if __name__ == "__main__":
    image = draw_tasks()
    image.show()