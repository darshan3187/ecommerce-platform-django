from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User


class RegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        base_classes = (
            "mt-1 block w-full rounded-md border border-gray-300 "
            "px-3 py-2 text-sm text-gray-900 shadow-sm "
            "focus:border-indigo-500 focus:ring-indigo-500"
        )

        self.fields['username'].widget.attrs.update({
            "class": base_classes,
            "placeholder": "Enter username",
        })

        self.fields['email'].widget.attrs.update({
            "class": base_classes,
            "placeholder": "Enter email",
        })

        self.fields['password1'].widget.attrs.update({
            "class": base_classes,
            "placeholder": "Enter password",
        })

        self.fields['password2'].widget.attrs.update({
            "class": base_classes,
            "placeholder": "Confirm password",
        })
