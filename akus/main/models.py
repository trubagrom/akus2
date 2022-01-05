from django.db import models


class User(models.Model):
    name = models.CharField('Имя', max_length=20)
    login = models.CharField('Логин', max_length=20)

    def __str__(self):
        return self.name


class Instruments(models.Model):
    name = models.CharField(max_length=255)

