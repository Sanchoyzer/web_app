from django import forms


class UserRegistrationForm(forms.Form):
    username = forms.CharField(
        required=True,
        label='Логин',
        max_length=32
    )
    password = forms.CharField(
        required=True,
        label='Пароль',
        max_length=32,
        widget=forms.PasswordInput()
    )


class UserFeedbackForm(forms.Form):
    email = forms.EmailField(
        required=True,
        label='Ваш email'
    )
    text = forms.CharField(
        required=True,
        label='Сообщение',
        max_length=256,
        widget=forms.Textarea
    )
