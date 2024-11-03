# KaOs Monitor

## Features

- Fetches the latest posts from a specified web page.
- Sends notifications to a Discord channel using a webhook URL.
- Plays a sound when a new post is detected.
- Logs activities and errors to a log file.

## Requirements

- Python 3.x
- `requests` library
- `beautifulsoup4` library
- `playsound` library

## Installation

- Download the latest release available on - [KaOs Monitor GitHub](https://github.com/phoenix1of1/KaOs-monitor)
- Extract to your prefered location.
- If you want to use the Discord feature, open monitor_latest_posts.py in your favourite editor and find: webhook_url = 'your_discord_webhook_url_here'
- Insert your Discord webhook then save and close.
- Open a terminal, navigate to where the script is saved then type monitor_latest_posts.py
- To close the script, use CTRL + C

## Sound Options

- If you want to change the soundfile used, open monitor_latest_posts.py in your favourite editor.
- Find the following line - sound_file_path = os.path.join(script_dir, 'success game.mp3')
- Edit 'success game.mp3' with the name of your soundfile.
- Ensure the soundfile is in the same directory as the script.
- Save, close and start the script with the instructions above.

## Licence

This project is licensed under the MIT License. See the LICENSE file for details.
