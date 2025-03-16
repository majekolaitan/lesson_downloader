import os
import requests
import yt_dlp

def download_video(url, format_code, lesson_number):
    """
    Download the specified YouTube video using yt-dlp.
    """
    archive_file = f'downloaded_videos_lesson_{lesson_number}.txt'
    ydl_opts = {
        'format': format_code,
        'outtmpl': '%(title)s.%(ext)s',
        'download_archive': archive_file,
        'quiet': True,
        'no_warnings': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            print(f"Downloading: {url} in format: {format_code}")
            ydl.download([url])
        except yt_dlp.utils.DownloadError as e:
            print(f"Download failed for {url}: {e}")

def download_file(url):
    """
    Download a file from a given URL.
    """
    local_filename = url.split('/')[-1]
    if os.path.exists(local_filename):
        print(f"File {local_filename} already exists. Skipping download.")
        return

    try:
        print(f"Downloading {url}")
        response = requests.get(url, stream=True, timeout=10)
        response.raise_for_status()
        with open(local_filename, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
        print(f"Downloaded: {local_filename}")
    except Exception as e:
        print(f"Error downloading {url}: {e}")

def download_daily_lesson_audio_files():
    """
    Download daily lesson audio files based on the last Saturday.
    """
    from datetime import datetime, timedelta
    today = datetime.today()
    last_saturday = today - timedelta(days=(today.weekday() + 2) % 7)
    for i in range(7):
        download_date = last_saturday + timedelta(days=i)
        formatted_date = download_date.strftime('%Y-%m-%d')
        url = f"https://d7dlhz1yjc01y.cloudfront.net/audio/en/lessons/{formatted_date}.mp3"
        try:
            head_response = requests.head(url, timeout=10)
            if head_response.status_code == 200:
                if not os.path.exists(formatted_date + '.mp3'):
                    download_file(url)
                else:
                    print(f"File {formatted_date}.mp3 already exists. Skipping download.")
            else:
                print(f"File not found for {formatted_date}. Skipping.")
        except requests.exceptions.RequestException as e:
            print(f"Error checking availability for {url}: {e}")
