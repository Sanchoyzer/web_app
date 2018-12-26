from django.test import TestCase
from django.utils import timezone

from test_forms.models import EmailLog


class EmailLogModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        EmailLog.objects.create(date=timezone.now(), is_success=True)

    def test_date_label(self):
        email = EmailLog.objects.get(id=1)
        field_label = email._meta.get_field('date').verbose_name
        self.assertEquals(field_label, 'Дата отправки')
        
    def test_is_success_label(self):
        email = EmailLog.objects.get(id=1)
        field_label = email._meta.get_field('is_success').verbose_name
        self.assertEquals(field_label, 'Успешно?')

    def test_check_is_success_val(self):
        email = EmailLog.objects.get(id=1)
        self.assertEquals(email.is_success, True)
