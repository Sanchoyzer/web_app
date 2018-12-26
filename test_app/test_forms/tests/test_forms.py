from django.test import TestCase

from test_forms.forms import UserFeedbackForm


class UserFeedbackFormTest(TestCase):

    def test_feedback_form_email_correct(self):
        form_data = {'email': 'login@domen.com', 'text': 'some text'}
        form = UserFeedbackForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_feedback_form_email_incorrect(self):
        form_data = {'email': 'login_domen.com', 'text': 'some text'}
        form = UserFeedbackForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_feedback_form_email_field_label(self):
        form = UserFeedbackForm()
        self.assertTrue(form.fields['email'].label == 'Ваш email')

    def test_feedback_form_text_field_label(self):
        form = UserFeedbackForm()
        self.assertTrue(form.fields['text'].label == 'Сообщение')
