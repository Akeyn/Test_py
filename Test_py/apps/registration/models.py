from django.contrib.sessions.backends.db import SessionStore
from django.db import models
import time


# Create your models here.


class Country(models.Model):
    country_id = models.BigIntegerField(primary_key=True)
    country_code = models.CharField(max_length=2)
    country_name = models.TextField(max_length=32)

    def __str__(self):
        return str(self.country_name)


class Subscriber(models.Model):
    email = models.EmailField(max_length=64)
    firstName = models.CharField(max_length=32)
    secondName = models.CharField(max_length=32, null=True, blank=True)
    login = models.CharField(max_length=32)
    password = models.CharField(max_length=256)  # Сделать не изменяемым в админке
    birthday = models.DateField(null=True, blank=True)  # Сделать не изменяемым в админке
    country = models.IntegerField(choices=Country.objects.values_list('country_id', 'country_name'), null=True,
                                  blank=True)
    created_at = models.IntegerField(default=int(time.time()))  # timestamp - генерация при регистрации
    picture = models.ImageField(null=True, blank=True, upload_to="images/", verbose_name='Picture')

    def __str__(self):
        return str(str(self.id) + ' ' + self.login + ' ' + self.email)


class TypeMeter(models.Model):
    type_meter_name = models.CharField(max_length=32)
    metric_name = models.CharField(max_length=32)

    def __str__(self):
        return str(self.type_meter_name)


class Meter(models.Model):
    type_meter_id = models.BigIntegerField(choices=TypeMeter.objects.values_list('id', 'type_meter_name'), null=True,
                                           blank=True)  # TODO
    date_of_creation = models.DateField(null=True, blank=True)
    pulses_per_hour = models.IntegerField(null=True, blank=True)
    max_value = models.FloatField(null=True, blank=True)
    min_value = models.FloatField(null=True, blank=True)
    value = models.FloatField(null=True, blank=True)
    cost = models.FloatField(null=True, blank=True)
    recognized_id = models.CharField(max_length=32, null=True, blank=True)
    subscriber_id = models.IntegerField()

    def __str__(self):
        return str(self.recognized_id)


class HistoryMeter(models.Model):
    meter_id = models.BigIntegerField()
    min_value = models.FloatField(null=True, blank=True)
    end_value = models.FloatField(null=True, blank=True)
    difference = models.FloatField(null=True, blank=True)
    current_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return str(self.id)
