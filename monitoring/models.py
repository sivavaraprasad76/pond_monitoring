from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class User(models.Model):
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15, unique=True)
    password = models.CharField(max_length=100)

class PondData(models.Model):
    phone_number = models.CharField(max_length=15)
    timestamp = models.DateTimeField(auto_now_add=True)
    dissolved_oxygen = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(20)])
    ph = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(14)])
    temperature = models.FloatField()
    turbidity = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(1000)])
    tds = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(1000)])

class AeratorStatus(models.Model):
    phone_number = models.CharField(max_length=15)
    is_on = models.BooleanField(default=False)

class PondNote(models.Model):
    phone_number = models.CharField(max_length=15)
    note = models.TextField()

class HealthyRange:
    DO_MIN = 4
    PH_MIN = 5
    PH_MAX = 8
    TEMP_MIN = 23
    TEMP_MAX = 35
    TDS_TARGET = 10
    TURBIDITY_TARGET = 10

# ... rest of the models remain the same ...