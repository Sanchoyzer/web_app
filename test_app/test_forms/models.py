from django.db import models


class EmailLog(models.Model):
    date = models.DateTimeField(verbose_name='Дата отправки', db_index=True, auto_now_add=True)
    is_success = models.BooleanField(verbose_name='Успешно?', db_index=True, default=False)

    class Meta:
        verbose_name = 'Строка лога отправки email'
        verbose_name_plural = 'Лог отправки email'
