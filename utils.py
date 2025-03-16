import os
import re
from datetime import datetime, timedelta

def get_quarter_and_week(date):
    try:
        month = date.month
    except ValueError as ve:
        print(f"Invalid date provided: {ve}")
        return None, None

    if 1 <= month <= 3:
        quarter_start_month = 1
        quarter = 1
    elif 4 <= month <= 6:
        quarter_start_month = 4
        quarter = 2
    elif 7 <= month <= 9:
        quarter_start_month = 7
        quarter = 3
    else:
        quarter_start_month = 10
        quarter = 4

    quarter_start = datetime(date.year, quarter_start_month, 1)
    quarter_start_weekday = quarter_start.weekday()
    days_since_saturday = (quarter_start_weekday - 5) % 7
    week_start_date = quarter_start - timedelta(days=days_since_saturday)
    day_difference = (date - week_start_date).days
    week_of_quarter = (day_difference // 7) + 1
    return quarter, week_of_quarter

def parse_relative_time(relative_time):
    from datetime import datetime, timedelta
    from dateutil.relativedelta import relativedelta
    if not isinstance(relative_time, str):
        return None
    if relative_time.strip().lower() == "just now":
        return datetime.now()
    import re
    match = re.match(r'(\d+)\s+(\w+)\s+ago', relative_time)
    if not match:
        return None
    num = int(match.group(1))
    unit = match.group(2).lower()
    if 'second' in unit:
        return datetime.now() - timedelta(seconds=num)
    elif 'minute' in unit:
        return datetime.now() - timedelta(minutes=num)
    elif 'hour' in unit:
        return datetime.now() - timedelta(hours=num)
    elif 'day' in unit:
        return datetime.now() - timedelta(days=num)
    elif 'week' in unit:
        return datetime.now() - timedelta(weeks=num)
    elif 'month' in unit:
        return datetime.now() - relativedelta(months=num)
    elif 'year' in unit:
        return datetime.now() - relativedelta(years=num)
    return None

def cleanup_old_lessons(current_lesson_number):
    lesson_pattern = re.compile(r'Lesson (\d+)', re.IGNORECASE)
    date_pattern = re.compile(r'(\d{4}-\d{2}-\d{2})')
    today = datetime.now().date()
    last_saturday = today - timedelta(days=(today.weekday() + 2) % 7)
    for filename in os.listdir():
        lesson_match = lesson_pattern.search(filename)
        date_match = date_pattern.search(filename)
        if lesson_match:
            file_lesson_number = int(lesson_match.group(1))
            if file_lesson_number != current_lesson_number:
                print(f"Removing old lesson file: {filename}")
                os.remove(filename)
            else:
                print(f"Keeping current lesson file: {filename}")
        elif date_match:
            file_date_str = date_match.group(1)
            file_date = datetime.strptime(file_date_str, '%Y-%m-%d').date()
            if file_date < last_saturday:
                print(f"Removing old lesson file (date-based): {filename}")
                os.remove(filename)
            else:
                print(f"Keeping recent lesson file (date-based): {filename}")
        else:
            print(f"Skipping non-lesson file: {filename}")
