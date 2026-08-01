import requests
from config import TELEGRAM_TOKEN, CHAT_ID

def send_alert(message):
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        data = {"chat_id": CHAT_ID, "text": message}
        requests.post(url, data=data)
    except:
        print("Alert failed")