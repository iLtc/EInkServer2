import calendar
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont

def draw_calendar():
    # Get current date info
    now = datetime.now()
    year = now.year
    month = now.month
    day = now.day
    weekday_name = now.strftime('%A')
    month_year_str = now.strftime('%B %Y')

    # Set up fonts and sizes
    font_dayname = ImageFont.truetype("./fonts/Roboto-Regular.ttf", 60)
    font_day = ImageFont.truetype("./fonts/Roboto-Bold.ttf", 110)
    font_monthyear = ImageFont.truetype("./fonts/Roboto-Regular.ttf", 45)
    font_grid_header = ImageFont.truetype("./fonts/Roboto-Regular.ttf", 35)
    font_grid = ImageFont.truetype("./fonts/Roboto-Regular.ttf", 35)

    # Colors
    bg_color = (0, 0, 0)
    white = (255, 255, 255)
    red = (255, 0, 0)

    # Image size
    img_width, img_height = 545, 545
    image = Image.new("RGB", (img_width, img_height), bg_color)
    draw = ImageDraw.Draw(image)

    # --- Draw Day Name ---
    dayname_bbox = draw.textbbox((0,0), weekday_name, font=font_dayname)
    dayname_width = dayname_bbox[2] - dayname_bbox[0]
    dayname_height = dayname_bbox[3] - dayname_bbox[1]
    x_dayname = (img_width - dayname_width) // 2
    y = 5
    draw.text((x_dayname, y), weekday_name, font=font_dayname, fill=white)

    # --- Draw Day (number) ---
    day_str = f"{day:02d}"
    day_bbox = draw.textbbox((0,0), day_str, font=font_day)
    day_width = day_bbox[2] - day_bbox[0]
    day_height = day_bbox[3] - day_bbox[1]
    x_day = (img_width - day_width) // 2
    y += dayname_height + 16  # Add extra space
    draw.text((x_day, y), day_str, font=font_day, fill=red)

    # --- Draw Month Year ---
    monthyear_bbox = draw.textbbox((0,0), month_year_str, font=font_monthyear)
    monthyear_width = monthyear_bbox[2] - monthyear_bbox[0]
    monthyear_height = monthyear_bbox[3] - monthyear_bbox[1]
    x_monthyear = (img_width - monthyear_width) // 2
    y += day_height + 40  # Add extra space
    draw.text((x_monthyear, y), month_year_str, font=font_monthyear, fill=white)

    # --- Draw Calendar Grid ---
    cell_w = img_width // 7
    cell_h = 45
    y_grid = y + monthyear_height + 30
    x_grid = 0

    # Weekday headers
    weekdays = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
    for i, wd in enumerate(weekdays):
        color = red
        wd_bbox = draw.textbbox((0,0), wd, font=font_grid_header)
        wd_width = wd_bbox[2] - wd_bbox[0]
        x_wd = (cell_w - wd_width) // 2
        draw.text((x_grid + i*cell_w + x_wd, y_grid), wd, font=font_grid_header, fill=color)
    # Days
    cal = calendar.Calendar(calendar.SUNDAY)
    month_days = list(cal.itermonthdays(year, month))
    # Arrange days in rows
    y_days = y_grid + cell_h + 2
    for week in range(6):
        for i in range(7):
            idx = week*7 + i
            d = month_days[idx] if idx < len(month_days) else 0
            if d == 0:
                continue
            is_today = (d == day)
            color = red if (i == 0 or i == 6) else white  # Sunday/Saturday red
            day_str = f"{d:2d}"
            day_bbox = draw.textbbox((0,0), day_str, font=font_grid)
            day_width = day_bbox[2] - day_bbox[0]
            day_height = day_bbox[3] - day_bbox[1]
            x_day = (cell_w - day_width) // 2
            y_day = y_days + week*cell_h + (cell_h - day_height) // 2
            if is_today:
                # Draw white circle
                draw.rectangle((x_grid + i*cell_w, y_day - 3, x_grid + i*cell_w + cell_w, y_day + cell_h - 3), fill=white if color == bg_color else color)
                draw.text((x_grid + i*cell_w + x_day, y_day), day_str, font=font_grid, fill=bg_color)
            else:
                draw.text((x_grid + i*cell_w + x_day, y_day), day_str, font=font_grid, fill=color)

    return image


if __name__ == "__main__":
    image = draw_calendar()
    image.show()