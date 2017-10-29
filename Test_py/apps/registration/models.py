from django.db import models

# Create your models here.


class Country(models.Model):

    country_id = models.BigIntegerField(primary_key=True)
    country_code = models.CharField(max_length=2)
    country_name = models.TextField(max_length=32)

    def __str__(self):
        return str(self.country_name)


class Subscriber(models.Model):

    # user_id = models.BigIntegerField(primary_key=True)
    email = models.EmailField(max_length=64)
    firstName = models.CharField(max_length=32)
    secondName = models.CharField(max_length=32)
    login = models.CharField(max_length=32)
    password = models.CharField(max_length=32)
    date = models.DateField()
    country = models.CharField(max_length=32, choices=Country.objects.values_list('country_code', 'country_name'))

    def __str__(self):
        return str(str(self.id) + ' ' + self.login + ' ' + self.email)