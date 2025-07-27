import json
import re
from datetime import datetime, timedelta
# CHANGE: Import VideosSearch instead of ChannelSearch
from youtubesearchpython import VideosSearch, ResultMode
from dateutil.relativedelta import relativedelta
from config import CHANNEL_IDS
from utils import parse_relative_time

def get_lesson_title(lesson_number, quarter, year):
    """
    Search YouTube for the title of the current lesson using a general search
    and filtering for the specific channel.
    """
    channel_id = "UCw_AthKfwqB3XYpboTFZFmg"  # 3ABN Channel ID
    channel_name = "3ABN" # Add channel name to the query for better results
    
    # CHANGE: Add channel name to the query to improve relevance
    query = f"{channel_name} {lesson_number} Q{quarter} {year}"
    
    # CHANGE: Use VideosSearch, which is more robust than ChannelSearch
    # We use a limit to be efficient and avoid fetching too many results.
    search = VideosSearch(query, limit=10)
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
        # CHANGE: We now loop through the results and find the first video
        # that matches our target channel ID.
        for video in result['result']:
            if video.get('channel', {}).get('id') == channel_id:
                # Found a video from the correct channel, now process it.
                raw_title = video.get('title', 'No Title Found')
                match = re.search(r'“([^”]+)”', raw_title)
                if match:
                    return match.group(1)
        
        # If the loop finishes, no matching video was found
        print("Lesson title not found in the expected format from the target channel.")

    else:
        print("No results found for the given lesson query.")
    return None

def search_channel_videos(lesson_title, lesson_number, quarter, year):
    """
    Searches each defined channel for videos matching the lesson.
    
    - This function now uses VideosSearch and filters results by channel ID.
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
            
            # CHANGE: Use VideosSearch with a reasonable limit
            search = VideosSearch(query, limit=20)
            result_string = search.result(mode=ResultMode.json)
            
            try:
                result = json.loads(result_string)
            except json.JSONDecodeError:
                print(f"Failed to parse results for channel '{channel_name}'.")
                continue

            if result and 'result' in result and result['result']:
                # CHANGE: Filter the general results to only include videos from the target channel
                channel_videos = [
                    v for v in result['result']
                    if v.get('channel', {}).get('id') == details['id']
                ]

                if not channel_videos:
                    print(f"Channel '{channel_name}': No results found matching the channel ID.")
                    continue

                # The rest of the logic now operates on the filtered `channel_videos` list
                if details.get('first_result', False):
                    candidate = channel_videos[0]
                else:
                    # Process candidate videos: add published_datetime and sort.
                    for video in channel_videos:
                        # NOTE: The key from VideosSearch is 'publishedTime', not 'published'
                        published_time = video.get('publishedTime', 'unknown time')
                        video['published_datetime'] = parse_relative_time(published_time)
                    
                    valid_videos = [v for v in channel_videos if v.get('published_datetime') is not None]
                    
                    if valid_videos:
                        valid_videos = sorted(valid_videos, key=lambda v: v['published_datetime'], reverse=True)
                        candidate = valid_videos[0]
                    else:
                        candidate = None

                if candidate:
                    video_title = candidate.get('title', 'No Title Found')
                    video_url = f"https://www.youtube.com/watch?v={candidate['id']}"
                    print(f"Channel '{channel_name}' found video: {video_title}")

                    if details.get('confirm_download', False):
                        confirm = input("Do you want to add this video? [y/n]: ").strip().lower()
                        if confirm == 'y':
                            urls.append(video_url)
                        else:
                            print("Skipping this video.")
                    else:
                        urls.append(video_url)
                else:
                    print(f"Channel '{channel_name}': No valid video candidate found after filtering.")
            else:
                print(f"Channel '{channel_name}': No results found for the query.")
        except Exception as e:
            print(f"Error occurred while searching in channel '{channel_name}': {e}")
    return urls