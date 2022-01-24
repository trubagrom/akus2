from django.db import models
from django.contrib.auth.models import User


class UserInstuments(models.Model):
    # name = models.CharField('Имя', max_length=20)
    # login = models.CharField('Логин', max_length=20)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    instrument = models.ManyToManyField("Instruments")

    def __str__(self):
        return str(self.user)


class BandVacanction(models.Model):
    instrument = models.ForeignKey("Instruments", on_delete=models.RESTRICT)
    person = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    band = models.ForeignKey("Band", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.person} + {self.instrument.name} = {self.band.name}"


class Band(models.Model):
    name = models.CharField('Название', max_length=200)
    link = models.CharField('Ссылка на чат', max_length=500, null=True, blank=True)
    about = models.CharField('Описание', max_length=500, null=True, blank=True)

    def __str__(self):
        return self.name


class Instruments(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


