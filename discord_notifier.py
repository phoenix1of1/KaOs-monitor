import requests
import logging

def send_discord_notification(webhook_url, message):
    """Send a notification to a Discord channel using a webhook URL."""
    data = {
        "content": message
    }
    try:
        response = requests.post(webhook_url, json=data)
        response.raise_for_status()
        logging.debug('Notification sent successfully.')
    except Exception as e:
        logging.error(f'Failed to send notification: {e}')