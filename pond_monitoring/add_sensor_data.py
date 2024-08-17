import os
import django
import random
from datetime import datetime, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pond_monitoring.settings')
django.setup()

from monitoring.models import User, PondData

def add_sensor_data():
    users = User.objects.all()
    for user in users:
        PondData.objects.create(
            phone_number=user,
            dissolved_oxygen=random.uniform(3, 14),
            pH=random.uniform(4, 9),
            temperature=random.uniform(18, 42),
            turbidity=random.uniform(0.5, 11),
            tds=random.uniform(0.5, 11)
        )

if __name__ == '__main__':
    add_sensor_data()