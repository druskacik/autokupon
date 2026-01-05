import os
import requests

from dotenv import load_dotenv
load_dotenv()

def send_promotion_notification(count: int):
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    
    payload = {
        "chat_id": chat_id,
        "text": f"LIDL Promotions Activated: {count}"
    }
    
    response = requests.post(url, json=payload)
    response.raise_for_status()

def send_error_notification(error: str):
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    
    payload = {
        "chat_id": chat_id,
        "text": f"LIDL Promotions Error: {error}"
    }
    
    response = requests.post(url, json=payload)
    response.raise_for_status()
