from django.db import models


class PhoneBook(models.Model):
    name = models.CharField(verbose_name='Имя', db_index=True, max_length=32)
    phone = models.CharField(verbose_name='Телефон', db_index=True, max_length=12)
