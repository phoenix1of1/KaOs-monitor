import requests
from bs4 import BeautifulSoup
from datetime import datetime
import time
import os
import tempfile
import pickle
from logging_config import setup_logger
from discord_notifier import send_discord_notification
import winsound

# URL of the web page to monitor
url = 'https://kaoskrew.org/viewforum.php?f=13'
# Discord webhook URL
webhook_url = 'webhook url here'

# Setup logger
logger = setup_logger('monitor_logger', 'monitor_log.txt')

# Create a temporary directory to store fetched web pages
temp_dir = tempfile.mkdtemp()
cache_file = os.path.join(temp_dir, 'latest_post_cache.pkl')

def fetch_latest_posts():
    try:
        # Fetch the web page content
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        logger.debug('Fetched web page content successfully.')

        # Save the web page content to a temporary file
        temp_file_path = os.path.join(temp_dir, 'latest_page.html')
        with open(temp_file_path, 'w', encoding='utf-8') as temp_file:
            temp_file.write(response.text)
        logger.debug(f'Saved web page content to {temp_file_path}.')

        # Parse the HTML content
        soup = BeautifulSoup(response.content, 'html.parser')
        logger.debug('Parsed HTML content successfully.')

        # Find all <a> tags with class "topictitle" and corresponding <time> tags
        title_tags = soup.find_all('a', class_='topictitle')
        posts = []
        for title_tag in title_tags:
            parent_div = title_tag.find_parent('div')
            time_tag = parent_div.find('time') if parent_div else None
            datetime_str = time_tag.get('datetime') if time_tag else None
            if datetime_str:
                title = title_tag.text
                posts.append((datetime.fromisoformat(datetime_str), title))
        logger.debug(f'Extracted {len(posts)} posts with datetime and titles.')

        # Sort the posts in descending order by datetime
        posts.sort(reverse=True, key=lambda x: x[0])

        # Load the cached latest post datetime
        if os.path.exists(cache_file):
            with open(cache_file, 'rb') as cache:
                cached_latest_post = pickle.load(cache)
        else:
            cached_latest_post = None

        # Check if the latest post is newer than the cached latest post
        if not cached_latest_post or posts[0][0] > cached_latest_post:
            # Print the latest three posts with different colors
            latest_posts = ""
            colors = ["\033[92m", "\033[93m", "\033[91m"]  # Green, Yellow, Red
            for i, (dt, title) in enumerate(posts[:3]):
                latest_posts += f"{colors[i]}{dt} - {title}\033[0m\n"
            print(latest_posts)
            logger.info('Printed the latest three posts.')

            # Send notification to Discord
            send_discord_notification(webhook_url, latest_posts)
            logger.info('Sent notification to Discord.')

            # Play the success sound
            winsound.PlaySound('success game.mp3', winsound.SND_FILENAME)

            # Update the cached latest post datetime
            with open(cache_file, 'wb') as cache:
                pickle.dump(posts[0][0], cache)
            logger.info('Updated the cached latest post datetime.')

    except Exception as e:
        logger.error(f'Error occurred: {e}')
        print(f"\033[91mError occurred: {e}\033[0m")  # Print error in red

# Run the script every 5 minutes
while True:
    try:
        fetch_latest_posts()
        # Wait for 5 minutes (300 seconds)
        for remaining in range(300, 0, -1):
            print(f"\033[94mNext check in {remaining} seconds\033[0m", end='\r')
            time.sleep(1)
    except Exception as e:
        logger.error(f'Unexpected error: {e}')
        print(f"\033[91mUnexpected error: {e}\033[0m")  # Print unexpected error in red
        time.sleep(300)  # Wait for 5 minutes before retrying