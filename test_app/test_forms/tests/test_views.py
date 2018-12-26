from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from test_forms.models import EmailLog
from test_forms.views import send_email_background


class UsersListViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        number_of_users = 10
        for user_num in range(number_of_users):
            user = User.objects.create_user(username=f'test{user_num}')

    def test_view_url_exists_at_desired_location(self):
        resp = self.client.get('/test_forms/users/')
        self.assertEqual(resp.status_code, 200)
           
    def test_view_url_accessible_by_name(self):
        resp = self.client.get(reverse('forms-users'))
        self.assertEqual(resp.status_code, 200)
        
    def test_view_uses_correct_template(self):
        resp = self.client.get(reverse('forms-users'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'test_forms/users.html')


class EmailTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        User.objects.create_superuser(username='test', email='someemail@somedoman@.com', password='123')

    def test_send_email(self):
        count_log_before = EmailLog.objects.all().count()
        self.assertEqual(count_log_before, 0)
        send_email_background('email_subject', 'email_msg')
        count_log_after = EmailLog.objects.all().count()
        self.assertEqual(count_log_after, 1)
        email = EmailLog.objects.get(id=1)
        self.assertEqual(email.is_success, True)
