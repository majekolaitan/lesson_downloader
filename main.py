import os
import argparse
from datetime import date, datetime
from config import ROOT_DIR
from utils import get_sabbath_school_info, cleanup_old_lessons
from youtube import get_lesson_title, search_channel_videos
from downloader import download_video, download_daily_lesson_audio_files

# Set working directory
os.chdir(ROOT_DIR)

if __name__ == "__main__":
    current_year, current_quarter, current_lesson = get_sabbath_school_info()
    print(f"Current Year: {current_year}, Quarter: {current_quarter}, Lesson: {current_lesson}")

    lesson_title = get_lesson_title(current_lesson, current_quarter, current_year)
    if lesson_title:
        print(f"Current lesson title: {lesson_title}")
    else:
        print("Failed to retrieve the lesson title. Exiting...")
        exit(1)

    cleanup_old_lessons(current_lesson)

    parser = argparse.ArgumentParser(description='Download a Sabbath School lesson video from 3ABN.')
    parser.add_argument('-f', '--format', type=str, default="bestvideo[vcodec^=avc1][width=640]+bestaudio", help='The download format (default: "avc1@360")')
    args = parser.parse_args()
    format_code = args.format

    video_urls = search_channel_videos(lesson_title, current_lesson, current_quarter, current_year)
    for url in video_urls:
        if url.startswith("https://"):
            print(url)
            download_video(url, format_code, current_lesson)
        else:
            print(f"Skipping invalid URL: {url}")

    download_daily_lesson_audio_files()
