from django.forms import ModelForm
from django import forms
from wishlist_app.models import User


class UserUpdateForm(ModelForm):
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)
    email = forms.EmailField(max_length=75)

    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name",)

