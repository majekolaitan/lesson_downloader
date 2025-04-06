import json
import re
from datetime import datetime, timedelta
from youtubesearchpython import ChannelSearch, ResultMode
from dateutil.relativedelta import relativedelta
from config import CHANNEL_IDS
from utils import parse_relative_time

def get_lesson_title(lesson_number, quarter, year):
    """
    Search YouTube for the title of the current lesson.
    """
    query = f"{lesson_number} Q{quarter} {year}"
    channel_id = "UCw_AthKfwqB3XYpboTFZFmg"  # 3ABN Channel ID
    search = ChannelSearch(query, channel_id)
    result_string = search.result(mode=ResultMode.json)

    if not result_string:
        print("No results returned from YouTube.")
        return None

    try:
        result = json.loads(result_string)
    except json.JSONDecodeError:
        print("Failed to parse search results.")
        return None

    if result and 'result' in result and result['result']:
        first_video = result['result'][0]
        raw_title = first_video.get('title', 'No Title Found')
        match = re.search(r'“([^”]+)”', raw_title)
        if match:
            return match.group(1)
        else:
            print("Lesson title not found in the expected format.")
    else:
        print("No results found for the given lesson.")
    return None

def search_channel_videos(lesson_title, lesson_number, quarter, year):
    """
    Searches each defined channel for videos matching the lesson.
    
    - If first_result is True, the first video candidate is selected.
    - If first_result is False, the most recent valid video (after sorting by published time) is chosen.
    - If confirm_download is True, the candidate video title is printed and you are prompted to confirm before adding the video.
    """
    urls = []
    for channel_name, details in CHANNEL_IDS.items():
        try:
            query = details['query_format'].format(
                lesson_title=lesson_title, lesson_number=lesson_number, quarter=quarter, year=year
            )
            print(f"\nSearching in channel '{channel_name}' for query: {query}")
            search = ChannelSearch(query, details['id'])
            result_string = search.result(mode=ResultMode.json)
            
            try:
                result = json.loads(result_string)
            except json.JSONDecodeError:
                print(f"Failed to parse results for channel '{channel_name}'.")
                continue

            if result and 'result' in result and result['result']:
                videos = result['result']
                # Determine the candidate video based on first_result flag.
                if details.get('first_result', False):
                    candidate = videos[0]
                else:
                    # Process candidate videos: add published_datetime and sort.
                    for video in videos:
                        published_time = video.get('published', 'unknown time')
                        video['published_datetime'] = parse_relative_time(published_time)
                    valid_videos = [v for v in videos if v.get('published_datetime') is not None]
                    if valid_videos:
                        valid_videos = sorted(valid_videos, key=lambda v: v['published_datetime'], reverse=True)
                        candidate = valid_videos[0]
                    else:
                        candidate = None

                if candidate:
                    video_title = candidate.get('title', 'No Title Found')
                    video_url = f"https://www.youtube.com/watch?v={candidate['id']}"
                    print(f"Channel '{channel_name}' found video: {video_title}")

                    # Ask for confirmation if confirm_download is True.
                    if details.get('confirm_download', False):
                        confirm = input("Do you want to add this video? [y/n]: ").strip().lower()
                        if confirm == 'y':
                            urls.append(video_url)
                        else:
                            print("Skipping this video.")
                    else:
                        urls.append(video_url)
                else:
                    print(f"Channel '{channel_name}': No valid video candidate found")
            else:
                print(f"Channel '{channel_name}': No results found")
        except Exception as e:
            print(f"Error occurred while searching in channel '{channel_name}': {e}")
    return urls
