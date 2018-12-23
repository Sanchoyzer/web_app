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
