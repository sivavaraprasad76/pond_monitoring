from celery import shared_task
from .models import PondData
from .utils import send_sms, is_in_healthy_range
from django.utils import timezone
from datetime import timedelta

@shared_task
def send_periodic_updates():
    latest_data = PondData.objects.order_by('user', '-timestamp').distinct('user')
    
    for data in latest_data:
        message = f"Latest pond data: DO: {data.dissolved_oxygen}, pH: {data.ph}, Temp: {data.temperature}, Turbidity: {data.turbidity}, TDS: {data.tds}"
        if not send_sms(data.user.phone_number, message):
            print(f"Failed to send SMS to {data.user.username}")

@shared_task
def check_conditions_and_alert():
    latest_data = PondData.objects.order_by('user', '-timestamp').distinct('user')
    
    for data in latest_data:
        if not is_in_healthy_range(data):
            if not data.aerator_status:
                # Turn on aerator
                data.aerator_status = True
                data.save()
                if not send_sms(data.user.phone_number, "Alert: Pond conditions out of range. Aerator turned on."):
                    print(f"Failed to send alert SMS to {data.user.username}")
            else:
                # Check if it's been more than 30 minutes since the last check
                if data.timestamp < timezone.now() - timedelta(minutes=30):
                    if not send_sms(data.user.phone_number, "Alert: Pond conditions still out of range after aerator activation."):
                        print(f"Failed to send follow-up alert SMS to {data.user.username}")