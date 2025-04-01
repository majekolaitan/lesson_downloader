import os
import argparse
from datetime import date, datetime
from config import ROOT_DIR
from utils import get_quarter_and_week, cleanup_old_lessons
from youtube import get_lesson_title, search_channel_videos
from downloader import download_video, download_daily_lesson_audio_files

# Set working directory
os.chdir(ROOT_DIR)

if __name__ == "__main__":
    today = datetime.today()
    # today = datetime(2025, 4, 1)
    current_quarter, current_lesson_number = get_quarter_and_week(today)
    current_year = today.year
    print(f"Current Year: {current_year}, Quarter: {current_quarter}, Lesson: {current_lesson_number}")

    lesson_title = get_lesson_title(current_lesson_number, current_quarter, current_year)
    if lesson_title:
        print(f"Current lesson title: {lesson_title}")
    else:
        print("Failed to retrieve the lesson title. Exiting...")
        exit(1)

    cleanup_old_lessons(current_lesson_number)

    parser = argparse.ArgumentParser(description='Download a Sabbath School lesson video from 3ABN.')
    parser.add_argument('-f', '--format', type=str, default='140', help='The download format (default: "140")')
    args = parser.parse_args()
    format_code = args.format

    video_urls = search_channel_videos(lesson_title, current_lesson_number, current_quarter, current_year)
    for url in video_urls:
        if url.startswith("https://"):
            print(url)
            download_video(url, format_code, current_lesson_number)
        else:
            print(f"Skipping invalid URL: {url}")

    download_daily_lesson_audio_files()
