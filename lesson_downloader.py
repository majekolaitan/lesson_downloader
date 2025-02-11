import os
import re
import requests
import json  # Import the JSON module to handle JSON parsing
import argparse
from youtubesearchpython import ChannelSearch, ResultMode
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import yt_dlp

# Get the user's home directory dynamically
USER_HOME_DIR = os.path.expanduser('~')

# Set the root directory (e.g., a subdirectory within the user's home folder)
ROOT_DIR = os.path.join(USER_HOME_DIR, 'Videos/Lesson Study') 

# Set the working directory to the root directory
os.chdir(ROOT_DIR)

# Now, all file operations will be relative to ROOT_DIR


# Define the channel IDs and query formats
CHANNEL_IDS = {
    '3abn': {'id': 'UCw_AthKfwqB3XYpboTFZFmg', 'query_format': '{lesson_title} | Sabbath School Panel by 3ABN - Lesson {lesson_number} Q{quarter} {year}', 'first_result': True},
    'itiswritten': {'id': 'UCtWyoUrGPAkZgnp2486Ir4w', 'query_format': 'Sabbath School - {year} Q{quarter} Lesson {lesson_number}: {lesson_title}', 'first_result': True},
    'hopess': {'id': 'UCm34NbuHzE9t9hHutOxwIOA', 'query_format': 'Lesson {lesson_number}', 'first_result': False},
    'claudiocarneiro': {'id': 'UCvJRu-jirSkv6yuxakirENg', 'query_format': '{year} Q{quarter} Lesson {lesson_number} – {lesson_title} – Audio by Percy Harrold', 'first_result': True},
    'HopeLives365': {'id': 'UCOuDMda3jxj-g_iI1P2d2zw', 'query_format': 'Sabbath School with Mark Finley | Lesson {lesson_number} — Q{quarter} – {year}', 'first_result': True},
    'egwhiteaudio': {'id': 'UCPS3A-60tKmKTCKWZMT9upA', 'query_format': '{year} Q{quarter} Lesson {lesson_number} – EGW Notes – {lesson_title}', 'first_result': True},
    'claudiocarneiroegw': {'id': 'UCvJRu-jirSkv6yuxakirENg', 'query_format': '{year} Q{quarter} Lesson {lesson_number} – EGW Notes – {lesson_title} Carla Morris', 'first_result': True},
}

def get_quarter_and_week(date):
    try:
        month = date.month
    except ValueError as ve:
        print(f"Invalid date provided: {ve}")
        return None, None

    # Determine which quarter the month falls in
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

    # Find the start of the quarter (first day of the quarter)
    quarter_start = datetime(date.year, quarter_start_month, 1)

    # Adjust the quarter start to the previous Saturday (or same day if it's Saturday)
    # In Python, weekday(): Monday is 0 and Sunday is 6. So Saturday is 5.
    quarter_start_weekday = quarter_start.weekday()
    days_since_saturday = (quarter_start_weekday - 5) % 7
    week_start_date = quarter_start - timedelta(days=days_since_saturday)

    # Calculate the difference in days between the date and the adjusted week start date
    day_difference = (date - week_start_date).days

    # Calculate the week number of the quarter, weeks start on Saturday
    week_of_quarter = (day_difference // 7) + 1

    return quarter, week_of_quarter


# Function to search YouTube for the current lesson title
def get_lesson_title(lesson_number, quarter, year):
    """
    Search YouTube for the title of the current lesson and extract it from the first result.
    """
    # Define the query to search for
    query = f"Sabbath School Panel by 3ABN - Lesson {lesson_number} Q{quarter} {year}"
    
    # Perform the search on the 3ABN YouTube channel
    channel_id = "UCw_AthKfwqB3XYpboTFZFmg"  # 3ABN Channel ID
    search = ChannelSearch(query, channel_id)
    
    # Get the search results in JSON format
    result_string = search.result(mode=ResultMode.json)

    # Parse the JSON result
    if not result_string:
        print("No results returned from YouTube.")
        return None

    try:
        result = json.loads(result_string)
    except json.JSONDecodeError:
        print("Failed to parse search results.")
        return None

    # Check if results exist and extract the first video's title
    if result and 'result' in result and result['result']:
        first_video = result['result'][0]
        raw_title = first_video.get('title', 'No Title Found')
        
        # Use regex to extract the text within the first pair of quotation marks
        match = re.search(r'“([^”]+)”', raw_title)
        if match:
            lesson_title = match.group(1)
            return lesson_title
        else:
            print("Lesson title not found in the expected format.")
            return None
    else:
        print("No results found for the given lesson.")
        return None

# Function to convert relative time strings into datetime objects
def parse_relative_time(relative_time):
    if not isinstance(relative_time, str):
        return None

    # Handle "Just now" case
    if relative_time.strip().lower() == "just now":
        return datetime.now()

    # Match patterns like "5 minutes ago", "2 hours ago", "1 day ago", etc.
    match = re.match(r'(\d+)\s+(\w+)\s+ago', relative_time)
    if not match:
        return None  # Handle unexpected formats gracefully

    num = int(match.group(1))
    unit = match.group(2).lower()

    # Use timedelta for units smaller than a month
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
    # Use relativedelta for months and years
    elif 'month' in unit:
        return datetime.now() - relativedelta(months=num)
    elif 'year' in unit:
        return datetime.now() - relativedelta(years=num)
    else:
        return None  # In case of an unrecognized unit

def search_channel_videos(lesson_title, lesson_number, quarter, year):
    urls = []

    # Iterate through the defined channels and their search formats
    for channel_name, details in CHANNEL_IDS.items():
        try:
            # Generate the query string dynamically using the provided details
            query = details['query_format'].format(
                lesson_title=lesson_title, lesson_number=lesson_number, quarter=quarter, year=year
            )
            print(f"Searching in channel {channel_name} for query: {query}")

            # Perform the search within the specific channel using the generated query
            search = ChannelSearch(query, details['id'])
            result_string = search.result(mode=ResultMode.json)  # This returns a string

            # Parse the result string into a JSON object
            try:
                result = json.loads(result_string)
            except json.JSONDecodeError:
                print(f"Failed to parse results for {channel_name}.")
                continue

            # Extract the video results if they exist
            if result and 'result' in result and result['result']:
                videos = result['result']

                # If first_result is True, use the first video directly
                if details['first_result']:
                    first_video = videos[0]
                    video_url = f"https://www.youtube.com/watch?v={first_video['id']}"
                    urls.append(video_url)
                else:
                    # Parse the 'published' time into a datetime object
                    for video in videos:
                        published_time = video.get('published', 'unknown time')
                        video['published_datetime'] = parse_relative_time(published_time)

                    # Filter out videos with None as published_datetime
                    valid_videos = [v for v in videos if v['published_datetime'] is not None]

                    if valid_videos:
                        # Sort the valid videos by their parsed 'published_datetime', newest first
                        valid_videos = sorted(valid_videos, key=lambda v: v['published_datetime'], reverse=True)
                        
                        # Get the most recent video after sorting
                        most_recent_video = valid_videos[0]
                        video_url = f"https://www.youtube.com/watch?v={most_recent_video['id']}"
                        urls.append(video_url)
                    else:
                        urls.append(f"{channel_name}: No valid video results found")
            else:
                urls.append(f"{channel_name}: No results found")

        except Exception as e:
            print(f"Error occurred while searching in channel {channel_name}: {e}")

    return urls

# Function to download a YouTube video using yt-dlp
def download_video(url, format_code, lesson_number):
    """
    Download the specified YouTube video using yt-dlp.

    Parameters:
    - url (str): The URL of the YouTube video.
    - format_code (str): The format code to be passed to yt-dlp (e.g., "140" for audio).
    - lesson_number (int): The current lesson number for dynamic naming.
    """
    # Dynamically generate the archive filename based on the lesson number
    archive_file = f'downloaded_videos_lesson_{lesson_number}.txt'
    
    ydl_opts = {
        'format': format_code,
        'outtmpl': '%(title)s.%(ext)s',  # Define the output template
        'download_archive': archive_file,  # Use dynamic archive filename
        'quiet': True,  # Suppress yt-dlp output
        'no_warnings': True,  # Suppress warnings
    }

    # Use yt-dlp to download the video with the specified options
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            print(f"Downloading: {url} in format: {format_code}")
            ydl.download([url])
        except yt_dlp.utils.DownloadError as e:
            print(f"Download failed for {url}: {e}")

# Function to download daily lesson audio files
def download_daily_lesson_audio_files():
    """
    Download daily lesson audio files from a pre-defined URL format based on the last Saturday.
    """
    today = datetime.today()
    
    # Find the last Saturday
    last_saturday = today - timedelta(days=(today.weekday() + 2) % 7)

    # Loop from last Saturday to Friday of the current week (last Saturday + 6 days)
    for i in range(7):
        download_date = last_saturday + timedelta(days=i)
        formatted_date = download_date.strftime('%Y-%m-%d')
        url = f"https://d7dlhz1yjc01y.cloudfront.net/audio/en/lessons/{formatted_date}.mp3"
        
        # Check if the file is available by making a HEAD request
        try:
            head_response = requests.head(url, timeout=10)
            if head_response.status_code == 200:
                # Check if the file is already downloaded before calling download
                if not os.path.exists(formatted_date + '.mp3'):
                    download_file(url)
                else:
                    print(f"File {formatted_date}.mp3 already exists. Skipping download.")
            else:
                print(f"File not found for {formatted_date}. Skipping.")
        except requests.exceptions.RequestException as e:
            print(f"Error checking availability for {url}: {e}")


def download_file(url):
    """
    Helper function to download a file from a given URL.
    Skips downloading if the file already exists.
    """
    local_filename = url.split('/')[-1]

    # Check if the file already exists
    if os.path.exists(local_filename):
        print(f"File {local_filename} already exists. Skipping download.")
        return

    try:
        print(f"Downloading {url}")
        response = requests.get(url, stream=True, timeout=10)
        response.raise_for_status()  # Raises HTTPError for bad responses (4xx or 5xx)
        with open(local_filename, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
        print(f"Downloaded: {local_filename}")
    except requests.exceptions.Timeout:
        print(f"Request timed out: {url}")
    except requests.exceptions.ConnectionError:
        print(f"Connection error occurred for: {url}")
    except requests.exceptions.HTTPError as err:
        print(f"HTTP error occurred: {err}")
    except Exception as e:
        print(f"Error downloading {url}: {e}")


def cleanup_old_lessons(current_lesson_number):
    """
    Removes old lesson files from the directory that are from previous lessons.
    Also removes lesson files in the format YYYY-MM-DD that are older than the last Saturday.
    
    Parameters:
    - current_lesson_number (int): The current lesson number to keep.
    """
    # Regex patterns
    lesson_pattern = re.compile(r'Lesson (\d+)', re.IGNORECASE)  # Regex to find 'Lesson X' or 'Lesson 02'
    date_pattern = re.compile(r'(\d{4}-\d{2}-\d{2})')  # Regex to find filenames in 'YYYY-MM-DD' format

    # Calculate the last Saturday
    today = datetime.now().date()
    last_saturday = today - timedelta(days=(today.weekday() + 2) % 7)

    # List all files in the current directory
    for filename in os.listdir():
        # Check if the filename contains "Lesson X" (with or without zero padding)
        lesson_match = lesson_pattern.search(filename)
        date_match = date_pattern.search(filename)

        if lesson_match:
            # Handle 'Lesson X' files, strip leading zeros for comparison
            file_lesson_number = int(lesson_match.group(1))
            if file_lesson_number != current_lesson_number:
                print(f"Removing old lesson file: {filename}")
                os.remove(filename)
            else:
                print(f"Keeping current lesson file: {filename}")
        elif date_match:
            # Handle files in 'YYYY-MM-DD' format
            file_date_str = date_match.group(1)
            file_date = datetime.strptime(file_date_str, '%Y-%m-%d').date()
            if file_date < last_saturday:
                print(f"Removing old lesson file (date-based): {filename}")
                os.remove(filename)
            else:
                print(f"Keeping recent lesson file (date-based): {filename}")
        else:
            print(f"Skipping non-lesson file: {filename}")


# Main logic
if __name__ == "__main__":
    today = datetime.today()
    current_quarter, current_lesson_number = get_quarter_and_week(today)
    current_year = today.year
    print(f"Current Year: {current_year}, Quarter: {current_quarter}, Lesson: {current_lesson_number}")

    lesson_title = get_lesson_title(current_lesson_number, current_quarter, current_year)
    if lesson_title:
        print(f"Current lesson title: {lesson_title}")
    else:
        print("Failed to retrieve the lesson title. Exiting...")
        exit(1)

    # Perform the cleanup before downloading new files
    cleanup_old_lessons(current_lesson_number)

    # Argument parser setup
    parser = argparse.ArgumentParser(description='Download a Sabbath School lesson video from 3ABN.')
    parser.add_argument('-f', '--format', type=str, default='140', help='The download format (default: "140")')
    args = parser.parse_args()
    format_code = args.format

    # Perform the search and print the results
    video_urls = search_channel_videos(lesson_title, current_lesson_number, current_quarter, current_year)

    for url in video_urls:
        if url.startswith("https://"):
            print(url)
            download_video(url, format_code, current_lesson_number)  # Pass lesson number to the function
        else:
            print(f"Skipping invalid URL: {url}")

    # Download daily lesson audio files
    download_daily_lesson_audio_files()
    

    
