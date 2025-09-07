import requests
from core.settings import BOT_TOKEN

# Telegramga oddiy xabar yuborish
def send_telegram_message(telegram_id, message, inline_buttons=None):
    url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage'
    data = {
        'chat_id': telegram_id,
        'text': message
    }
    if inline_buttons:
        data['reply_markup'] = {
            'inline_keyboard': [
                [{'text': btn['text'], 'callback_data': btn['callback_data']} for btn in inline_buttons]
            ]
        }
    response = requests.post(url, data=data)
    return response

# Telegramga manzil yuborish (geolokatsiya)
def send_telegram_location(telegram_id, latitude, longitude):
    url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendLocation'
    data = {
        'chat_id': telegram_id,
        'latitude': latitude,
        'longitude': longitude
    }
    response = requests.post(url, data=data)
    return response