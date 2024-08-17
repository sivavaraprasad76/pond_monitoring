
from twilio.rest import Client
from django.conf import settings


def is_in_healthy_range(data):
    return (6.5 <= data.dissolved_oxygen <= 8.0 and
            6.5 <= data.ph <= 8.5 and
            20 <= data.temperature <= 30 and
            data.turbidity <= 50 and
            data.tds <= 1000)


import requests
from django.conf import settings

def format_phone_number(phone_number):
    # Remove any non-digit characters
    phone_number = ''.join(filter(str.isdigit, phone_number))
    
    # Ensure the number is 10 digits (assuming Indian mobile numbers)
    if len(phone_number) == 10:
        return phone_number
    elif len(phone_number) == 12 and phone_number.startswith('91'):
        return phone_number[2:]
    else:
        raise ValueError("Invalid phone number format")

def send_sms(to_number, message):
    formatted_number = format_phone_number(to_number)
    url = "https://www.fast2sms.com/dev/bulkV2"
    
    payload = {
        'authorization': settings.FAST2SMS_API_KEY,
        'route': 'q',  # Use 'q' for Quick SMS
        'message': message,
        'language': 'english',
        'flash': 0,
        'numbers': formatted_number,
    }
    
    headers = {
        'cache-control': "no-cache"
    }
    
    try:
        response = requests.request("POST", url, data=payload, headers=headers)
        response_data = response.json()
        
        if response_data['return']:
            print(f"SMS sent successfully to {formatted_number}")
            return True
        else:
            print(f"Failed to send SMS to {formatted_number}: {response_data['message']}")
            return False
    except Exception as e:
        print(f"Error sending SMS: {str(e)}")
        return False