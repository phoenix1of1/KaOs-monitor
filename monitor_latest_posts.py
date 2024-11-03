import requests
import feedparser
from datetime import datetime
import time
import os
import tempfile
import pickle
from logging_config import setup_logger
from discord_notifier import send_discord_notification
from playsound import playsound

# URL of the RSS feed to monitor
rss_url = 'https://kaoskrew.org/feed'
# Discord webhook URL
webhook_url = 'webhook url here'

# Setup logger
logger = setup_logger('monitor_logger', 'monitor_log.txt')

# Create a temporary directory to store fetched RSS feed
temp_dir = tempfile.mkdtemp()
cache_file = os.path.join(temp_dir, 'latest_post_cache.pkl')

def fetch_latest_posts():
    try:
        # Fetch the RSS feed content
        response = requests.get(rss_url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        logger.debug('Fetched RSS feed content successfully.')

        # Save the RSS feed content to a temporary file
        temp_file_path = os.path.join(temp_dir, 'latest_feed.xml')
        with open(temp_file_path, 'w', encoding='utf-8') as temp_file:
            temp_file.write(response.text)
        logger.debug(f'Saved RSS feed content to {temp_file_path}.')

        # Parse the RSS feed content
        feed = feedparser.parse(response.content)
        logger.debug('Parsed RSS feed content successfully.')

        # Extract posts from the RSS feed
        posts = []
        for entry in feed.entries:
            if entry.title.startswith("KaOs Game Releases"):
                post = {
                    'title': entry.title,
                    'link': entry.link,
                    'published': entry.published_parsed
                }
                posts.append(post)
                logger.debug(f'Found post: {post["title"]} published at {post["published"]}.')

        # Sort posts by published date in descending order and get the latest three
        posts.sort(key=lambda x: x['published'], reverse=True)
        latest_three_posts = posts[:3]

        return latest_three_posts

    except Exception as e:
        logger.error(f'Error fetching latest posts: {e}')
        return []

def format_time(struct_time):
    return time.strftime('%Y-%m-%d %H:%M:%S', struct_time)

# Example usage
if __name__ == "__main__":
    cycle_counter = 0
    previous_titles = []
    script_dir = os.path.dirname(os.path.abspath(__file__))
    sound_file_path = os.path.join(script_dir, 'success game.mp3')
    
    while True:
        cycle_counter += 1
        os.system('cls')  # Clear the terminal output on Windows
        print(f"Cycle {cycle_counter}: Fetching latest posts...")
        latest_posts = fetch_latest_posts()
        latest_titles = [post['title'] for post in latest_posts]
        
        # Check for new posts
        if previous_titles and latest_titles != previous_titles:
            playsound(sound_file_path)  # Play the sound file
        
        previous_titles = latest_titles
        
        colors = ['\033[92m', '\033[93m', '\033[91m']  # Green, Yellow, Red
        for i, post in enumerate(latest_posts):
            color = colors[i] if i < len(colors) else '\033[0m'  # Default color if out of range
            readable_time = format_time(post["published"])
            print(f'{color}Title: {post["title"]}, Link: {post["link"]}, Published: {readable_time}\033[0m')
        
        # Dynamic countdown timer for the 5-minute cycle
        for remaining in range(300, 0, -1):
            print(f"New cycle starting in {remaining} seconds...", end='\r')
            time.sleep(1)