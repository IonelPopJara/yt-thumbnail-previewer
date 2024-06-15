import os
import json
import datetime

import googleapiclient.errors
import googleapiclient.discovery

from dotenv import load_dotenv

API_SERVICE_NAME = "youtube"
API_VERSION = "v3"
API_KEY = os.getenv("API_KEY")
FILE_NAME = 'data.json'

MAX_LIFETIME_HOURS = 24

# Load the .env file so it can read the API key
load_dotenv()


def fetch_top_videos():
    """
    Fetches the YouTube API for the top 50 videos and stores their data in a JSON file
    """

    load_dotenv()

    api_service_name = "youtube"
    api_version = "v3"
    api_key = os.getenv("API_KEY")

    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey=api_key)

    print("Fetching top videos...\n")

    request = youtube.videos().list(
            part="snippet,statistics",
            chart="mostPopular",
            regionCode="US",
            maxResults=25
    )

    response = request.execute()

    for video in response['items']:
        channel_id = video['snippet']['channelId']
        channel_icon_url = get_channel_icon(youtube, channel_id)
        video['channelIcon'] = channel_icon_url

    write_json_data(response['items'])

    print('New data was cached')


def get_channel_icon(youtube, channel_id):
    """
    Fetches the channel icon URL for a given channel ID
    """
    request = youtube.channels().list(
        part="snippet",
        id=channel_id
    )

    response = request.execute()

    if response['items']:
        return response['items'][0]['snippet']['thumbnails']['default']['url']
    else:
        return None


def write_json_data(input_data):
    """
    Formats and saves the data of the fetched videos into a JSON file
    """

    data = {}
    # data['timestamp'] = datetime.datetime.now().isoformat()
    data['timestamp'] = datetime.datetime.now().replace(microsecond=0).isoformat()
    data['items'] = []

    for video in input_data:

        video_data = {}
        video_data['title'] = video['snippet']['title']
        video_data['channel'] = video['snippet']['channelTitle']
        video_data['date'] = video['snippet']['publishedAt']
        video_data['views'] = video['statistics']['viewCount']
        video_data['channelIcon'] = video['channelIcon']

        if 'maxres' in video['snippet']['thumbnails']:
            video_data['thumbnail'] = video['snippet']['thumbnails']['maxres']['url']
        elif 'standard' in video['snippet']['thumbnails']:
            video_data['thumbnail'] = video['snippet']['thumbnails']['standard']['url']
        else:
            continue
        # elif 'high' in video['snippet']['thumbnails']:
            # video_data['thumbnail'] = video['snippet']['thumbnails']['high']['url']

            # video_data['thumbnail'] = video['snippet']['thumbnails']['medium']['url']

            # continue
            # video_data['thumbnail'] = video['snippet']['thumbnails']['default']['url']

        data['items'].append(video_data)

    with open(FILE_NAME, 'w', encoding='utf-8') as data_file:
        json.dump(data, data_file, ensure_ascii=False, indent=4)


def retrieve_top_videos():
    """
    Retrieves cached top videos if the cached data is not older than a predefined duration. If the cache is stale (i.e., older than the predefined duration) or unavailable, fetch new data from the YouTube API and update the cache.
    """

    # Check if the file exists
    if os.path.exists('data.json'):
        # Get the content of the file
        with open(FILE_NAME, 'r', encoding='utf-8') as data_file:
            response = json.load(data_file)

        # Get the cached time and current time
        current_date = datetime.datetime.now()
        cached_date = datetime.datetime.strptime(response['timestamp'], '%Y-%m-%dT%H:%M:%S')

        difference_in_hours = (current_date - cached_date).total_seconds() / 3600

        # If the cached data is still valid
        if difference_in_hours > MAX_LIFETIME_HOURS:
            # Fetch the videos and re-read the file
            fetch_top_videos()

            with open(FILE_NAME, 'r', encoding='utf-8') as data_file:
                response = json.load(data_file)

    # Otherwise, if the file does not exist
    else:
        # Fetch the videos and re-read the file
        fetch_top_videos()

        with open(FILE_NAME, 'r', encoding='utf-8') as data_file:
            response = json.load(data_file)

    #Return only the videos, not the timestamp
    return response['items'] 

