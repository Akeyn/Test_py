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
    secondName = models.CharField(max_length=32)
    login = models.CharField(max_length=32)
    password = models.CharField(max_length=256)  # Сделать не изменяемым в админке
    birthday = models.DateField()  # Сделать не изменяемым в админке
    country = models.IntegerField(choices=Country.objects.values_list('country_id', 'country_name'))
    created_at = models.IntegerField(default=int(time.time()))  # timestamp - генерация при регистрации

    def __str__(self):
        return str(str(self.id) + ' ' + self.login + ' ' + self.email)